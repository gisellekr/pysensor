class ConvertData:
    def printData(self, data):
        pop = "강수확률 : " + data[0] + "%"
        pty = self.convertPTY(data[1])
        pcp = self.convertPCP(data[2])
        reh = "습도 : " + data[3] + "%"
        sno = self.convertSNO(data[4])
        sky = self.convertSKY(data[5])
        tmp = "1시간 기온 : " + data[6] + "℃"
        tmn = "아침 최저기온 : " + data[7] + "℃"
        tmx = "낮 최고기온 : " + data[8] + "℃"
        uuu = self.convertUUU(data[9])
        vvv = self.convertVVV(data[10])
        wav = "파고 : " + data[11] + "M"
        vec = self.convertVEC(data[12])
        wsd = "풍속 : " + data[13] + "m/s"
        print(pop)
        print(pty)
        print(pcp)
        print(reh)
        print(sno)
        print(sky)
        print(tmp)
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

        return ret_value

    def convertPCP(self, pcp):
        ret_value = "1시간 강수량 : "
        f_pcp = float(pcp)
        if f_pcp <= 1.0:
            ret_value = ret_value + "1mm 미만"
        elif f_pcp > 1.0 and f_pcp < 30:
            ret_value = ret_value + "1~29mm"
        elif f_pcp >= 30 and f_pcp < 50:
            ret_value = ret_value + "30~50mm"
        else:
            ret_value = ret_value + "50mm 이상"
        return ret_value

    def convertSNO(self, sno):
        ret_value = "1시간 신적설 : "
        f_sno = float(sno)
        if f_sno <= 1:
            ret_value = ret_value + "1cm 미만"
        elif f_sno > 1 and f_sno < 5:
            ret_value = ret_value + "1~4.9cm"
        else:
            ret_value = ret_value + "5cm 이상"
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
        con_vec = (i_vec + (22.5 * 0.5)) // 22.5
        if con_vec == 0:
            ret_value = ret_value + "N"
        elif con_vec == 1:
            ret_value = ret_value + "NNE"
        elif con_vec == 2:
            ret_value = ret_value + "NE"
        elif con_vec == 3:
            ret_value = ret_value + "ENE"
        elif con_vec == 4:
            ret_value = ret_value + "E"
        elif con_vec == 5:
            ret_value = ret_value + "ESE"
        elif con_vec == 6:
            ret_value = ret_value + "SE"
        elif con_vec == 7:
            ret_value = ret_value + "SSE"
        elif con_vec == 8:
            ret_value = ret_value + "S"
        elif con_vec == 9:
            ret_value = ret_value + "SSW"
        elif con_vec == 10:
            ret_value = ret_value + "SW"
        elif con_vec == 11:
            ret_value = ret_value + "WSW"
        elif con_vec == 12:
            ret_value = ret_value + "W"
        elif con_vec == 13:
            ret_value = ret_value + "WNW"
        elif con_vec == 14:
            ret_value = ret_value + "NW"
        elif con_vec == 15:
            ret_value = ret_value + "NNW"
        elif con_vec == 16:
            ret_value = ret_value + "N"
        return ret_value

