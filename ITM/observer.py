from datetime import datetime, timedelta
from html_stream import HTMLstream


class Observer:

    def __init__(self):
        self.flight_list = []


    def get_all_flight(self, flight_type):
        return HTMLstream().get_all_flights(flight_type)
    
    
    def get_after_flight(self, flight_type):
        now_time = datetime.now()
        if flight_type == "dep":
            start_time = now_time + timedelta(minutes=-10)
        else:
            start_time = now_time + timedelta(minutes=-30)
        start_time_min = int(start_time.strftime("%H%M"))
        
        after_flight = []
        for flight in HTMLstream().get_all_flights(flight_type):
            if flight["estimated"] == "---":
                older = int(flight["scheduled"].replace(":",""))
            else:
                scheduled_int = int(flight["scheduled"].replace(":",""))
                estimated_int = int(flight["estimated"].replace(":",""))
                older = max(scheduled_int, estimated_int)
            
            if flight["state_en"] == "Now Boarding":
                flight["is_attention"] = True
            elif flight["state_en"] == "Proceed To Gate" and older - start_time_min <= 30:
                flight["is_attention"] = True
            else:
                flight["is_attention"] = False
 
            if older > start_time_min:
                after_flight.append(flight)
        
        return after_flight


if __name__ == "__main__":
    flight_type = "dep"
    for i, flight in enumerate(Observer().get_after_flight(flight_type)):
        print(i, flight)
