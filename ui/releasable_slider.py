from kivy.uix.slider import Slider

class ReleasableSlider(Slider):
    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super(ReleasableSlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(ReleasableSlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            self.dispatch('on_release')
            return True
