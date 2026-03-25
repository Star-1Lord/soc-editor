from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import struct

class Editor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.inputs = {}

        for name in ["Gold", "Wood", "Stone", "Ore", "Amber"]:
            ti = TextInput(hint_text=name, multiline=False)
            self.inputs[name] = ti
            self.add_widget(ti)

        btn = Button(text="APPLY")
        btn.bind(on_press=self.apply)
        self.add_widget(btn)

    def apply(self, instance):
        path = "/sdcard/Download/1.sav"

        with open(path, "rb") as f:
            data = f.read()

        values = [int(self.inputs[k].text or 0) for k in self.inputs]

        for i in range(0, len(data)-20, 4):
            vals = struct.unpack("<5I", data[i:i+20])
            if all(v < 1000000 for v in vals):
                data = data[:i] + struct.pack("<5I", *values) + data[i+20:]
                break

        with open("/sdcard/Download/edited.sav", "wb") as f:
            f.write(data)

class MyApp(App):
    def build(self):
        return Editor()

MyApp().run()
