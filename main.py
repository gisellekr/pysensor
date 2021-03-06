import serial
import signal
import threading
import time
# import pickle
import sys
import requests
import datetime
import station
import location_x
import location_y
import convertWeather

from urllib.parse import urlencode, quote_plus
from xml.etree import ElementTree

url_station = "http://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getMsrstnList"
url_data = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
url_weather = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
url_weather20 = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
de_key = "FiT7JZmgP3ia3n3gZS+0RAryoftJJxWjSOaRm2BR1dOoJRHeR1vOzwpAVDN9zb0OzAJIH5hqN/8EkLkZsKlP1Q=="

def makeCrc(data):
    sum = 0
    for val in data:
        # print("val = %d"%val)
        sum += val
    crc = 256 - (sum % 256)
    return crc

def parsingResOfSensor(data):
    # m_res = {}
    m_res = []
    # Sensor : 0
    m_res.append(0)
    crc_data = []
    for val in range(len(data)-1):
        crc_data.append(data[val])

    check_crc = makeCrc(crc_data)
    # print("check_crc = %d, data[27] = %d"%(check_crc, data))
    if (check_crc != data[27]):
        return -1

    if data[1] == 0x19:
        tmp_co2 = data[4]
        tmp_co2 = tmp_co2 << 8
        # m_res['CO2'] = tmp_co2 + data[5]
        m_res.append(tmp_co2 + data[5])

        tmp_voc = data[6]
        tmp_voc = tmp_voc << 8
        # m_res['VOC'] = tmp_voc + data[7]
        m_res.append(tmp_voc + data[7])

        tmp_humidity = data[8]
        tmp_humidity = tmp_humidity * 256
        tmp_humidity = tmp_humidity + data[9]
        # m_res['Humidity'] = tmp_humidity / 10
        m_res.append(tmp_humidity / 10)

        tmp_temperature = data[10]
        tmp_temperature = tmp_temperature * 256
        tmp_temperature = tmp_temperature + data[11]
        # m_res['Temperature'] = (tmp_temperature - 500) / 10
        m_res.append((tmp_temperature - 500) / 10)

        tmp_pm1 = data[12]
        tmp_pm1 = tmp_pm1 << 8
        # m_res['PM1'] = tmp_pm1 + data[13]
        m_res.append(tmp_pm1 + data[13])

        tmp_pm25 = data[14]
        tmp_pm25 = tmp_pm25 << 8
        # m_res['PM25'] = tmp_pm25 + data[15]
        m_res.append(tmp_pm25 + data[15])

        tmp_pm10 = data[16]
        tmp_pm10 = tmp_pm10 << 8
        # m_res['PM10'] = tmp_pm10 + data[17]
        m_res.append(tmp_pm10 + data[17])

        tmp_voc_now_ref = data[18]
        tmp_voc_now_ref = tmp_voc_now_ref << 8
        # m_res['VOCNowRef'] = tmp_voc_now_ref + data[19]
        m_res.append(tmp_voc_now_ref + data[19])

        tmp_voc_ref_rvalue = data[20]
        tmp_voc_ref_rvalue = tmp_voc_ref_rvalue << 8
        # m_res['VOCRefRValue'] = tmp_voc_ref_rvalue + data[21]
        m_res.append(tmp_voc_ref_rvalue + data[21])

        tmp_voc_now_rvalue = data[22]
        tmp_voc_now_rvalue = tmp_voc_now_rvalue << 8
        # m_res['VOCNowRValue'] = tmp_voc_now_rvalue + data[23]
        m_res.append(tmp_voc_now_rvalue + data[23])

        tmp_reserve = data[24]
        tmp_reserve = tmp_reserve << 8
        # m_res['Reserve'] = tmp_reserve + data[25]
        m_res.append(tmp_reserve + data[25])

        m_res.append(data[26])

        m_res.append(data[27])

        # print(m_res)
        str_data = list(map(str, m_res))
        with open("sdata.log", "w") as f:
            # pickle.dump(m_res, f)
            f.write(",".join(str_data))


        with open("sdata.log", "r") as f:
            read_data = f.read()
            list_data = read_data.split(",")
            num_data = list(map(float, list_data))
            print("Type:{0}, CO2:{1}, VOC:{2}, Humidity:{3}, Temperature:{4}, PM1:{5}, PM2.5:{6}, PM10:{7}, VOC now:{8}, VOC rvalue:{9}, VOC now rvalue:{10}, Reserve:{11}, State:{12}".format(num_data[0], num_data[1], num_data[2], num_data[3], num_data[4], num_data[5], num_data[6], num_data[7], num_data[8], num_data[9], num_data[10], num_data[11], num_data[12]))

        time.sleep(1)

def parsingResOfAirKorea(data):
    m_res = []

    try:
        with open("sdata.log", "r") as f:
            read_data = f.read()
            latest_data = read_data.split(",")
            # Sensor Data ???????????? ??????
            if len(latest_data) > 7:
                latest_data = ["1", "0", "0", "0", "0", "0", "0"]
            # print("latest_data = {0}".format(latest_data))
    except FileNotFoundError:
        latest_data = ["1", "0", "0", "0", "0", "0", "0"]

    # AirKorea : 1
    m_res.append("1")
    for element in data:
        try:
            pm25 = element.findtext("pm25Value")
            # Value Check
            int(pm25)
            m_res.append(pm25)
        except ValueError:
            m_res.append(latest_data[1])
        try:
            pm10 = element.findtext("pm10Value")
            int(pm10)
            m_res.append(pm10)
        except ValueError:
            m_res.append(latest_data[2])
        try:
            o3 = element.findtext("o3Value")
            float(o3)
            m_res.append(o3)
        except ValueError:
            m_res.append(latest_data[3])
        try:
            no2 = element.findtext("no2Value")
            float(no2)
            m_res.append(no2)
        except ValueError:
            m_res.append(latest_data[4])
        try:
            co = element.findtext("coValue")
            float(co)
            m_res.append(co)
        except ValueError:
            m_res.append(latest_data[5])
        try:
            so2 = element.findtext("so2Value")
            float(so2)
            m_res.append(so2)
        except ValueError:
            m_res.append(latest_data[6])

        # ?????? ??????
        # element.findtext("dataTime")
        break

    # print("m_res = {0}".format(m_res))
    with open("sdata.log", "w") as f:
        f.write(",".join(m_res))

    with open("sdata.log", "r") as f:
        read_data = f.read()
        list_data = read_data.split(",")
        num_data = list(map(float, list_data))
        print("type:{0}, PM2.5:{1}, PM10:{2}, O3:{3}, NO2:{4}, CO:{5}, SO2:{6}".format(num_data[0], num_data[1], num_data[2], num_data[3], num_data[4], num_data[5], num_data[6]))

    time.sleep(1)

def stopThread(signum, frame):
    global exit_thread
    exit_thread = True

def readThread(ser):
    global data_array
    global exit_thread
    while True:
        try:
            data = ser.readline()
            if data:
                # print(data)
                parsingResOfSensor(data)

        except serial.SerialException as e:
            break
        time.sleep(1)


def writeThread(ser, timer):
    send_data = [17, 2, 1, 0]
    send_data.append(makeCrc(send_data))
    # print(bytearray(send_data))
    ser.write(bytearray(send_data))
    # 10s by Test
    # threading.Timer(10, writeThread, args=(ser,)).start()
    # 3600 is 1 Hour
    threading.Timer(timer, writeThread, args=(ser, timer,)).start()

def requestThread(str_station, idx_station, timer):
    # AirKorea
    requestAirKorea(str_station)

    # Weather
    requestWeather(idx_station)

    # 10s by Test
    # threading.Timer(10, requestThread, args=(str_station, idx_station,)).start()
    # 3600 is 1 Hour
    threading.Timer(timer, requestThread, args=(str_station, idx_station, timer,)).start()

def requestAirKorea(str_station):
    query_params = "?" + urlencode({
        quote_plus("serviceKey"): de_key,
        quote_plus("returnType"): "xml",
        quote_plus("numOfRows"): "1",
        quote_plus("pageNo"): "1",
        quote_plus("stationName"): str_station,
        quote_plus("dataTerm"): "DAILY",
        quote_plus("ver"): "1.3"
    })

    req_body = requests.get(url_data + query_params)
    root_data = ElementTree.fromstring(req_body.text)

    iter_data = root_data.iter(tag="item")
    parsingResOfAirKorea(iter_data)

def requestWeather(str_station):
    curr = datetime.datetime.now()
    default_date = curr_date = curr.strftime("%Y%m%d")
    default_time = "0200"
    if curr.hour < 2:
        m_curr = curr - datetime.timedelta(days=1)
        curr_date = m_curr.strftime("%Y%m%d")
        curr_time = "2300"
    elif curr.hour < 5:
        curr_time = "0200"
    elif curr.hour < 8:
        curr_time = "0500"
    elif curr.hour < 11:
        curr_time = "0800"
    elif curr.hour < 14:
        curr_time = "1100"
    elif curr.hour < 17:
        curr_time = "1400"
    elif curr.hour < 20:
        curr_time = "1700"
    elif curr.hour < 23:
        curr_time = "2000"
    else:
        curr_time = "2300"
        
    nx = location_x.LocationXData().getLocationX(str_station)
    ny = location_y.LocationYData().getLocationY(str_station)
    
    # ?????? ?????? 2??? Data??? ????????? Default ?????? ??????
    default_params = "?" + urlencode({
        quote_plus("ServiceKey"): de_key,
        quote_plus("pageNo"): "1",
        quote_plus("numOfRows"): "250",
        quote_plus("dataType"): "xml",
        quote_plus("base_date"): curr_date,
        quote_plus("base_time"): default_time,
        quote_plus("nx"): nx,
        quote_plus("ny"): ny
    })
    # default_body = requests.get(url_weather + default_params)
    default_body = requests.get(url_weather20 + default_params)
    default_data = ElementTree.fromstring(default_body.text)
    default_items = default_data.iter(tag="items")
    default_array = ["0"] * 14
    default_result = parsingDefaultWeather(default_array, default_items, default_date)
    print("default_result={0}".format(default_result))

    # ?????? ?????? ?????? ?????? Data??? Update
    current_params = "?" + urlencode({
        quote_plus("ServiceKey"): de_key,
        quote_plus("pageNo"): "1",
        quote_plus("numOfRows"): "14",
        quote_plus("dataType"): "xml",
        quote_plus("base_date"): curr_date,
        quote_plus("base_time"): curr_time,
        quote_plus("nx"): nx,
        quote_plus("ny"): ny
    })
    # current_body = requests.get(url_weather + current_params)
    current_body = requests.get(url_weather20 + current_params)
    current_data = ElementTree.fromstring(current_body.text)
    current_items = current_data.iter(tag="items")
    current_result = parsingCurrentWeather(default_array, current_items)
    print("current_result={0}".format(current_result))

    with open("wdata.log", "w") as f:
        f.write(",".join(current_result))

    with open("wdata.log", "r") as f:
        read_data = f.read()
        list_data = read_data.split(",")
        # num_data = list(map(float, list_data))
        # print("POP:{0}, PTY:{1}, PCP:{2}, REH:{3}, SNO:{4}, SKY:{5}, TMP:{6}, TMN:{7}, TMX:{8}, UUU:{9}, VVV:{10}, WAV:{11}, VEC:{12}, WSD:{13}".format(num_data[0], num_data[1], num_data[2], num_data[3], num_data[4], num_data[5], num_data[6], num_data[7], num_data[8], num_data[9], num_data[10], num_data[11], num_data[12], num_data[13]))
    
        convertWeather.ConvertData().printData(list_data)

def parsingDefaultWeather(m_result, datas, date):
    
    getPOP = getPTY = getPCP = getREH = getSNO = getSKY = getTMP = getTMN = getTMX = getUUU = getVVV = getWAV = getVEC = getWSD = False
    for item in datas:
        for element in item:
            category = element.findtext("category")
            fcst_date = element.findtext("fcstDate")
            if (getPOP == False) and (category == "POP") and (fcst_date == date):
                m_result[0] = element.findtext("fcstValue")
                getPOP = True
            elif (getPTY == False) and (category == "PTY") and (fcst_date == date):
                m_result[1] = element.findtext("fcstValue")
                getPTY = True
            elif (getPCP == False) and (category == "PCP") and (fcst_date == date):
                print("PCP={0}".format(element.findtext("fcstValue")))
                arrayPCP = element.findtext("fcstValue").split("mm")
                m_result[2] = arrayPCP[0]
                getPCP = True
            elif (getREH == False) and (category == "REH") and (fcst_date == date):
                m_result[3] = element.findtext("fcstValue")
                getREH = True
            elif (getSNO == False) and (category == "SNO") and (fcst_date == date):
                print("SNO={0}".format(element.findtext("fcstValue")))
                arraySNO = element.findtext("fcstValue").split("cm")
                m_result[4] = arraySNO[0]
                getSNO = True
            elif (getSKY == False) and (category == "SKY") and (fcst_date == date):
                m_result[5] = element.findtext("fcstValue")
                getSKY = True
            elif (getTMP == False) and (category == "TMP") and (fcst_date == date):
                m_result[6] = element.findtext("fcstValue")
                getTMP = True
            elif (getTMN == False) and (category == "TMN") and (fcst_date == date):
                m_result[7] = element.findtext("fcstValue")
                getTMN = True
            elif (getTMX == False) and (category == "TMX") and (fcst_date == date):
                m_result[8] = element.findtext("fcstValue")
                getTMX = True
            elif (getUUU == False) and (category == "UUU") and (fcst_date == date):
                m_result[9] = element.findtext("fcstValue")
                getUUU = True
            elif (getVVV == False) and (category == "VVV") and (fcst_date == date):
                m_result[10] = element.findtext("fcstValue")
                getVVV = True
            elif (getWAV == False) and (category == "WAV") and (fcst_date == date):
                m_result[11] = element.findtext("fcstValue")
                getWAV = True
            elif (getVEC == False) and (category == "VEC") and (fcst_date == date):
                m_result[12] = element.findtext("fcstValue")
                getVEC = True
            elif (getWSD == False) and (category == "WSD") and (fcst_date == date):
                m_result[13] = element.findtext("fcstValue")
                getWSD = True
    return m_result

def parsingCurrentWeather(m_result, datas):
    
    getPOP = getPTY = getPCP = getREH = getSNO = getSKY = getTMP = getTMN = getTMX = getUUU = getVVV = getWAV = getVEC = getWSD = False
    for item in datas:
        for element in item:
            category = element.findtext("category")
            # ?????? ?????? Data??? Update ?????? ???
            if (getPOP == True) and (category == "POP"):
                break

            if (getPOP == False) and (category == "POP"):
                m_result[0] = element.findtext("fcstValue")
                getPOP = True
            elif (getPTY == False) and (category == "PTY"):
                m_result[1] = element.findtext("fcstValue")
                getPTY = True
            elif (getPCP == False) and (category == "PCP"):
                arrayPCP = element.findtext("fcstValue").split("mm")
                m_result[2] = arrayPCP[0]
                getPCP = True
            elif (getREH == False) and (category == "REH"):
                m_result[3] = element.findtext("fcstValue")
                getREH = True
            elif (getSNO == False) and (category == "SNO"):
                arraySNO = element.findtext("fcstValue").split("cm")
                m_result[4] = arraySNO[0]
                getSNO = True
            elif (getSKY == False) and (category == "SKY"):
                m_result[5] = element.findtext("fcstValue")
                getSKY = True
            elif (getTMP == False) and (category == "TMP"):
                m_result[6] = element.findtext("fcstValue")
                getTMP = True
            elif (getTMN == False) and (category == "TMN"):
                m_result[7] = element.findtext("fcstValue")
                getTMN = True
            elif (getTMX == False) and (category == "TMX"):
                m_result[8] = element.findtext("fcstValue")
                getTMX = True
            elif (getUUU == False) and (category == "UUU"):
                m_result[9] = element.findtext("fcstValue")
                getUUU = True
            elif (getVVV == False) and (category == "VVV"):
                m_result[10] = element.findtext("fcstValue")
                getVVV = True
            elif (getWAV == False) and (category == "WAV"):
                m_result[11] = element.findtext("fcstValue")
                getWAV = True
            elif (getVEC == False) and (category == "VEC"):
                m_result[12] = element.findtext("fcstValue")
                getVEC = True
            elif (getWSD == False) and (category == "WSD"):
                m_result[13] = element.findtext("fcstValue")
                getWSD = True
    return m_result

if __name__ == "__main__":
    try:
        with open("configdata.conf", "r") as f:
            read_sensor = f.readline()
            sensor_array = read_sensor.split("=")
            print("sensor_array[0]={0}, sensor_array[1]={1}".format(sensor_array[0], sensor_array[1]))
            if sensor_array[1].strip() == "ON":
                ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0)
                read_timer = f.readline()
                timer_array = read_timer.split("=")
                print("timer_array[0]={0}, timer_array[1]={1}".format(timer_array[0], timer_array[1]))
                timer = int(timer_array[1].strip())

                if ser.is_open:
                    # Request Command for Sensor data
                    writeThread(ser, timer)

                    # Receive for Sensor data
                    r_thread = threading.Thread(target=readThread, args=(ser,))
                    r_thread.start()
                else:
                    print("Cannot connect serial port(/dev/ttyUSB0)")
            elif sensor_array[1].strip() == "OFF":
                read_timer = f.readline()
                timer_array = read_timer.split("=")
                print("timer_array[0]={0}, timer_array[1]={1}".format(timer_array[0], timer_array[1]))
                timer = int(timer_array[1].strip())

                read_station = f.readline()
                station_array = read_station.split("=")
                print("station_array[0]={0}, station_array[1]={1}".format(station_array[0], station_array[1]))
                idx_station = station_array[1].strip()
                try:
                    str_station = station.StationData().getStationName(idx_station)
                    print("str_station={0}".format(str_station))
                    requestThread(str_station, idx_station, timer)
                except KeyError:
                    print("Not found station, Check to station index")


            else:
                print("Cannot find config data, Check to configdata.conf")
    except FileNotFoundError:
        print("No such file: configdata.conf")

        
# State Change by configdata.conf
# Command
# /usr/bin/python3 /home/pi/work/pysensor/main.py
