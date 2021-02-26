import os
os.environ["KIVY_AUDIO"] = "sdl2"

from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ListProperty, BooleanProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

from observer import Observer

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'piragino_w6.ttc')

sound = SoundLoader.load('./sound/chime_itm.wav')

kv = """
<AirDataInfo>:
    bright: 0
    icon_path: ''
    image: ''
    scheduled: ''
    estimated: ''
    image_path: ''
    flight_no: ''
    district_jp: ''
    district_en: ''
    state_jp: ''
    state_en: ''
    state_rgb_r: 1
    state_rgb_g: 1
    state_rgb_b: 1
    gate: ''
    canvas:
        Color:
            rgba: root.bright, root.bright, root.bright, 1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        orientation: 'horizontal'
        color: 1, 1, 1, 1
        Image:
            size_hint_x: 1/22
            source: root.icon_path
        Label:
            size_hint_x: 1.5/22
            text: root.scheduled
        Label:
            size_hint_x: 1.5/22
            text: root.estimated
            color: 255/255, 204/255, 0/255, 1
        Image:
            size_hint_x: 2/22
            source: root.image_path
        Label:
            size_hint_x: 1.5/22
            text: root.flight_no
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 2/22
            text: root.district_jp
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 3/22
            text: root.district_en
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 4/22
            text: root.state_jp
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            color: root.state_rgb_r, root.state_rgb_g, root.state_rgb_b, 1
        Label:
            size_hint_x: 4/22
            text: root.state_en
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            color: root.state_rgb_r, root.state_rgb_g, root.state_rgb_b, 1
        Label:
            size_hint_x: 1.5/22
            text: root.gate
<FlightBoard>:
    orientation: 'vertical'
    rv: rv
    ActionBar:
        ActionView:
            ActionPrevious:
                title: root.flight_type
                with_previous: False
                icon: './image/logo/logo_IT.jpg'
            ActionButton:
                text: '切り替え'
                on_press: root.change_flight_type()
    BoxLayout:
        size_hint_y: 1/10
        orientation: 'horizontal'
        canvas:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            size_hint_x: 2.5/22
            text: root.info_string[0]
        Label:
            size_hint_x: 1.5/22
            text: root.info_string[1]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 2/22
            text: root.info_string[2]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 1.5/22
            text: root.info_string[3]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 5/22
            text: root.info_string[4]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 8/22
            text: root.info_string[5]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 1.5/22
            text: root.info_string[6]
    RecycleView:
        size_hint_y: 9/10
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: sp(60) #スクロール速度
        bar_width: sp(20)
        viewclass: 'AirDataInfo'
        RecycleBoxLayout:
            default_size: None, sp(50)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
"""

Builder.load_string(kv)



class FlightBoard(BoxLayout):

    #info_kind = StringProperty()
    #info_string = ListProperty([])
    blinker = BooleanProperty()

    def __init__(self, **kwargs):
        self.info_string = ['定刻', '変更', '航空会社', '便名', '行先', '備考', 'ゲート']
        self.flight_type = 'dep'
        self.black_color_1 = 16
        self.black_color_2 = 24
        self.info_color = (255/255, 204/255, 0/255)
        self.warning_color = (255/255, 102/255, 0/255)
        self.blinker = True
        super(FlightBoard, self).__init__(**kwargs)
        self.rv.data = []
        self.set_airdata()

        Clock.schedule_interval(self.blink, 1)
        Clock.schedule_interval(self.renew_airdata, 10)
    

    def set_airdata(self):
        self.rv.data = []
        for i, airdata in enumerate(Observer().get_after_flight(self.flight_type)):
            black_color = self.black_color_1 if i % 2 else self.black_color_2
            airdata["bright"] = black_color / 255
            """
            if airdata["is_attention"] == True:
                airdata["icon_path"] = './image/icon/attention_{0}.png'.format(black_color)
            else:
                airdata["icon_path"] = './image/icon/black_{0}.png'.format(black_color)
            """

            # Blinker option
            if self.blinker == True and airdata["is_attention"] == True:
                airdata["icon_path"] = './image/icon/attention_{0}.png'.format(black_color)
            else:
                airdata["icon_path"] = './image/icon/black_{0}.png'.format(black_color)

            airdata["estimated"] = "" if airdata["estimated"] == "---" else airdata["estimated"]
            airdata["gate"] = "" if airdata["gate"] == "---" else airdata["gate"]
            airdata["image_path"] = './image/logo/logo_{0}_{1}.png'.format(airdata["airline"], black_color)
            airdata["state_rgb_r"] = str(self.warning_color[0]) if airdata["state_en"] == "Cancelled" else str(1.0)
            airdata["state_rgb_g"] = str(self.warning_color[1]) if airdata["state_en"] == "Cancelled" else str(1.0)
            airdata["state_rgb_b"] = str(self.warning_color[2]) if airdata["state_en"] == "Cancelled" else str(1.0)
            self.rv.data.append(airdata)

    
    def change_flight_type(self):
        if self.flight_type == "dep":
            self.flight_type = "arr"
        else:
            self.flight_type = "dep"
        print("Set mode to {0}".format(self.flight_type))
        self.set_airdata()
        print("Set airdata is done.")


    def renew_airdata(self, dt):
        self.set_airdata()
        print("Renewed.")


    def blink(self, dt):
        if self.blinker == True:
            self.blinker = False
        else:
            self.blinker = True
        self.set_airdata()



class AirDataInfo(BoxLayout):
    pass



class FlightBoardApp(App):
    def build(self):
        return FlightBoard()



if __name__ == '__main__':
    FlightBoardApp().run()
