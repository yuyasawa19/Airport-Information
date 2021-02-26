import json
import urllib.request

from flight import Flight


class Jsonstream:

    def get_json_object(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        json_object = json.loads(response.read().decode("utf8"))
        return json_object
    

    # Load local json file for debug.
    def get_local_json_object(self, json_path):
        with open(json_path, "r") as f:
            json_object = json.load(f)
            return json_object
    

    def get_flight_list(self, flight_type):
        if flight_type == "dd":  # Domestic Departure
            url = "https://tokyo-haneda.com/app_resource/flight/data/dms/hdacfdep.json"
        elif flight_type == "da":  # Domestic Arrival
            url = "https://tokyo-haneda.com/app_resource/flight/data/dms/hdacfarv.json"
        # TODO: International flights is not supported to "Flight" class.
        elif flight_type == "id":  # International Departure
            url = "https://tokyo-haneda.com/app_resource/flight/data/int/hdacfdep.json"
        elif flight_type == "ia":  # International Arrival
            url = "https://tokyo-haneda.com/app_resource/flight/data/int/hdacfarv.json"
        else:
            print("Invalid flight_type.\nAvailable type: ['dd','da','id','ia']")
            return []
        
        json_object = self.get_json_object(url)
        #json_object = self.get_local_json_object("/Users/yuyasawa/hnd/hdacfdep.json")
        flight_list = []

        if flight_type[1] == "d":
            for flight_info in json_object["flight_info"]:
                flight = Flight(
                    airline_code=flight_info["航空会社"][0]["ＡＬコード"],
                    airline_name_jp=flight_info["航空会社"][0]["ＡＬ和名称"],
                    airline_name_en=flight_info["航空会社"][0]["ＡＬ英名称"],
                    flight_no=flight_info["航空会社"][0]["便名"],
                    district_jp=flight_info["行先地空港和名称"],
                    district_en=flight_info["行先地空港英名称"],
                    transition_jp=flight_info["経由地空港和名称"],
                    transition_en=flight_info["経由地空港英名称"],
                    scheduled_time=flight_info["定刻"],
                    estimated_time=flight_info["変更時刻"],
                    terminal=flight_info["ターミナル区分"],
                    wing=flight_info["ウイング区分"],
                    remarks=flight_info["備考訳名称"],
                    gate_jp=flight_info["ゲート和名称"],
                    gate_en=flight_info["ゲート英名称"]
                )
                flight_list.append(flight)
        
        elif flight_type[1] == "a":
            for flight_info in json_object["flight_info"]:
                # TODO: Rewrite for arrival
                flight = Flight(
                    airline_code=flight_info["航空会社"][0]["ＡＬコード"],
                    airline_name_jp=flight_info["航空会社"][0]["ＡＬ和名称"],
                    airline_name_en=flight_info["航空会社"][0]["ＡＬ英名称"],
                    flight_no=flight_info["航空会社"][0]["便名"],
                    district_jp=flight_info["出発地空港和名称"],
                    district_en=flight_info["出発地空港英名称"],
                    transition_jp=flight_info["経由地空港和名称"],
                    transition_en=flight_info["経由地空港英名称"],
                    scheduled_time=flight_info["定刻"],
                    estimated_time=flight_info["変更時刻"],
                    terminal=flight_info["ターミナル区分"],
                    wing=flight_info["ウイング区分"],
                    remarks=flight_info["備考訳名称"],
                    gate_jp=flight_info["スポット番号"],
                    gate_en=flight_info["スポット番号"]
                )
                flight_list.append(flight)
        
        return flight_list


if __name__ == "__main__":
    flight_list = Jsonstream().get_flight_list("da")
    for flight in flight_list:
        print(str(flight) + "\n")
