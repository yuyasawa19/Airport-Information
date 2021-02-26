from jsonstream import Jsonstream

class Observer:


    def __init__(self):
        self.js = Jsonstream()
        self.flight_list = []
        self.prev_flight_list = []
        self.attention_list = []
        self.dep_or_arr = "D"
        try:
            self.flight_list = self.js.get_today_airdata_list(self.dep_or_arr)
        except:
            pass
    

    def renew_list(self):
        self.prev_flight_list = self.flight_list
        try:
            self.flight_list = self.js.get_today_airdata_list(self.dep_or_arr)
        except:
            pass

    
    def reset_airdata(self, kind):
        self.flight_list = self.js.get_today_airdata_list(kind)