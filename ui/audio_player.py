import pika
import json
from kivy.core.audio import SoundLoader
import glob
import os
import time

class AudioPlayer:
    
    def __init__(self):
        self.current_audio = None
        self.current_position = 0
        self.uid = None

    def play_audio(self, uid):
        self.uid = uid
        audio_path = ''
        
        for file in glob.glob('data/audio/' + uid + '*'):
            audio_path = file
    
        audio_path = os.path.abspath(audio_path)
        
        self.stop_audio()
        self.current_audio = SoundLoader.load(audio_path)
        self.current_audio.play()

    def stop_audio(self):
        if self.current_audio is not None:
            self.current_audio.stop()
            self.current_audio = None

    def pause(self):
        if self.current_audio is not None:
            self.current_position = self.current_audio.get_pos()
            self.current_audio.stop()
    
    def is_playing(self):
        if self.current_audio is None:
            return False
        else:
            return self.current_audio.state == 'play'

    def resume(self):
        if self.current_audio is not None:
            self.seek(self.current_position)

    def set_volume(self, volume):
        if self.current_audio is not None:
            self.current_audio.volume = volume

    def seek(self, target):
        if self.current_audio is not None:
            # Some audio providers can not seek when it's not playing
            self.current_audio.play()
            time.sleep(0.5) # Without delay, seek does not have any effect
            self.current_audio.seek(target)

    def seek_information(self):
        if self.current_audio is None:
            return (0, 0)
        else:
            return (self.current_audio.get_pos(), self.current_audio.length)

    def get_cached_position(self):
        return self.current_position
