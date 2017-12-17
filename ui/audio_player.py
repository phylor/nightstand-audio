import json
import glob
import time
from vlc import MediaPlayer

class AudioPlayer:
    
    def __init__(self):
        self.current_audio = MediaPlayer()

    def play(self, audio_path):
        self.audio_path = audio_path
        self.current_audio = MediaPlayer('file://' + audio_path)
        self.current_audio.play()

    def pause(self):
        self.current_audio.set_pause(True)
    
    def is_playing(self):
        return self.current_audio.is_playing()

    def resume(self):
	self.current_audio.set_pause(False)

    def set_volume(self, volume):
        volume = int(volume)
        self.current_audio.audio_set_volume(volume)

    def seek(self, target):
        self.current_audio.set_position(target)

    def seek_information(self):
        return (self.current_audio.get_position(), 1.0)

    def remaining(self):
        ms_left = (self.current_audio.get_length() - self.current_audio.get_time()) / 1000

        return '-' + str(int(ms_left / 60)) + ':' + str(int(ms_left % 60)).zfill(2)

    def replay(self):
        self.play(self.audio_path)
