import os
import json

class Figurine:
    audio_directory = 'audio'
    figurine_directory = 'figurines'

    def __init__(self, uid, data_directory):
        self.uid = uid
        self.data_directory = data_directory

        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path(), 'r') as figurine:
                data = figurine.read()
                self.data = json.loads(data)
        except IOError:
            self.data = {}

    def file_path(self):
        return os.path.abspath(os.path.join(self.data_directory, Figurine.figurine_directory, self.uid + '.json'))

    def get_audio_path(self):
        return os.path.abspath(os.path.join(self.data_directory, Figurine.audio_directory, self.data['audio_path']))

    def exists(self):
        return 'audio_path' in self.data

    def save(self, audio_path):
        self.data = {'uid': self.uid, 'audio_path': audio_path}

        with open(self.file_path(), 'w') as figurine:
            figurine.write(json.dumps(self.data))

    def delete(self):
        os.remove(self.file_path())
