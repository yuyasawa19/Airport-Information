from bs4 import BeautifulSoup
import requests
from air_data import AirData

dep_url = "https://www.osaka-airport.co.jp/flight/itm_searchresult?s01=1&airport=&s03=&s04=&submit=1"
arr_url = "https://www.osaka-airport.co.jp/flight/itm_searchresult?s01=2&airport=&s03=&s04=&submit=1"
dep_url_en = "https://www.osaka-airport.co.jp/en/flight/itm_searchresult?s01=1&airport=&s03=&s04=&submit=1"
arr_url_en = "https://www.osaka-airport.co.jp/en/flight/itm_searchresult?s01=2&airport=&s03=&s04=&submit=1"


class HTMLstream:

    def get_flight_list(self, url, flight_type):
        flight_list = []
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        soup_lists = soup.find_all("tr")
        for i, flight in enumerate(soup_lists):
            if i >= 2:
                span = flight.find_all("span")
                scheduled = span[0].text
                estimated = span[1].text
                airline = span[3].text
                td = flight.find_all("td")
                district = td[1].text
                flight_no = td[2].find("span",{"class":"airline"}).next_sibling.strip()
                gate = td[3].text
                state = td[4].text
                try:
                    int(estimated.replace(":",""))
                except:
                    if estimated != "---":
                        state = estimated
                        estimated = "---"
                flight_list.append(
                    AirData(scheduled=scheduled, estimated=estimated, district=district,
                            airline=airline, flight_no=flight_no, gate=gate, state=state)
                )
        return flight_list


    def get_all_flights(self, flight_type):
        if flight_type == "dep":
            url_jp = dep_url
            url_en = dep_url_en
        elif flight_type == "arr":
            url_jp = arr_url
            url_en = arr_url_en
        else:
            print("Error: invalid flight_type.")
            return {}

        flight_lists_jp = self.get_flight_list(url_jp, flight_type)
        flight_lists_en = self.get_flight_list(url_en, flight_type)

        if len(flight_lists_jp) != len(flight_lists_en):
            print("Error: len(flight_lists) is different between languages.")
            return {}
        
        flight_list = []
        for flight_jp, flight_en in zip(flight_lists_jp, flight_lists_en):
            flight = {
                "scheduled" : flight_jp.scheduled,
                "estimated" : flight_jp.estimated,
                "airline" : flight_jp.airline,
                "flight_no" : flight_jp.flight_no,
                "district_jp" : flight_jp.district,
                "district_en" : flight_en.district,
                "state_jp" : flight_jp.state,
                "state_en" : flight_en.state,
                "gate" : flight_jp.gate
            }
            flight_list.append(flight)
        
        return flight_list


# Just for debug
if __name__ == "__main__":
    lists = HTMLstream().get_all_flights("arr")
    print(lists)
