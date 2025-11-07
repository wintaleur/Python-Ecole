import time
import timeit
from src.Utility.Scheduler import Scheduler
from src.Globals import gameParameters

class GameLoop:
    __isRunning = False
    __tickScheduler = Scheduler.new()
    __frameScheduler = Scheduler.new()
    __now = 0.0
    __last = 0.0
    __dt = 0.0
    __frameCount = 0
    __tickCount = 0
    __lastReportTime = 0.0
    __frameSpeedObjective = gameParameters["FrameSpeedObjective"]
    __tickSpeedObjective = gameParameters["TickSpeedObjective"]

    def __init__(self):
        pass

    @classmethod
    def new(cls) -> 'GameLoop':
        """Crée une nouvelle instance de GameLoop."""
        return cls()

    def __getMsTime(self):
        return time.perf_counter() * 1000  # Convertir en millisecondes

    def sleepMs(self, milliseconds: float):
        """
        Fait une pause pendant un nombre donné de millisecondes en utilisant timeit pour un contrôle actif.
        
        :param milliseconds: Nombre de millisecondes pendant lesquelles on souhaite dormir.
        """
        # Convertir les millisecondes en secondes
        target_time = milliseconds / 1000.0
        start_time = timeit.default_timer()
        
        # Attente active jusqu'à ce que le temps écoulé soit égal à target_time
        while timeit.default_timer() - start_time < target_time:
            pass  # Boucle active jusqu'à ce que le temps soit écoulé

    def run(self):
        self.setup()
        self.__isRunning = True
        self.loop()

    def stop(self):
        self.__isRunning = False

    @property
    def isRunning(self):
        return self.__isRunning

    def setup(self):
        self.__frameSpeedObjective = gameParameters["FrameSpeedObjective"]  # en FPS
        self.__tickSpeedObjective = gameParameters["TickSpeedObjective"]  # en TPS

    def loop(self):
        tickInterval = 1000.0 / self.__tickSpeedObjective  # Intervalle de tick en millisecondes
        frameInterval = 1000.0 / self.__frameSpeedObjective  # Intervalle de frame en millisecondes
        lastTickTime = self.__getMsTime()
        lastFrameTime = self.__getMsTime()
        timer = self.__getMsTime()  # Temps de départ pour les rapports FPS/TPS

        while self.__isRunning:
            self.__now = self.__getMsTime()
            elapsedTickTime = self.__now - lastTickTime  # Écoulé depuis le dernier tick
            elapsedFrameTime = self.__now - lastFrameTime  # Écoulé depuis le dernier frame

            tickReady = elapsedTickTime >= tickInterval
            frameReady = elapsedFrameTime >= frameInterval

            # Exécuter le tick si l'intervalle est atteint
            if tickReady:
                self.update(elapsedTickTime)
                lastTickTime = self.__now
                self.__tickCount += 1

            # Exécuter le frame si l'intervalle est atteint
            if frameReady:
                self.render()
                lastFrameTime = self.__now
                self.__frameCount += 1

            # Vérification des FPS et TPS toutes les secondes (calcul direct)
            if self.__now - timer >= 1000:
                # Calcul du tick et du frame ratio directement dans la boucle
                tickRatio = self.__tickCount / self.__tickSpeedObjective
                frameRatio = self.__frameCount / self.__frameSpeedObjective

                print(f"Tick Ratio: {tickRatio:.2f} ({self.__tickCount} ticks / {self.__tickSpeedObjective} objectif)")
                print(f"Frame Ratio: {frameRatio:.2f} ({self.__frameCount} frames / {self.__frameSpeedObjective} objectif)")

                # Réinitialiser les compteurs après le rapport
                self.__frameCount = 0
                self.__tickCount = 0

                # Réinitialisation du timer
                timer = self.__now

            # Calcul du temps restant avant la prochaine itération
            remainingTickTime = tickInterval - (self.__now - lastTickTime)
            remainingFrameTime = frameInterval - (self.__now - lastFrameTime)

            # Attente combinée si les deux ont besoin de dormir
            if remainingTickTime > 0 and remainingFrameTime > 0:
                # Attendre le plus longtemps des deux
                self.sleepMs(min(remainingTickTime, remainingFrameTime))
                
    def render(self):
        self.__frameScheduler.update(0)

    def update(self, dt: float):
        self.__tickScheduler.update(dt)
