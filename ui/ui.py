from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import NoTransition
from kivy.clock import Clock
from kivy.config import Config

import pika
import json
from thread import start_new_thread
import time
import glob
import os
import sys

from audio_player import AudioPlayer
from releasable_slider import ReleasableSlider
from big_label import BigLabel
from figurine import Figurine
sys.path.append(os.path.abspath("./rfid_reader"))
from reader import RfidReader

if sys.platform.startswith('linux'):
    Config.set('graphics', 'fullscreen', 'auto')
else:
    Config.set('graphics', 'width', 800)
    Config.set('graphics', 'height', 480)

class Main(FloatLayout):
    pass

class NightstandApp(App):
    def __init__(self):
        super(NightstandApp, self).__init__()

        self.player = AudioPlayer()
        self.current_uid = None

        self.reader = RfidReader()

    def build(self):
        self.main = Main()
        self.main.manager.state = 'main'
        self.main.manager.transition = NoTransition()
        self.main.ids.volume_slider.bind(value=self.on_volume_slider_change)
        data = map(lambda audio: {'text': os.path.basename(audio), 'is_selected': False}, glob.glob('data/audio/*'))

        args_converter = lambda row_index, rec: {'text': rec['text'],
                                         'size_hint_y': None,
                                         'height': 75}

        self.list_adapter = ListAdapter(data=data,
                           args_converter=args_converter,
                           cls=ListItemButton,
                           selection_mode='single',
                           allow_empty_selection=False)
        self.main.ids.audio_list.adapter = self.list_adapter


        start_new_thread(self.update_seek_slider, ())
        
        return self.main

    def on_volume_slider_change(self, instance, value):
        self.player.set_volume(value)

    def seek_to_user(self):
        new_position = self.main.ids.seek_slider.value
        self.player.seek(new_position)

    def show_playing_screen(self, restart_playback=True):
        self.root.manager.current = 'playing'
        self.root.manager.state = 'playing'

        if restart_playback:
            self.player.play(self.figurine.get_audio_path())

    def show_create_figurine_screen(self):
        self.root.manager.current = 'create_figurine'

    def update_seek_slider(self):
        while True:
            if self.player.is_playing():
                (position, length) = self.player.seek_information()
                self.main.ids.seek_slider.range = (0, length)
                self.main.ids.seek_slider.value = position

                self.main.ids.play_pause_button.text = 'Pause'
                self.main.ids.playing_label.text = 'Playing..'
            else:
                self.main.ids.play_pause_button.text = 'Play'
                self.main.ids.playing_label.text = ''

            time.sleep(1)

    def togglePause(self):
        if self.player is not None:
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.resume()

    def save_figurine(self):
        selected_audio_path = self.list_adapter.selection[0].text

        self.figurine = Figurine(self.current_uid)
        self.figurine.save(selected_audio_path)

        self.show_playing_screen()

    def message_received(self, uid, action):
        print uid + ' / ' + action
    
        if action == 'figurine_added':
            if self.current_uid == uid:
                self.show_playing_screen(False)
                self.player.resume()
            else:
                self.figurine = Figurine(uid)

                if self.figurine.exists():
                    self.show_playing_screen()
                else:
                    self.show_create_figurine_screen()

            self.current_uid = uid
        elif action == 'figurine_removed':
            self.player.pause()

            self.root.manager.current = 'main'
            self.root.manager.state = 'main'


    def check_rfid_reader(self, delta_time):
        self.reader.read_rfid(self.message_received)

if __name__ == '__main__':
    app = NightstandApp()

    Clock.schedule_interval(app.check_rfid_reader, 1 / 2.)

    app.run()
