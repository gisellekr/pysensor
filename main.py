import serial
import signal
import threading
import time
import pickle

from serial.serialutil import Timeout

# 데이터 저장 리스트
data_array = []

# 쓰레드 종료 변수
exit_thread = False

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
    crc_data = []
    for val in range(len(data)-1):
        crc_data.append(data[val])

    check_crc = makeCrc(crc_data)
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

        print(m_res)
        with open("sdata.log", "wb") as f:
            pickle.dump(m_res, f)

        time.sleep(1)




def stopThread(signum, frame):
    global exit_thread
    exit_thread = True

def readThread(ser):
    global data_array
    global exit_thread
    print(exit_thread)
    while not exit_thread:
        try:
            data = ser.readline()
            
            if data:
                # print(data)
                parsingResOfSensor(data)

        except serial.SerialException as e:
            break


def writeThread(ser):
    send_data = [17, 2, 1, 0]
    send_data.append(makeCrc(send_data))
    print(bytearray(send_data))
    ser.write(bytearray(send_data))
    threading.Timer(10, writeThread, args=(ser,)).start()


if __name__ == "__main__":
    # 종료 시그널 등록
    signal.signal(signal.SIGINT, stopThread)

    # 시리얼 열기
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0)

    print(ser.is_open)

    if ser.is_open:
        # Request Command
        writeThread(ser)

        # 시리얼 읽기 쓰레드 생성
        r_thread = threading.Thread(target=readThread, args=(ser,))
        r_thread.start()

        


