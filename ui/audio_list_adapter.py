from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
import os
import glob

class AudioListAdapter(ListAdapter):
    def __init__(self, data_directory):
        self.audio_directory = os.path.join(data_directory, 'audio')
        audio_files = self.files()

        data = map(lambda audio: {'text': os.path.relpath(audio, self.audio_directory), 'is_selected': False}, audio_files)

        args_converter = lambda row_index, rec: {'text': rec['text'],
                                         'size_hint_y': None,
                                         'height': 75, 'font_size': 40}

        super(ListAdapter, self).__init__(
                           data=data,
                           args_converter=args_converter,
                           cls=ListItemButton,
                           selection_mode='single',
                           allow_empty_selection=False)

    def files(self):
        file_types = ('*.mp3', '*.wav', '*.ogg')
        audio_files = []
        for files in file_types:
            audio_files.extend(glob.glob(os.path.join(self.audio_directory, '**/' + files)))

        return audio_files
