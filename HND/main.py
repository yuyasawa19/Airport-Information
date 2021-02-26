import os
from datetime import datetime
from random import sample
from string import ascii_lowercase

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.text import DEFAULT_FONT, LabelBase
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

from observer import Observer

os.environ["KIVY_AUDIO"] = "sdl2"

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'piragino_w6.ttc')

sound = SoundLoader.load('./sound/chime_itm.wav')

kv = """
<AirDataInfo>:
    id: ad
    id: lbl
    bright: 0
    scheduled_time: ''
    estimated_time: ''
    image_path: ''
    flight_no: ''
    district: ''
    status: ''
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
        Label:
            size_hint_x: 1.3/22
            text: root.scheduled_time
        Label:
            size_hint_x: 1.3/22
            text: root.estimated_time
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
            id: label
            size_hint_x: 2/22
            text: root.district
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 1.5/22
            text: root.gate
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            id: label
            size_hint_x: 4.4/22
            text: root.status
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            color: root.state_rgb_r, root.state_rgb_g, root.state_rgb_b, 1
<FlightBoard>:
    orientation: 'vertical'
    rv: rv
    label: label
    ActionBar:
        ActionView:
            ActionPrevious:
                title: '羽田空港　フライト情報'
                with_previous: False
            ActionButton:
                text: '出発/到着 切り替え'
                on_press: root.change_flight_type()
    BoxLayout:
        size_hint_y: 1.5/12
        orientation: 'horizontal'
        canvas:
            Color:
                rgba: 0.05, 0.05, 0.05, 1
            Rectangle:
                size: self.size
                pos: self.pos
        Image:
            size_hint_x: 2/16
            source: root.pict_icon_path
        Label:
            size_hint_x: 4/16
            text: root.info_kind_ja
            text_size: self.size
            font_size: 40
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 4/16
            text: root.info_kind_en
            text_size: self.size
            font_size: 24
            halign: 'left'
            valign: 'middle'
        BoxLayout:
            size_hint_x: 4/16
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    size_hint_x: 3/4
                    text: '第１ターミナル便'
                    text_size: self.size
                    halign: 'right'
                    valign: 'middle'
                CheckBox:
                    size_hint_x: 1/4
                    id: t1
                    active: root.t1
                    on_press: root.check_terminal('t1')
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    size_hint_x: 3/4
                    text: '第２ターミナル便'
                    text_size: self.size
                    halign: 'right'
                    valign: 'middle'
                CheckBox:
                    size_hint_x: 1/4
                    id: t2
                    active: root.t2
                    on_press: root.check_terminal('t2')
        BoxLayout:
            size_hint_x: 2/16
            orientation: 'vertical'
            Label:
                size_hint_y: 2/4
                text: '只今の時刻'
                #text_size: self.size
                valign: 'bottom'
            Label:
                id: label
                size_hint_y: 2/4
                font_size: 24
                text: root.now_time
                color: 255/255, 204/255, 0/255, 1
    BoxLayout:
        size_hint_y: 1/12
        orientation: 'horizontal'
        canvas:
            Color:
                rgba: 0.05, 0.05, 0.05, 1
            Rectangle:
                size: self.size
                pos: self.pos
            #Line:
            #    rectangle: self.x+1, self.y+1, self.width-1, self.height-1
            #    #dash_offset: 5
            #    #dash_length: 3
        Label:
            size_hint_x: 1.3/22
            text: root.info_string[0]
        Label:
            size_hint_x: 1.3/22
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
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 2/22
            text_size: self.size
            text: root.info_string[4]
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 1.5/22
            text: root.info_string[6]
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 4.4/22
            text: root.info_string[5]
            text_size: self.size
            halign: 'left'
            valign: 'middle'
    Label:
        size_hint_y: 0.1/12
        canvas:
            Color:
                rgba: root.rgba_line[0], root.rgba_line[1], root.rgba_line[2], root.rgba_line[3]
            Rectangle:
                size: self.size
                pos: self.pos
    RecycleView:
        size_hint_y: 9/12
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: sp(60)
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

    language = StringProperty()
    info_kind_ja = StringProperty()
    info_kind_en = StringProperty()
    now_time = StringProperty()
    pict_icon_path = StringProperty()
    info_string = ListProperty([])
    rgba_line = ListProperty([])
    t1 = BooleanProperty()
    t2 = BooleanProperty()

    def __init__(self, **kwargs):
        self.language = "ja"
        self.info_kind_ja = "国内線　出発"
        self.info_kind_en = "Domestic Departure"
        self.t1 = self.t2 = True
        self.info_string = ["定刻", "変更", "航空会社",  "便名", "行先", "備考", "ゲート"]
        self.flight_type = "dd"
        self.pict_icon_path = "./image/icon/icon_departure.png"
        self.rgba_line = [0, 224/255, 151/255, 1]
        super(FlightBoard, self).__init__(**kwargs)
        self.flight_list = []
        self.ob = Observer()
        self.ob.load_all_flight(flight_type=self.flight_type)
        self.set_airdata()
        self.blinker = True
        Clock.schedule_interval(self.switch_language, 15)
        Clock.schedule_interval(self.renew_airdata, 10)
        Clock.schedule_interval(self.measure_time, 0.5)
    

    def set_airdata(self):
        self.rv.data = []
        after_flight_list = self.ob.get_after_flight(flight_type=self.flight_type, t1=self.t1, t2=self.t2)
        if len(self.flight_list) == 0:
            reduce_flight_num = 0
        else:
            reduce_flight_num = len(self.flight_list) - len(after_flight_list)
        anim = Animation(opacity=0, duration=0.2) + Animation(opacity=1, duration=0.2)
        if reduce_flight_num != 0:
            anim.start(self.rv)
        self.flight_list = after_flight_list

        for i, flight in enumerate(self.flight_list):
            bright = 16/255 if i % 2 else 24/255
            image_path = "image/logo/{0}_b.png".format(flight.airline_code)
            flight_no = str(int(flight.flight_no))
            scheduled_time = flight.scheduled_time.split()[1][:-3]
            estimated_time = flight.estimated_time.split()[1][:-3] if flight.estimated_time != "" else ""
            # Language option
            if self.language == "ja":
                district = flight.district_jp
                status = flight.remarks["ja"]
            else:
                district = flight.district_en
                status = flight.remarks["en"]
            # Status string color and gate option
            if flight.remarks["ja"] == "欠航":
                gate = ""
                state_rgb_r, state_rgb_g, state_rgb_b = 255/255, 102/255, 0/255
            else:
                gate = flight.gate_jp.lstrip("0")
                state_rgb_r, state_rgb_g, state_rgb_b = 255/255, 255/255, 255/255
            
            self.rv.data.append(
                {
                    "image_path": image_path, "flight_no": flight_no, "district": district,
                    "scheduled_time": scheduled_time, "estimated_time": estimated_time,
                    "status": status, "gate": gate, "bright": bright,
                    "state_rgb_r": state_rgb_r, "state_rgb_g": state_rgb_g, "state_rgb_b": state_rgb_b
                }
            )


    def renew_airdata(self, dt):
        self.ob.load_all_flight(flight_type=self.flight_type)
        self.set_airdata()


    def change_flight_type(self):
        if self.flight_type[1] == "d":
            self.flight_type = "da"
            self.pict_icon_path = "./image/icon/icon_arrival.png"
            self.info_kind_ja = "国内線　到着"
            self.info_kind_en = "Domestic Arrival"
            if self.language == "ja":
                self.info_string = ["定刻", "変更", "航空会社", "便名", "出発地", "備考", "ゲート"]
            else:
                self.info_string = ["Scheduled", "Estimated", "Airline", "Flight", "Origin", "Remarks", "Gate"]
            self.rgba_line = [249/255, 222/255, 81/255, 1]
        elif self.flight_type[1] == "a":
            self.flight_type = "dd"
            self.pict_icon_path = "./image/icon/icon_departure.png"
            self.info_kind_ja = "国内線　出発"
            self.info_kind_en = "Domestic Departure"
            if self.language == "ja":
                self.info_string = ["定刻", "変更", "航空会社", "便名", "行先", "備考", "ゲート"]
            else:
                self.info_string = ["Scheduled", "Estimated", "Airline", "Flight", "Destination", "Remarks", "Gate"]
            self.rgba_line = [0, 224/255, 151/255, 1]
        self.flight_list = []
        self.ob.load_all_flight(flight_type=self.flight_type)
        self.set_airdata()
    

    def check_terminal(self, show_terminal):
        if show_terminal == "t1":
            self.t1 = not self.t1
        elif show_terminal == "t2":
            self.t2 = not self.t2
        self.flight_list = []
        self.set_airdata()

    
    def switch_language(self, dt):
        if self.language == "ja":
            self.language = "en"
            if self.flight_type[1] == "d":
                self.info_string = ["Scheduled", "Estimated", "Airline", "Flight", "Destination", "Remarks", "Gate"]
            elif self.flight_type[1] == "a":
                self.info_string = ["Scheduled", "Estimated", "Airline", "Flight", "Origin", "Remarks", "Gate"]
        else:
            self.language = "ja"
            if self.flight_type[1] == "d":
                self.info_string = ["定刻", "変更", "航空会社", "便名", "行先", "備考", "ゲート"]
            elif self.flight_type[1] == "a":
                self.info_string = ["定刻", "変更", "航空会社", "便名", "出発地", "備考", "ゲート"]
        #anim = Animation(opacity=0, duration=0.2) + Animation(opacity=1, duration=0.2)
        #anim.start(self.rv)
        self.set_airdata()

    
    def measure_time(self, dt):
        nowtime = datetime.now()
        hour = str(nowtime.hour).zfill(2)
        minute = str(nowtime.minute).zfill(2)
        colon = "：" if nowtime.second % 2 == 0 else "　"
        #colon = "：" if self.blinker == True else "　"
        self.now_time = "{0}{1}{2}".format(hour, colon, minute)
        #self.blinker = not self.blinker


class AirDataInfo(BoxLayout):

    def get_data_index(self):
        return self.parent.get_view_index_at(self.center)


class FlightBoardApp(App):

    def build(self):
        return FlightBoard()


if __name__ == '__main__':
    FlightBoardApp().run()
