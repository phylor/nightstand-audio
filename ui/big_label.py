from kivy.uix.label import Label

class BigLabel(Label):
    def __init__(self, **kwargs):
        super(BigLabel, self).__init__(**kwargs)

        self.bold = True
        self.font_size = 75
        self.padding = (50, 50)
