class AirData:

    def __init__(self, scheduled, estimated, district,
                 airline, flight_no, gate, state):
        self.scheduled = scheduled
        self.estimated = estimated
        self.district = district
        self.airline = airline
        self.flight_no = flight_no
        self.gate = gate
        self.state = state
    
    # Just for debug.
    def show_data(self):
        show_string = ""
        show_string += "Flight:  {0} {1}\n".format(self.airline, self.flight_no)
        show_string += "District:  {0}\n".format(self.district)
        show_string += "Scheduled:  {0}\n".format(self.scheduled)
        show_string += "Estimated:  {0}\n".format(self.estimated)
        show_string += "Gate:  {0}\n".format(self.gate)
        show_string += "State:  {0}\n".format(self.state)
        print(show_string)
