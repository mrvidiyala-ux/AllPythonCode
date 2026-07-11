from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Input field
        self.input_box = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=40,
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.input_box)

        # Buttons layout
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", ".", "+"],
            ["="]
        ]

        for row in buttons:
            row_layout = BoxLayout()
            for label in row:
                btn = Button(
                    text=label,
                    font_size=32,
                    on_press=self.on_button_press
                )
                row_layout.add_widget(btn)
            self.add_widget(row_layout)

    def on_button_press(self, instance):
        text = instance.text

        if text == "C":
            self.input_box.text = ""
        elif text == "=":
            try:
                self.input_box.text = str(eval(self.input_box.text))
            except Exception:
                self.input_box.text = "Error"
        else:
            self.input_box.text += text


class CalculatorApp(App):
    def build(self):
        return Calculator()


if __name__ == "__main__":
    CalculatorApp().run()

