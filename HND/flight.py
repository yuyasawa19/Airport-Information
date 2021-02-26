class Flight:

    def __init__(self, airline_code, airline_name_jp, airline_name_en, flight_no,
                 district_jp, district_en, transition_jp, transition_en,
                 scheduled_time, estimated_time, terminal, wing, remarks, gate_jp, gate_en):
        self.airline_code = airline_code
        self.airline_name_jp = airline_name_jp
        self.airline_name_en = airline_name_en
        self.flight_no = flight_no
        self.district_jp = district_jp
        self.district_en = district_en
        self.transition_jp = transition_jp
        self.transition_en = transition_en
        self.scheduled_time = scheduled_time
        self.estimated_time = estimated_time
        self.terminal = terminal
        self.wing = wing
        self.remarks = remarks
        self.gate_jp = gate_jp
        self.gate_en = gate_en

    
    def __str__(self):
        string = \
            "airline_code: " + str(self.airline_code) + \
            "\nairline_name_jp: " + str(self.airline_name_jp) + \
            "\nairline_name_en: " + str(self.airline_name_en) + \
            "\ndistrict_jp: " + str(self.district_jp) + \
            "\ndistrict_en: " + str(self.district_en) + \
            "\ntransition_jp: " + str(self.transition_jp) + \
            "\ntransition_en: " + str(self.transition_en) + \
            "\nscheduled_time: " + str(self.scheduled_time) + \
            "\nestimated_time: " + str(self.estimated_time) + \
            "\nterminal: " + str(self.terminal) + \
            "\nwing: " + str(self.wing) + \
            "\nremarks: " + str(self.remarks) + \
            "\ngate_jp: " + str(self.gate_jp) + \
            "\ngate_en: " + str(self.gate_en)        
        return string
