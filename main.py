from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.graphics import Color, Rectangle
import os


class MyApp(App):
    def build(self):
        # ===== フォント設定 =====
        font_path = os.path.join(os.path.dirname(__file__), "font", "NotoSansJP-ExtraBold.ttf")
        resource_add_path(os.path.dirname(font_path))
        LabelBase.register(DEFAULT_FONT, font_path)

        # ===== メインレイアウト =====
        root_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        with root_layout.canvas.before:

            Color(1, 1, 1, 1)  # 白色
            root_bg = Rectangle(pos=root_layout.pos, size=root_layout.size)
            # サイズ・位置が変わった時に背景も追従
            root_layout.bind(pos=lambda instance, value: setattr(root_bg, 'pos', value))
            root_layout.bind(size=lambda instance, value: setattr(root_bg, 'size', value))

        scroll_content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=20, padding=10)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        # タイトルラベル（文字重なり防止: text_size指定）
        title = Label(
            text=" ハンバーガーメニュー ",
            font_size="28sp",
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
            color=(0,0,0,1),
        )
        # text_sizeをウィジェットサイズに合わせる
        title.bind(size=lambda instance, value: setattr(instance, 'text_size', value))

        # ===== メニュー一覧 =====
        scroll = ScrollView(size_hint=(1, 0.8))
        grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        img_dir = os.path.join(os.path.dirname(__file__), "img")
        
        # スクロールの一番上に画像を追加
        top_img = Image(source='./img/top.png', allow_stretch=True, keep_ratio=True, size_hint_y=None, height=500)



        menus = [
            ("barbecue.png", "テリヤキ"),
            ("classicbeef.png", "クラシックビーフ"),
            ("spicychicken.png", "スパイシーチキン"),
            ("vegetarian.png", "ベジタリアン"),
            ("hotdog.png", "ホットドッグ"),
            ("nugget.png", "ナゲット"),
            ("poteto.png", "ポテト"),
            ("coffee.png", "コーヒー"),
        ]

        # メニューアイテム生成
        for img_name, label_text in menus:
            item = self.create_menu_item(os.path.join(img_dir, img_name), label_text)
            grid.add_widget(item)


        scroll_content.add_widget(top_img)
        scroll_content.add_widget(grid)
        scroll.add_widget(scroll_content)
        root_layout.add_widget(title)
        root_layout.add_widget(scroll)

        # ===== 下部のボタン =====
        order_button = Button(
            text="注文画面へ進む",
            font_size="20sp",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        order_button.bind(on_press=self.go_to_order)

        root_layout.add_widget(order_button)

        return root_layout

    def create_menu_item(self, img_path, text):
        """画像とラベルをまとめたメニューカード"""
        item_layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=20,
            size_hint_y=None,
            height=Window.height * 0.8
        )

        # 画像（枠内でサイズ調整）
        img = Image(
            source=img_path,
            size_hint_y=0.5, 
            fit_mode="contain",
            pos_hint={"center_x": 0.5},
        )


        label = Label(
            text=text,
            font_size="30sp",
            halign="center",
            valign="middle",
            size_hint_y=0.3,
            color=(0, 0, 0, 1),
        )
        
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        
        qty_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=60)
        minus_btn = Button(text="-", font_size="20sp", size_hint_x=0.2)
        qty_label = Label(text="0", font_size="20sp", size_hint_x=0.2, color=(0,0,0,1))
        plus_btn = Button(text="+", font_size="20sp", size_hint_x=0.2)


        plus_btn.bind(on_press=lambda x: qty_label.setter('text')(qty_label, str(int(qty_label.text) + 1)))
        minus_btn.bind(on_press=lambda x: qty_label.setter('text')(qty_label, str(max(0, int(qty_label.text) - 1))))
        
        qty_layout.add_widget(minus_btn)
        qty_layout.add_widget(qty_label)
        qty_layout.add_widget(plus_btn)

        item_layout.add_widget(img)
        item_layout.add_widget(label)
        item_layout.add_widget(qty_layout)

        return item_layout

    def go_to_order(self, instance):
        print("注文画面に進みます！")


if __name__ == "__main__":
    MyApp().run()