from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.utils import platform
import os

class MyApp(App):

    def build(self):
        font_path = os.path.join(os.path.dirname(__file__), "font", "NotoSansJP-ExtraBold.ttf")
        resource_add_path(os.path.dirname(font_path))
        LabelBase.register(DEFAULT_FONT, font_path)
        self.img_path = "./img/barbecue.png"
        self.img_widget = Image(source=self.img_path)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="ヴァンヴァーがー"))
        layout.add_widget(self.img_widget)
        return layout
if __name__ == "__main__":

    MyApp().run()