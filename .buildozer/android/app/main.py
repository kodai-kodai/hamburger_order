from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.graphics import Color, Rectangle
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.uix.widget import Widget
import os


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # build() で作成したルートを Screen に追加して表示させる
        root = self.build()
        self.add_widget(root)
        
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
        # 端末幅に応じて 1 列 or 2 列に切り替え（スマホは 1 列推奨）
        cols = 2 if Window.width > dp(600) else 1
        grid = GridLayout(cols=cols, spacing=dp(8), padding=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        # 追加
        
        img_dir = os.path.join(os.path.dirname(__file__), "img")
        
        # スクロールの一番上に画像を追加
        # スクロールの一番上に画像を追加（画面高さの割合で指定）
        top_img = Image(
            source=os.path.join(img_dir, "top.png"),
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=None,
            height=Window.height * 0.30  # 必要に応じて 0.25-0.4 を調整
        )



        menus = [
            ("barbecue.png", "テリヤキ", 480),
            ("classicbeef.png", "クラシックビーフ", 520),
            ("spicychicken.png", "スパイシーチキン", 500),
            ("vegetarian.png", "ベジタリアン", 460),
            ("hotdog.png", "ホットドッグ", 400),
            ("nugget.png", "ナゲット", 300),
            ("poteto.png", "ポテト", 250),
            ("coffee.png", "コーヒー", 200),
        ]
        self.selected_items = {}  # 商品名: {"qty": 数量, "price": 単価, "img": 画像パス}
        

        # メニューアイテム生成
        for img_name, label_text, price in menus:
            img_path = os.path.join(img_dir, img_name)
            item = self.create_menu_item(img_path, label_text, price)
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

    def create_menu_item(self, img_path, text, price):
        """画像とラベルをまとめたメニューカード"""
        item_layout = BoxLayout(
            orientation="vertical",
            padding=8,
            spacing=10, 
            size_hint_y=None,
            height=dp(320)
        )

        # 画像（枠内でサイズ調整）
        img = Image(
            source=img_path,
            size_hint_y=None,
            height=dp(140),
            fit_mode="contain",
            allow_stretch=True,
            pos_hint={"center_x": 0.5, "center_y": 0.2},
        )


        label = Label(
            text=f"{text}\n¥{price}",
            font_size="24sp",                # 必要に応じて調整
            halign="center",
            valign="middle",
            size_hint_y=None,                # 高さを明示してクリッピングを防ぐ
            height=dp(48),
            color=(0, 0, 0, 1),
        )
        # 幅に合わせて改行させ、高さは自分で決める（None を渡すと縦方向は自動）
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        spacer = Widget(size_hint_y=1)
        
        # サイズ選択が必要なメニュー名一覧
        size_items = ("コーヒー", "ナゲット", "ポテト")
        size_spinner = None
        size_widget = None
        if text in size_items:
            options = ["S ¥-50", "M", "L ¥+50"]
            default = "M"

            size_layout = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(44))
            size_label = Label(text="サイズ:", font_size="16sp", size_hint_x=0.45, color=(0,0,0,1), halign="left", size_hint_y=None, height=dp(44))
            size_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            size_spinner = Spinner(text=default, values=options, size_hint=(None, None), size=(dp(88), dp(44)), font_size="16sp")
            size_layout.add_widget(size_label)
            size_layout.add_widget(size_spinner)
            size_widget = size_layout

        # 数量ボタンは高さを確保（タッチしやすく）
        qty_layout = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(52))
        minus_btn = Button(text="-", font_size="20sp", size_hint=(0.2, None), height=dp(48))
        qty_label = Label(text="0", font_size="18sp", size_hint=(0.2, None), height=dp(48), color=(0,0,0,1))
        plus_btn = Button(text="+", font_size="20sp", size_hint=(0.2, None), height=dp(48))

        def calc_price_by_size(base_price, size_text):
            # Spinner の値が "S ¥-50" のような形式でも先頭の S/M/L を使う
            if not size_text:
                size_key = "M"
            else:
                size_key = str(size_text).split()[0]  # "S ¥-50" -> "S"
            if size_key == "S":
                return max(0, base_price - 50)
            if size_key == "L":
                return base_price + 50
            return base_price

        def update_selected_item(size_text, new_qty):
            # size_text には "S ¥-50" などが入る可能性を想定して正規化
            size_key = str(size_text).split()[0] if size_text else "M"
            # new_qty が 0 ならエントリを削除
            if new_qty <= 0:
                if text in self.selected_items:
                    del self.selected_items[text]
                return
            adj_price = calc_price_by_size(price, size_key)
            self.selected_items[text] = {"qty": new_qty, "price": adj_price, "img": img_path, "size": size_key}

        def update_qty(delta):
            current = int(qty_label.text)
            new_qty = max(0, current + delta)
            qty_label.text = str(new_qty)
            # サイズが選べる場合は spinner の選択を使う、なければ base price
            size_text = size_spinner.text if size_spinner else None
            update_selected_item(size_text if size_text else "M", new_qty)  # デフォルト M

        plus_btn.bind(on_press=lambda x: update_qty(+1))
        minus_btn.bind(on_press=lambda x: update_qty(-1))

        # サイズを変更したとき、既に数量があるなら選択価格を更新
        if size_spinner:
            def on_size_change(inst, val):
                current_qty = int(qty_label.text)
                if current_qty > 0:
                    update_selected_item(val, current_qty)
            size_spinner.bind(text=on_size_change)

        qty_layout.add_widget(minus_btn)
        qty_layout.add_widget(qty_label)
        qty_layout.add_widget(plus_btn)

        item_layout.add_widget(img)
        item_layout.add_widget(label)
        if size_widget:
            item_layout.add_widget(size_widget)
        item_layout.add_widget(spacer)
        item_layout.add_widget(qty_layout)

        return item_layout
    def go_to_order(self, instance):
        order_screen = self.manager.get_screen('order')
        order_screen.display_order(self.selected_items)
        self.manager.current = 'order'

# ===== 注文確認画面 =====
class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
        
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
            self.layout.bind(pos=lambda instance, value: setattr(bg, 'pos', value))
            self.layout.bind(size=lambda instance, value: setattr(bg, 'size', value))

        # タイトル（高さ固定）
        self.title = Label(
            text="注文内容確認",
            font_size="20sp",
            size_hint=(1, None),
            height=dp(56),
            halign="center",
            valign="middle",
            color=(0,0,0,1),
        )
        self.title.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.layout.add_widget(self.title)

        # 注文リスト（スクロール）
        self.scroll = ScrollView(size_hint=(1, 1))
        self.order_list = GridLayout(cols=1, spacing=dp(8), size_hint_y=None, padding=(0, dp(4)))
        self.order_list.bind(minimum_height=self.order_list.setter('height'))
        self.scroll.add_widget(self.order_list)
        self.layout.add_widget(self.scroll)

        # 合計＋ボタン領域（下部、固定高さ）
        button_box = BoxLayout(size_hint=(1, None), height=dp(72), spacing=dp(8))
        self.back_button = Button(text="← 追加注文する", font_size="18sp", background_color=(0.6,0.6,0.6,1))
        self.pay_button = Button(text="会計する", font_size="18sp", background_color=(0.2,0.6,0.2,1))

        self.back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.pay_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'complete'))

        button_box.add_widget(self.back_button)
        button_box.add_widget(self.pay_button)
        self.layout.add_widget(button_box)

        self.add_widget(self.layout)

    def display_order(self, selected_items):
        self.order_list.clear_widgets()
        total_price = 0

        for name, info in selected_items.items():
            if info["qty"] > 0:
                subtotal = info["qty"] * info["price"]
                total_price += subtotal

                # 行は横並び、アイテム画像は固定幅、テキストは折り返し
                item_box = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(88))
                img = Image(source=info["img"], size_hint=(None, None), size=(dp(72), dp(72)), allow_stretch=True, keep_ratio=True)
                text_label = Label(
                    text=f"{name}\n数量: {info['qty']}　小計: ¥{subtotal}",
                    font_size="16sp",
                    halign="left",
                    valign="middle",
                    size_hint=(1, 1),
                    color=(0,0,0,1),
                )
                text_label.bind(size=lambda i, v: setattr(i, 'text_size', (i.width, None)))

                item_box.add_widget(img)
                item_box.add_widget(text_label)
                self.order_list.add_widget(item_box)

        # 合計表示 or 空の場合メッセージ
        if total_price == 0:
            self.order_list.add_widget(Label(text="注文がありません。", font_size="16sp", size_hint_y=None, height=dp(48), halign="center",color=(0,0,0,1),))
        else:
            total_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(64), padding=(0, dp(6)))
            total_label = Label(
                text=f"合計金額: ¥{total_price}",
                font_size="20sp",
                halign="center",
                valign="middle",
                size_hint=(1,1),
                color=(0,0,0,1),
            )
            total_label.bind(size=lambda i, v: setattr(i, 'text_size', v))
            total_box.add_widget(total_label)
            self.order_list.add_widget(total_box)

# ===== 会計完了画面 =====
class CompleteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        
        # 白背景（メニュー画面と同様）
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            bg = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=lambda instance, value: setattr(bg, 'pos', value))
            layout.bind(size=lambda instance, value: setattr(bg, 'size', value))

        layout.add_widget(Label(
            text="ご注文ありがとうございました！",
            font_size="22sp",
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(64),
            color=(0,0,0,1),
        ))
        layout.add_widget(Label(
            text="お会計が完了しました。",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(48),
            color=(0,0,0,1),
        ))

        # 中央に余白を入れてボタンを下部に寄せる
        layout.add_widget(Widget(size_hint_y=1))

        back_btn = Button(
            text="メニューに戻る",
            font_size="18sp",
            size_hint=(1, None),
            height=dp(56),
            background_color=(0.2,0.6,0.9,1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)

        self.add_widget(layout)


# ===== アプリ起動 =====
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(OrderScreen(name='order'))
        sm.add_widget(CompleteScreen(name='complete'))
        return sm
    
if __name__ == "__main__":
    MyApp().run()