# timing/scheduler.py
import time
from typing import Callable, List


class Task:
    """Représente une tâche à exécuter à intervalles fixes."""

    def __init__(self, interval: float, callback: Callable[[], None]):
        self.interval = interval  # Intervalle en secondes
        self.accumulation = 0.0  # Accumulateur pour savoir quand exécuter la tâche
        self.callback = callback  # Fonction à exécuter
    
    @classmethod
    def new(cls, interval: float, callback: Callable[[], None]) -> 'Task':
        """Crée une nouvelle tâche."""
        return cls(interval, callback)

    def update(self, dt: float) -> None:
        """Met à jour l'accumulateur et exécute la tâche si nécessaire."""
        self.accumulation += dt
        if self.accumulation >= self.interval:
            self.callback()  # Exécute la tâche
            self.accumulation -= self.interval  # Réinitialise l'accumulateur


class Scheduler:
    """Un planificateur simple pour exécuter des tâches à intervalles fixes."""

    def __init__(self):
        self.tasks: List[Task] = []

    @classmethod
    def new(cls) -> 'Scheduler':
        """Crée une nouvelle instance de Scheduler."""
        return cls()

    def add_task(self, interval: float, task: Callable[[], None]) -> None:
        """Ajoute une tâche au planificateur."""
        self.tasks.append(Task(interval, task))

    def replace(self, tasks: List[Callable[[], None]]) -> None:
        """Remplace toutes les tâches par les nouvelles tâches spécifiées."""
        self.reset()
        for t in tasks:
            self.add_task(0, t)

    def reset(self) -> None:
        """Réinitialise toutes les tâches."""
        self.tasks.clear()

    def update(self, dt: float) -> None:
        """Mise à jour des tâches, à appeler à chaque itération de la boucle."""
        for task in self.tasks:
            task.update(dt)
