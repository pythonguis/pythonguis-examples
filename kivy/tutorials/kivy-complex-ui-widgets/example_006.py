from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.bubble import Bubble, BubbleButton, BubbleContent
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class FormattingBubble(Bubble):
    def __init__(self, target_text, **kwargs):
        super().__init__(**kwargs)

        # Customizing the bubble
        self.size_hint = (None, None)
        self.size = (dp(120), dp(50))
        self.arrow_pos = "top_mid"
        self.orientation = "horizontal"
        self.target_label = target_text

        # Add formatting buttons
        bold_btn = BubbleButton(text="Bold")
        italic_btn = BubbleButton(text="Italic")
        bold_btn.bind(on_release=lambda x: self.on_format("bold"))
        italic_btn.bind(on_release=lambda x: self.on_format("italic"))

        # Add the buttons to the bubble
        bubble_content = BubbleContent()
        bubble_content.add_widget(bold_btn)
        bubble_content.add_widget(italic_btn)

        self.add_widget(bubble_content)

    def on_format(self, format_type):
        if format_type == "bold":
            self.target_label.text = f"[b]{self.target_label.text}[/b]"
        elif format_type == "italic":
            self.target_label.text = f"[i]{self.target_label.text}[/i]"
        self.parent.remove_widget(self)


class BubbleApp(App):
    title = "Bubble Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        root = FloatLayout()

        self.text = Label(
            text="Click this text to apply formatting",
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            markup=True,
        )
        self.text.bind(on_touch_down=self.show_bubble)

        root.add_widget(self.text)
        root.bind(on_touch_down=self.dismiss_bubbles)

        return root

    def show_bubble(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.remove_all_bubbles()
            bubble = FormattingBubble(target_text=self.text)
            bubble.pos = (touch.x - bubble.width / 2, touch.y - bubble.height - dp(10))
            self.root.add_widget(bubble)

    def dismiss_bubbles(self, instance, touch):
        if instance == self.root and not self.text.collide_point(*touch.pos):
            self.remove_all_bubbles()

    def remove_all_bubbles(self):
        for widget in self.root.children[:]:
            if isinstance(widget, FormattingBubble):
                self.root.remove_widget(widget)
                return


BubbleApp().run()
