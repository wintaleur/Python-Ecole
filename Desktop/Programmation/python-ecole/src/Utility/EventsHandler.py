class Event:
    """Classe représentant un événement auquel on peut connecter des callbacks."""
    
    def __init__(self):
        self.callbacks = []

    def connect(self, callback):
        """Connecte un callback à cet événement."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            print(f"Callback {callback.__name__} connecté à l'événement.")
        else:
            print(f"Callback {callback.__name__} est déjà connecté.")
    
    def trigger(self, *args, **kwargs):
        """Déclenche l'événement et appelle tous les callbacks connectés."""
        print("Déclenchement de l'événement...")
        for callback in self.callbacks:
            callback(*args, **kwargs)

class EventMixin:
    """Mixin permettant d'ajouter la gestion des événements."""
    
    def __init__(self):
        self.events = {}

    def create_event(self, event_name):
        """Crée un nouvel événement avec un nom spécifique."""
        if event_name not in self.events:
            self.events[event_name] = Event()
            print(f"Événement '{event_name}' créé.")
        return self.events[event_name]
    
    def get_event(self, event_name):
        """Récupère un événement existant par son nom."""
        return self.events.get(event_name, None)
