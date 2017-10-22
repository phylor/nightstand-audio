import os
import json

class Figurine:
    audio_directory = 'data/audio'
    figurine_directory = 'data/figurines'

    def __init__(self, uid):
        self.uid = uid

        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path(), 'r') as figurine:
                data=figurine.read()
                self.data = json.loads(data)
        except IOError:
            self.data = {}

    def file_path(self):
        return os.path.abspath(os.path.join(Figurine.figurine_directory, self.uid + '.json'))

    def get_audio_path(self):
        return os.path.abspath(os.path.join(Figurine.audio_directory, self.data['audio_path']))
