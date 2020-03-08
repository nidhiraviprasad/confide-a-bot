import kivy
from kivy.app import App, runTouchApp
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import chat


class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))




class MyGrid(GridLayout):
	def __init__(self, **kwargs):
		super(MyGrid, self).__init__(**kwargs)
		self.rows=2
		self.cols=1

		Window.clearcolor = (0.502, 0.8196, 1, 0.98)

		self.cbot = chat.chatBot()

		self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.bottom = GridLayout(cols=2, spacing=3, size_hint=(1,0.15))
		self.root = ScrollView(size_hint=(1, 0.85))

		self.layout.bind(minimum_height=self.layout.setter('height'))
		l = WrappedLabel(text='Hello! How are you doing? (type bye anytime to stop)', size_hint=(1, None), padding=(5, 5), color=[0,0,0,1])
		self.layout.add_widget(l)

		self.root.add_widget(self.layout)
		self.textbox = TextInput(text='type here...', size_hint=(0.8, None))
		self.btn = Button(text='send', size_hint_x=None, width=75)
		self.btn.bind(on_press=self.pressed)

		self.bottom.add_widget(self.textbox)
		self.bottom.add_widget(self.btn)

		self.add_widget(self.root)
		self.add_widget(self.bottom)

	def pressed(self, instance):
		t = '|  ' + self.textbox.text
		nlabel = WrappedLabel(text = t, size_hint=(1, None), padding=(5, 5), color=[1,1,1,1])
		self.layout.add_widget(nlabel)
		self.root.scroll_to(nlabel)
		out = self.cbot.chat(t)
		nlabel2 = WrappedLabel(text=out, size_hint=(1, None), padding=(5, 5), color=[0,0,0,1])
		self.layout.add_widget(nlabel2)
		self.root.scroll_to(nlabel2)
		self.textbox.text = ""



class ConfideABotApp(App):
	def build(self):
		return MyGrid()




if __name__ == "__main__":
	ConfideABotApp().run()
