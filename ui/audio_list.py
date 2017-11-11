from kivy.uix.recycleview import RecycleView

import os
import glob

class AudioList(RecycleView):
    def __init__(self, **kwargs):
        super(AudioList, self).__init__(**kwargs)

    def show_all(self):
        audio_files = self.files()
        self.data = map(lambda audio: { 'name': os.path.basename(audio), 'directory': os.path.relpath(os.path.dirname(audio), self.audio_directory) }, audio_files)

    def files(self):
        file_types = ('*.mp3', '*.wav', '*.ogg')
        audio_files = []

        for files in file_types:
            audio_files.extend(glob.glob(os.path.join(self.audio_directory, '**/' + files)))

        return audio_files

    def set_selection(self, data):
        self.selection = data
