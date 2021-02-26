from datetime import datetime, timedelta

from jsonstream import Jsonstream


class Observer:

    def __init__(self):
        self.flight_list = []


    def sort_codeshare_sametime(self, sametime_flights):
        dict_sametime = {}
        sorted_sametime = []

        for flight in sametime_flights:
            if flight.gate_jp not in dict_sametime:
                dict_sametime[flight.gate_jp] = [(flight.airline_code, flight)]
            else:
                dict_sametime[flight.gate_jp].append((flight.airline_code, flight))
        
        for gate, ftp_list in dict_sametime.items():
            if gate == "":
                for ftp in ftp_list:
                    sorted_sametime.append(ftp[1])
            else:
                if len(ftp_list) == 2:  # There is a codeshare flight
                    if ftp_list[0][0] == "ANA":
                        sorted_sametime.append(ftp_list[1][1])
                        sorted_sametime.append(ftp_list[0][1])
                    else:
                        sorted_sametime.append(ftp_list[0][1])
                        sorted_sametime.append(ftp_list[1][1])
                elif len(ftp_list) == 1:
                    sorted_sametime.append(ftp_list[0][1])
                else:
                    print("Exception: len(ftp_list) is invalid.")
        
        if len(sametime_flights) != len(sorted_sametime):
            print(False, dict_sametime)

        return sorted_sametime

    
    def sort_codeshare(self):
        sorted_flight_list = []
        sametime_flights = []

        for i, flight in enumerate(self.flight_list):
            if i == 0:  # First flight
                time = flight.scheduled_time
                sametime_flights.append(flight)
            else:
                if flight.scheduled_time == time:
                    sametime_flights.append(flight)
                else:
                    sorted_sametime_flights = self.sort_codeshare_sametime(sametime_flights)
                    sorted_flight_list.extend(sorted_sametime_flights)
                    sametime_flights = [flight]
                    time = flight.scheduled_time
        # Last flight
        sorted_sametime_flights = self.sort_codeshare_sametime(sametime_flights)
        sorted_flight_list.extend(sorted_sametime_flights)

        if len(self.flight_list) != len(sorted_flight_list):
            print("WARNING: length of sorted_list is different from original flight_list.")

        self.flight_list = sorted_flight_list


    def load_all_flight(self, flight_type):
        self.flight_list = Jsonstream().get_flight_list(flight_type)
        self.sort_codeshare()
    
    
    def get_after_flight(self, flight_type, t1=True, t2=True):
        now_time = datetime.now()
        if flight_type[1] == "d":
            start_time_dt = now_time + timedelta(minutes=-5)
        else:
            start_time_dt = now_time + timedelta(minutes=-10)

        after_flight = []
        for flight in self.flight_list:
            scheduled_dt = datetime.strptime(flight.scheduled_time, '%Y/%m/%d %H:%M:%S')
            if flight.estimated_time == "":
                older = scheduled_dt
            else:
                estimated_dt = datetime.strptime(flight.estimated_time, '%Y/%m/%d %H:%M:%S')
                older = estimated_dt if scheduled_dt < estimated_dt else scheduled_dt
 
            if older > start_time_dt:
                if (flight.terminal == "1" and t1 == True) or (flight.terminal == "2" and t2 == True):
                    after_flight.append(flight)
        
        return after_flight


if __name__ == "__main__":
    ob = Observer()
    flight_type = "dd"
    ob.load_all_flight(flight_type=flight_type)
    #ob.sort_codeshare()
    """
    after_flight = ob.get_after_flight(flight_type)
    for f in after_flight:
        print(f)
    """
