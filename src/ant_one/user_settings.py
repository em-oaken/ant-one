import pickle
from pathlib import Path

class UserSettings:

    # Original settings
    def __init__(self, settings_path):
        self._name = 'Pretty Oecophylla Smaragdina'
        self._pimp_color_antennae = '#393A3E'
        self._pimp_color_body = '#393A3E'
        self._pimp_color_legs = '#393A3E'

        self.settings_path = settings_path
        self.load()
    
    # Getters and setters
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def pimp_color_antennae(self):
        return self._pimp_color_antennae
    
    @pimp_color_antennae.setter
    def pimp_color_antennae(self, value):
        self._pimp_color_antennae = value
    
    @property
    def pimp_color_body(self):
        return self._pimp_color_body
    
    @pimp_color_body.setter
    def pimp_color_body(self, value):
        self._pimp_color_body = value
    
    @property
    def pimp_color_legs(self):
        return self._pimp_color_legs
    
    @pimp_color_legs.setter
    def pimp_color_legs(self, value):
        self._pimp_color_legs = value
    
    # Save and load
    def save(self):
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_path, 'wb') as sf:
            pickle.dump(self, sf)
    
    def load(self):
        if self.settings_path.exists():
            with open(self.settings_path, 'rb') as sf:
                fetched_settings = pickle.load(sf)
            self.__dict__.update(fetched_settings.__dict__)
