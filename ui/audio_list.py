from kivy.uix.recycleview import RecycleView

import os
import glob
import json
import fnmatch
import sys
import unicodedata

class AudioList(RecycleView):
    def __init__(self, **kwargs):
        super(AudioList, self).__init__(**kwargs)

    def show_all(self):
        audio_files = self.files()
        self.data = map(lambda audio: { 'name': os.path.basename(audio), 'directory': os.path.relpath(os.path.dirname(audio), self.audio_directory) }, audio_files)

    def show_unused(self):
        audio_files = self.unused_files()
        self.data = map(lambda audio: { 'name': os.path.basename(audio), 'directory': os.path.relpath(os.path.dirname(audio), self.audio_directory) }, audio_files)

    def files(self):
        file_types = ('*.mp3', '*.wav', '*.ogg')
        audio_files = []

        for files in file_types:
            for root, dirnames, filenames in os.walk(self.audio_directory):
                for filename in fnmatch.filter(filenames, files):
                    if not filename.startswith('.'):
                        if not sys.platform.startswith('linux'): # OS X workaround
                            filename = unicodedata.normalize('NFC', unicode(filename, 'utf-8')).encode('utf-8')
                        audio_files.append(os.path.join(root, filename))

        return audio_files

    def set_selection(self, data):
        self.selection = data

    def used_files(self):
        files = []

        for json_file in glob.glob(os.path.join(self.data_directory, 'figurines', '*.json')):
            with open(json_file, 'r') as json_data:
                data = json_data.read()
                files.append(json.loads(data)['audio_path'])

        return files

    def unused_files(self):
        all_files = set(self.files())
        used_files = set(self.used_files())

        return [item for item in all_files if item not in used_files]
