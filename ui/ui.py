from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton

import pika
import json
from thread import start_new_thread
import time
from wifi import Cell, Scheme

from audio_player import AudioPlayer
from releasable_slider import ReleasableSlider

class Main(FloatLayout):
    pass

class NightstandApp(App):

    def build(self):
        self.player = AudioPlayer()
        
        self.main = Main()
        self.main.manager.state = 'main'
        self.main.ids.volume_slider.bind(value=self.on_volume_slider_change)
        data = [{'text': str(i), 'is_selected': False} for i in range(100)]
        data = map(lambda cell: {'text': cell.ssid, 'is_selected': False}, Cell.all('en0'))

        args_converter = lambda row_index, rec: {'text': rec['text'],
                                         'size_hint_y': None,
                                         'height': 75}

        list_adapter = ListAdapter(data=data,
                           args_converter=args_converter,
                           cls=ListItemButton,
                           selection_mode='single',
                           allow_empty_selection=False)
        self.main.ids.wifi_networks.adapter = list_adapter

        self.current_uid = None

        start_new_thread(self.update_seek_slider, ())
        
        return self.main

    def on_volume_slider_change(self, instance, value):
        self.player.set_volume(value)

    def seek_to_user(self):
        new_position = self.main.ids.seek_slider.value
        self.player.seek(new_position)

    def show_playing_screen(self):
        self.root.manager.current = 'playing'
        self.root.manager.state = 'playing'

    def update_seek_slider(self):
        while True:
            if self.player.is_playing():
                (position, length) = self.player.seek_information()
                self.main.ids.seek_slider.range = (0, length)
                self.main.ids.seek_slider.value = position

            time.sleep(1)

    def togglePause(self):
        if self.player is not None:
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.resume()

    def message_received(self, channel, method, properties, body):
        message = json.loads(body)
        
        print message['uid'] + ' / ' + message['event']
    
        if message['event'] == 'figurine_added':
            if self.current_uid == message['uid']:
                print "resuming by adding figurine"
                self.player.resume()
            else:
                self.player.play_audio(message['uid'])

            self.current_uid = message['uid']

            self.show_playing_screen()
        elif message['event'] == 'figurine_removed':
            self.player.pause()

            self.root.manager.current = 'main'
            self.root.manager.state = 'main'

if __name__ == '__main__':
    app = NightstandApp()

    connection_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    channel.queue_declare(queue='nightstand-audio')
    
    channel.basic_consume(app.message_received,
                          queue='nightstand-audio',
                          no_ack=True)
    
    start_new_thread(channel.start_consuming, ())

    app.run()
