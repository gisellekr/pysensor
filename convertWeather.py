class ConvertData:
    def printData(self, data):
        pop = "강수확률 : " + data[0] + "%"
        pty = self.convertPTY(data[1])
        r06 = self.convertR06(data[2])
        reh = "습도 : " + data[3] + "%"
        s06 = self.convertS06(data[4])
        sky = self.convertSKY(data[5])
        t3h = "3시간 기온 : " + data[6] + "℃"
        tmn = "아침 최저기온 : " + data[7] + "℃"
        tmx = "낮 최고기온 : " + data[8] + "℃"
        uuu = self.convertUUU(data[9])
        vvv = self.convertVVV(data[10])
        wav = "파고 : " + data[11] + "M"
        vec = self.convertVEC(data[12])
        wsd = "풍속 : " + data[13] + "m/s"
        print(pop)
        print(pty)
        print(r06)
        print(reh)
        print(s06)
        print(sky)
        print(t3h)
        print(tmn)
        print(tmx)
        print(uuu)
        print(vvv)
        print(wav)
        print(vec)
        print(wsd)

    def convertPTY(self, pty):
        ret_value = "강수형태 : "
        i_pty = int(pty)
        if i_pty == 0:
            ret_value = ret_value + "없음"
        elif i_pty == 1:
            ret_value = ret_value + "비"
        elif i_pty == 2:
            ret_value = ret_value + "비/눈"
        elif i_pty == 3:
            ret_value = ret_value + "눈"
        elif i_pty == 4:
            ret_value = ret_value + "소나기"
        elif i_pty == 5:
            ret_value = ret_value + "빗방울"
        elif i_pty == 6:
            ret_value = ret_value + "빗방울/눈날림"
        elif i_pty == 7:
            ret_value = ret_value + "눈날림"
        return ret_value

    def convertR06(self, r06):
        ret_value = "6시간 강수량 : "
        f_r06 = float(r06)
        if f_r06 < 0.1:
            ret_value = ret_value + "없음"
        elif f_r06 >= 0.1 and f_r06 < 1:
            ret_value = ret_value + "1mm 미만"
        elif f_r06 >= 1 and f_r06 < 5:
            ret_value = ret_value + "1~4mm"
        elif f_r06 >= 5 and f_r06 < 10:
            ret_value = ret_value + "5~9mm"
        elif f_r06 >= 10 and f_r06 < 20:
            ret_value = ret_value + "10~19mm"
        elif f_r06 >= 20 and f_r06 < 40:
            ret_value = ret_value + "20~39mm"
        elif f_r06 >= 40 and f_r06 < 70:
            ret_value = ret_value + "40~69mm"
        else:
            ret_value = ret_value + "70mm 이상"
        return ret_value

    def convertS06(self, s06):
        ret_value = "6시간 신적설 : "
        f_s06 = float(s06)
        if f_s06 < 0.1:
            ret_value = ret_value + "없음"
        elif f_s06 >= 0.1 and f_s06 < 1:
            ret_value = ret_value + "1cm 미만"
        elif f_s06 >= 1 and f_s06 < 5:
            ret_value = ret_value + "1~4cm"
        elif f_s06 >= 5 and f_s06 < 10:
            ret_value = ret_value + "5~9cm"
        elif f_s06 >= 10 and f_s06 < 20:
            ret_value = ret_value + "10~19cm"
        else:
            ret_value = ret_value + "20cm 이상"
        return ret_value

    def convertSKY(self, sky):
        ret_value = "하늘상태 : "
        i_sky = int(sky)
        if i_sky == 1:
            ret_value = ret_value + "맑음"
        elif i_sky == 2:
            ret_value = ret_value + "구름조금"
        elif i_sky == 3:
            ret_value = ret_value + "구름많음"
        elif i_sky == 4:
            ret_value = ret_value + "흐림"
        return ret_value

    def convertUUU(self, uuu):
        ret_value = "풍속(동서) : "
        f_uuu = float(uuu)
        if f_uuu < 0:
            ret_value = ret_value + str(abs(f_uuu)) + "m/s (서)"
        else:
            ret_value = ret_value + str(f_uuu) + "m/s (동)"
        return ret_value

    def convertVVV(self, vvv):
        ret_value = "풍속(남북) : "
        f_vvv = float(vvv)
        if f_vvv < 0:
            ret_value = ret_value + str(abs(f_vvv)) + "m/s (남)"
        else:
            ret_value = ret_value + str(f_vvv) + "m/s (북)"
        return ret_value

    def convertVEC(self, vec):
        ret_value = "풍향 : "
        i_vec = int(vec)
        if i_vec == 0:
            ret_value = ret_value + "N"
        elif i_vec > 0 and i_vec < 45:
            ret_value = ret_value + "NNE"
        elif i_vec == 45:
            ret_value = ret_value + "NE"
        elif i_vec > 45 and i_vec < 90:
            ret_value = ret_value + "NEE"
        elif i_vec == 90:
            ret_value = ret_value + "E"
        elif i_vec > 90 and i_vec < 135:
            ret_value = ret_value + "ESE"
        elif i_vec == 135:
            ret_value = ret_value + "SE"
        elif i_vec > 135 and i_vec < 180:
            ret_value = ret_value + "SES"
        elif i_vec == 180:
            ret_value = ret_value + "S"
        elif i_vec > 180 and i_vec < 225:
            ret_value = ret_value + "SSW"
        elif i_vec == 225:
            ret_value = ret_value + "SW"
        elif i_vec > 225 and i_vec < 270:
            ret_value = ret_value + "SWW"
        elif i_vec == 270:
            ret_value = ret_value + "W"
        elif i_vec > 270 and i_vec < 315:
            ret_value = ret_value + "WNW"
        elif i_vec == 315:
            ret_value = ret_value + "NW"
        elif i_vec > 315 and i_vec > 360:
            ret_value = ret_value + "NWN"
        elif i_vec == 360:
            ret_value = ret_value + "N"
        return ret_value

