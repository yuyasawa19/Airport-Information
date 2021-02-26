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
from kivy.animation import Animation

from observer import Observer

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'piragino_w6.ttc')

sound = SoundLoader.load('./sound/chime.wav')

kv = """
<AirDataInfo>:
    r: 0
    g: 0
    b: 0
    icon: ''
    image: ''
    flight_no: ''
    district: ''
    scheduled_time: ''
    estimated_time: ''
    status: ''
    gate: ''
    canvas:
        Color:
            rgba: root.r, root.g, root.b, 1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        orientation: 'horizontal'
        color: 1, 1, 1, 1
        Image:
            source: root.icon
            size_hint_x: 1/17
        Image:
            size_hint_x: 2/17
            source: root.image
        Label:
            size_hint_x: 2/17
            text: root.flight_no
        Label:
            size_hint_x: 4/17
            text: root.district
        Label:
            size_hint_x: 2/17
            text: root.scheduled_time
        Label:
            size_hint_x: 2/17
            text: root.estimated_time
        Label:
            size_hint_x: 4/17
            text: root.status
        Label:
            size_hint_x: 2/17
            text: root.gate
<FlightBoard>:
    orientation: 'vertical'
    rv: rv
    ActionBar:
        ActionView:
            ActionPrevious:
                title: root.info_kind
                with_previous: False # trueだと頭のロゴがボタンになる？
                icon: './image/logo/logo_IT.jpg'
            ActionButton:
                text: '切り替え'
                on_press: root.change()

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
            size_hint_x: 1/17
        Label:
            size_hint_x: 4/17
            text: root.info_string[0]
        Label:
            size_hint_x: 4/17
            text: root.info_string[1]
        Label:
            size_hint_x: 2/17
            text: root.info_string[2]
        Label:
            size_hint_x: 2/17
            text: root.info_string[3]
        Label:
            size_hint_x: 4/17
            text: root.info_string[4]
        Label:
            size_hint_x: 2/17
            text: root.info_string[5]
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

    language = StringProperty()
    info_kind = StringProperty()
    info_string = ListProperty([])
    blinker = BooleanProperty()

    def __init__(self, **kwargs):
        self.info_string = ['便名', '行先', '定刻', '変更', '備考', '搭乗口']
        self.info_kind = '国内線　出発'
        self.language = 'jp'
        self.blinker = True
        super(FlightBoard, self).__init__(**kwargs)
        self.ob = Observer()
        self.ob.renew_list()
        self.rv.data = []
        self.set_airdata()
        self.renew_count = 0
        Clock.schedule_interval(self.change_jp2en, 10)
        Clock.schedule_interval(self.blink, 1)
        Clock.schedule_interval(self.renew_airdata, 10)
    

    def set_airdata(self):
        self.rv.data = []
        count = 0

        for airdata in self.ob.flight_list:

            if count % 2 == 0:
                rgb_r = 0
                rgb_g = 0
                rgb_b = 180/255
            else:
                rgb_r = 0
                rgb_g = 100/255
                rgb_b = 255/255
            
            if airdata.status_jp in ['搭乗最終','降機中']:
                if self.blinker == True:
                    icon_name = './image/icon/hibiscus.png'
                else:
                    if rgb_g == 0:
                        icon_name = './image/icon/blue.png'
                    else:
                        icon_name = './image/icon/cyan.png'
            elif airdata.status_jp in ['搭乗中','手荷物受取中']:
                icon_name = './image/icon/hibiscus.png'
            else:
                if rgb_g == 0:
                    icon_name = './image/icon/blue.png'
                else:
                    icon_name = './image/icon/cyan.png'
            
            image_name = './image/logo/logo_' + airdata.code + '.jpg'

            flight_no = str(airdata.flight_no)

            if self.language == 'jp':
                district = airdata.district_jp
            else:
                district = airdata.district_en
            
            tmp_str = airdata.scheduled_time
            scheduled_time = tmp_str[8] + tmp_str[9] + ':' + tmp_str[10] + tmp_str[11]

            if airdata.estimated_time != '':
                tmp_str = airdata.estimated_time
                estimated_time = tmp_str[8] + tmp_str[9] + ':' + tmp_str[10] + tmp_str[11]
            else:
                estimated_time = ''
            
            if self.language == 'jp':
                status = airdata.status_jp
            else:
                status = airdata.status_en
            
            gate = airdata.gate

            self.rv.data.append({'r':rgb_r, 'g':rgb_g, 'b':rgb_b, 'icon': icon_name, 'image':image_name,
                'flight_no':flight_no, 'district': district, 'scheduled_time':scheduled_time,
                'estimated_time':estimated_time, 'status':status, 'gate':gate})
            count += 1


    def set_info_status(self):
        if self.ob.dep_or_arr == 'D':
            if self.language == 'jp':                
                self.info_string = ['便名', '行先', '定刻', '変更', '備考', '搭乗口']
                self.info_kind = '国内線　出発'
            else:
                self.info_string = ['Flight', 'Destination', 'Scheduled', 'Estimated', 'Remarks', 'Gate']
                self.info_kind = 'Domestic Departures'
        else:
            if self.language == 'jp':
                self.info_string = ['便名', '出発地', '定刻', '変更', '備考', '出口']
                self.info_kind = '国内線　到着'
            else:
                self.info_string = ['Flight', 'Origin', 'Scheduled', 'Estimated', 'Remarks', 'Exit']
                self.info_kind = 'Domestic Arrivals'
        #self.set_airdata()


        
    def change_jp2en(self, dt):
        '''
        if self.ob.dep_or_arr == 'D':
            if self.language == 'jp':
                self.language = 'en'
                self.info_string = ['Flight', 'Destination', 'Scheduled', 'Estimated', 'Remarks', 'Gate']
                self.info_kind = 'Domestic Departures'
            else:
                self.language = 'jp'
                self.info_string = ['便名', '行先', '定刻', '変更', '備考', '搭乗口']
                self.info_kind = '国内線　出発'
            self.set_airdata()
        else:
            if self.language == 'jp':
                self.language = 'en'
                self.info_string = ['Flight', 'Origin', 'Scheduled', 'Estimated', 'Remarks', 'Exit']
                self.info_kind = 'Domestic Arrivals'
            else:
                self.language = 'jp'
                self.info_string = ['便名', '出発地', '定刻', '変更', '備考', '出口']
                self.info_kind = '国内線　到着'
            self.set_airdata()
        '''
        if self.language == 'jp':
            self.language = 'en'
        else:
            self.language = 'jp'
        self.set_info_status()
        self.set_airdata()

    
    def renew_airdata(self, dt):
        self.ob.renew_list()


    def blink(self, dt):
        if self.blinker == True:
            self.blinker = False
        else:
            self.blinker = True
        self.set_airdata()


    def change(self):
        if self.ob.dep_or_arr == 'D':
            self.ob.dep_or_arr = 'A'
        else:
            self.ob.dep_or_arr = 'D'
        self.ob.reset_airdata(self.ob.dep_or_arr)
        self.set_airdata()
        self.set_info_status()



class AirDataInfo(BoxLayout):
    pass



class FlightBoardApp(App):
    def build(self):
        return FlightBoard()



if __name__ == '__main__':
    FlightBoardApp().run()