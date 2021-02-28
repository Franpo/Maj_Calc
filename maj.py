#所有牌的编码
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白


#输入实例，规范化输入由前端完成
raw_maj = [1,1,2,2,3,3,4,4,6,6,7,7,9]
income_maj = 9
print("手牌"+ str(raw_maj))
print("进张" + str(income_maj))




#数搭子的库
class Dazi_Calc:

    def Tenpai_Arrange(maj):
        maj.sort()
        return maj
    
    def Maj_GetM(maj):
        maj_m = []
        for num in maj:
            if num >0 and num <10:
                maj_m.append(num)
        return maj_m
    
    def Maj_GetS(maj):
        maj_s = []
        for num in maj:
            if num >10 and num <20:
                maj_s.append(num)
        return maj_s
    
    def Maj_GetP(maj):
        maj_p = []
        for num in maj:
            if num >20 and num <30:
                maj_p.append(num)
        return maj_p

    def Maj_GetZ(maj):
        maj_z = []
        for num in maj:
            if num >30 and num <40:
                maj_z.append(num)
        return maj_z

    #老头牌+字
    def Maj_GetL(maj):
        maj_l = []
        for num in maj:
            if num in yaocyu_list:
                maj_l.append(num)
        return maj_l
    
    #标出所有雀头位置    
    def Maj_GetJyan(maj):
        maj_jyan = []
        lenth = len(maj)
        for num in range(0,lenth-1):
            if maj[num] == maj[num +1]:
                maj_jyan.append(num)
        lenth = len(maj_jyan)
        for num in range(0,lenth-2):
            if maj_jyan[num] == maj_jyan[num +2] - 2:
                maj_jyan[num+2] = 99
        maj_jyan = [num for num in maj_jyan if num != 99]
        lenth = len(maj_jyan)
        for num in range(0,lenth-1):
            if maj_jyan[num] == maj_jyan[num +1] - 1:
                maj_jyan[num+1] = 99
        maj_jyan = [num for num in maj_jyan if num != 99]        
        return maj_jyan

    #和了判定
    def Maj_Agari(maj):
        maj = Dazi_Calc.Tenpai_Arrange(maj)
        maj_jyan = Dazi_Calc.Maj_GetJyan(maj)
        if len(maj_jyan) != 0:
            for jyan_num in maj_jyan:
                maj_temp = []
                maj_temp += maj
                maj_temp.remove(maj[jyan_num])
                maj_temp.remove(maj[jyan_num])
                lenth = len(maj_temp)
                #标记刻子，顺子
                for num in range(0,lenth-2):
                    if maj_temp[num] != 99:
                        if maj_temp[num] != maj_temp[num+1] and maj_temp[num] +1 not in maj_temp:
                            break
                        if maj_temp[num] == maj_temp[num+1] and maj_temp[num] == maj_temp[num+2]:
                            maj_temp[num] = 99
                            maj_temp[num+1] = 99
                            maj_temp[num+2] = 99
                        if maj_temp[num] + 1 in maj_temp and maj_temp[num] + 2 in maj_temp and maj_temp[num] < 30:
                            syun_remove = maj_temp[num]
                            maj_temp.remove(syun_remove)
                            maj_temp.remove(syun_remove + 1)
                            maj_temp.remove(syun_remove + 2)
                            maj_temp.insert(0,99)
                            maj_temp.insert(0,99)
                            maj_temp.insert(0,99)
                #去除所有面子，检查是否有孤张
                maj_temp = [num for num in maj_temp if num != 99]
                if not maj_temp:
                    agari = True
                    break
                
                #七对判定
                elif len(maj_jyan) == 7:
                    agari = True

                #国土判定
                elif len(maj_jyan) == 1:
                    agari = True
                    for num in yaocyu_list:
                        if num not in maj:
                            agari = False
                            break
                else:
                    agari = False
            #检查是否存在虚空第五张牌
            if len(maj) >= 5:
                lenth =len(maj)
                for num in range(0,lenth-4):
                    if maj[num] == maj[num+4]:
                        agari = False
        else:
            agari = False
        return agari

#番种计算的库
class Han_Judge:
    #判断和牌类型
    def Judge_Type(maj,income):
        agari_type = "kokushi"
        maj_jyan = Dazi_Calc.Maj_GetJyan(maj)
        for num in yaocyu_list:
            if num not in maj:
                agari_type = "mentsu"
                break
        #国土十三面
        if agari_type == "kokushi" and maj[maj_jyan[0]] == income:
            agari_type = "kokushi_13"
        #七对判定
        if len(maj_jyan) == 7:
            agari_type = "7_tai"
            #七对中剔除两杯口
            for jyan_num in maj_jyan:
                maj_temp = []
                maj_temp += maj
                maj_temp.remove(maj[jyan_num])
                maj_temp.remove(maj[jyan_num])
                lenth = len(maj_temp)
                for num in range(0,lenth-2):
                    if maj_temp[num] != 99:
                        if maj_temp[num] +1 not in maj_temp:
                            break
                        if maj_temp[num] + 1 in maj_temp and maj_temp[num] + 2 in maj_temp and maj_temp[num] < 30:
                            syun_remove = maj_temp[num]
                            maj_temp.remove(syun_remove)
                            maj_temp.remove(syun_remove + 1)
                            maj_temp.remove(syun_remove + 2)
                            maj_temp.insert(0,99)
                            maj_temp.insert(0,99)
                            maj_temp.insert(0,99)
                maj_temp = [num for num in maj_temp if num != 99]
                if not maj_temp:
                    agari_type = "mentsu"
        return agari_type
    
    #判断染手
    def Judge_Somete(maj):
        somete = ""
        z = Dazi_Calc.Maj_GetZ(maj)
        m = Dazi_Calc.Maj_GetM(maj)
        s = Dazi_Calc.Maj_GetS(maj)
        p = Dazi_Calc.Maj_GetP(maj)
        if len(maj) == len(z):
            somete = "tsuiso"
        elif len(maj) == len(z) +len(m) or  len(maj) == len(z) +len(s) or  len(maj) == len(z) +len(p):
            somete = "koniso"
            if len(maj) == len(m) or len(maj) == len(s) or len(maj) == len(p):
                somete = "chiniso"
        return somete

    #判断老头
    def Judge_Laotou(maj):
        laotou = ""
        l = Dazi_Calc.Maj_GetL(maj)
        if len(l) == len(maj):
            z = Dazi_Calc.Maj_GetZ(maj)
            if not z:
                laotou = "chinlaotou"
            else:
                laotou = "konlaotou"
        return laotou
        
      

#负责输入输出的类     
class Tenpai_Calc:
    #(3n+1)张牌的待张计算
    def Tenpai_Machi(maj):
        machi_list = []
        for num in maj_list:
            maj_temp = []
            maj_temp += maj
            maj_temp.append(num)
            if Dazi_Calc.Maj_Agari(maj_temp) == True:
                machi_list.append(num)
        return machi_list
    
    #(3n+2)张牌的何切计算
    def Nani_Giru(maj):
        kire_list = list(set(maj))
        kiru_list = {}
        for num in kire_list:
            maj_temp = []
            maj_temp += maj
            maj_temp.remove(num)
            tenpai_list = Tenpai_Calc.Tenpai_Machi(maj_temp)
            if tenpai_list != []:
                kiru_list[num] = tenpai_list
        return kiru_list

    #算番，maj为待张型，income为待牌
    def Han_Calc(maj,income):
        han = 0
        fu = 20
        yaku = []
        yakuman = []
        maj.append(income)
        if Dazi_Calc.Maj_Agari(maj) == True:
            maj = Dazi_Calc.Tenpai_Arrange(maj)
            agari_type = Han_Judge.Judge_Type(maj,income_maj)
            if agari_type == "kokushi":
                han += 1000
                fu += 5
                yakuman.append("国士无双")
                print(yakuman)
            elif agari_type == "kokushi_13":
                han += 2000
                fu += 5
                yakuman.append("国士无双十三面")
            elif agari_type == "7_tai":
                han += 2
                fu = 25
                yaku.append("七对子")
                somete = Han_Judge.Judge_Somete(maj)
                if somete == "tsuiso":
                    han += 1000
                    yakuman.append("字一色")
                if somete == "koniso":
                    han += 3
                    yaku.append("混一色")
                if somete == "chiniso":
                    han += 6
                    yaku.append("清一色")
                laotou = Han_Judge.Judge_Laotou(maj)
                if laotou == "konlaotou":
                    han += 2
                    yaku.append("混老头")
        else:
            han = 0
            fu = 0
        if yakuman != []:
            yaku = []
            yaku += yakuman
        return han,fu,yaku
        



    
total = Tenpai_Calc.Han_Calc(raw_maj,income_maj)
print(total)

#kiru = Tenpai_Calc.Nani_Giru(raw_maj)
#print(kiru)




