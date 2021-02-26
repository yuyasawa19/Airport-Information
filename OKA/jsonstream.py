#-*-coding:utf-8-*-

import urllib.request
import json
from datetime import datetime, timedelta
from air_data import AirData



class Jsonstream:

    url = "https://www.naha-airport.co.jp/fis/fis_national.json?"


    def get_json_object(self):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        request = urllib.request.Request(url=self.url, headers=headers)
        response = urllib.request.urlopen(request)
        json_object = json.loads(response.read().decode("utf8"))

        return json_object


    def get_airdata_list(self):
        json_object = self.get_json_object()
        data_list = json_object["data"]
        air_data_list = []

        for data in data_list:
            code = data[0]
            flight_no = int(data[1])
            district_jp = data[2].replace("　","").replace("／","/")
            district_en = data[3]
            scheduled_time = data[4]
            estimated_time = data[5]
            update_time = data[6]
            status_jp = data[7]
            status_en = data[8]
            if status_jp == '欠航':
                gate = ''
            else:
                gate = data[9]
            dep_or_arr = data[10]
            codeshare_kind = data[11]
            codeshare_num = data[12]
            codeshare_code_1 = data[13]
            codeshare_flight_no_1 = data[14]
            codeshare_code_2 = data[15]
            codeshare_flight_no_2 = data[16]
            codeshare_code_3 = data[17]
            codeshare_flight_no_3 = data[18]

            ad = AirData(code, flight_no, district_jp, district_en, scheduled_time, estimated_time, update_time, status_jp, status_en, gate, dep_or_arr, codeshare_kind, codeshare_num, codeshare_code_1, codeshare_flight_no_1, codeshare_code_2, codeshare_flight_no_2, codeshare_code_3, codeshare_flight_no_3)

            # Remove code sharing flight which mode is "S"
            if codeshare_kind == "S":
                continue
            air_data_list.append(ad)

        return air_data_list

    
    def get_today_airdata_list(self, kind):
        now_time = datetime.now()

        if kind == 'D':
            start_time = now_time + timedelta(minutes=-10)
        else:
            start_time = now_time + timedelta(minutes=-30)

        start_time_str = start_time.strftime("%Y%m%d%H%M%S")
        start_time_int = int(start_time_str)

        end_time = now_time + timedelta(days=1)
        end_time_str = end_time.strftime("%Y%m%d%H%M%S")
        end_time_int = int(end_time_str)

        tomorrow_am00 = int(end_time_int/10E5) * 10E5  # float

        airdata_list = self.get_airdata_list()
        today_airdata_list = []

        for ad in airdata_list:
            if ad.dep_or_arr == kind:
                if ad.estimated_time == '':
                    estimated = ad.scheduled_time
                elif ad.estimated_time > ad.scheduled_time:
                    estimated = ad.estimated_time
                else:
                    estimated = ad.scheduled_time
                if int(estimated) < int(start_time_int):
                    continue
                if int(estimated) > int(tomorrow_am00):
                    break
                today_airdata_list.append(ad)

        return today_airdata_list