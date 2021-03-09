import math
#所有牌的编码，固定内容
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
ryu_list = [12,13,14,16,18,36]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白


#输入实例，规范化输入由前端完成。必须传入的字典包含：一副手牌，进张牌，场风，自风。以及副露以字典形式传入。可能的信息以列表形式传入，如天和，立直，自摸，一发，海底捞等
#input_maj = {"raw_maj":[1,1,1,2,3,4,5,6,7,8,9,9,9],"income_maj":3,"weather":31,"menfu":32,"dora":2,"additional_yaku":["天和"]}

#四副露列表，第一个元素代表副露种类，0为无，1为顺子，2为刻子，3为杠，4为暗杠，第二个元素代表副露牌，顺子情况下以顺子起点牌计算
#fulu = {1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0]}



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
    
    #绿一色
    def Maj_GetRyu(maj):
        maj_r = []
        for num in maj:
            if num in ryu_list:
                maj_r.append(num)
        return maj_r
    
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
    def Judge_Somete(maj,syun,ko):
        somete = ""
        maj_temp = []
        for num in maj:
            maj_temp.append(num)
        for num in syun:
            maj_temp.append(num)
        for num in ko:
            maj_temp.append(num)
        z = Dazi_Calc.Maj_GetZ(maj_temp)
        m = Dazi_Calc.Maj_GetM(maj_temp)
        s = Dazi_Calc.Maj_GetS(maj_temp)
        p = Dazi_Calc.Maj_GetP(maj_temp)
        if len(maj_temp) == len(z):
            somete = "tsuiso"
        elif len(maj_temp) == len(z) +len(m) or  len(maj_temp) == len(z) +len(s) or  len(maj_temp) == len(z) +len(p):
            somete = "koniso"
            if len(maj_temp) == len(m) or len(maj_temp) == len(s) or len(maj_temp) == len(p):
                somete = "chiniso"
        return somete

    #判断老头
    def Judge_Laotou(maj,syun,ko):
        laotou = ""
        maj_temp = []
        for num in maj:
            maj_temp.append(num)
        for num in ko:
            maj_temp.append(num)
        l = Dazi_Calc.Maj_GetL(maj_temp)
        if len(l) == len(maj_temp):
            z = Dazi_Calc.Maj_GetZ(maj_temp)
            if not z:
                laotou = "chinlaotou"
            else:
                laotou = "konlaotou"
        if syun != []:
            laotou = ""
        return laotou
    
    #判断绿一色
    def Judge_Ryu(maj,syun,ko):
        maj_temp = []
        for num in maj:
            maj_temp.append(num)
        for num in ko:
            maj_temp.append(num)
        for num in syun:
            maj_temp.append(num)
            maj_temp.append(num+1)
            maj_temp.append(num+2)
        ryu = Dazi_Calc.Maj_GetRyu(maj_temp)
        if len(ryu) == len(maj_temp):
            return True
        else:
            return False
        
    #判断断幺
    def Judge_Tanyao(maj,syun,ko):
        maj_temp = []
        tanyao = True
        for num in maj:
            maj_temp.append(num)
        for num in ko:
            maj_temp.append(num)
        for num in syun:
            maj_temp.append(num)
            maj_temp.append(num+1)
            maj_temp.append(num+2)
        for num in maj_temp:
            if num in yaocyu_list:
                tanyao = False
                break
        return tanyao

    #判断九莲
    def Judge_Cyuren(maj,income):
        cyuren = ""
        for num in maj:
            maj_temp =[]
            maj_temp += maj
            maj_temp.remove(num)
            if len(Tenpai_Calc.Tenpai_Machi(maj_temp)) == 9:
                maj.remove(income)
                if len(Tenpai_Calc.Tenpai_Machi(maj)) == 9:
                    cyuren = "cyuren_9"
                else:
                    cyuren = "cyuren"
                break
        return cyuren 

    #判断一杯口
    def Judge_1pai(syun,menchin,agari_type):
        pai = False
        if len(list(set(syun))) != len(syun) and menchin == True:
            pai = True
        return pai

    #判断二杯口
    def Judge_2pai(syun,menchin,agari_type):
        pai = False
        if len(list(set(syun))) +2 == len(syun) and menchin == True:
            pai = True
        return pai
    
    #判断对对和
    def Judge_Taitai(ko):
        taitai = False
        if len(ko) == 4:
            taitai = True
        return taitai
    
    #判断暗刻
    def Judge_Anko(ko,fulu_ko,ankan,income,tsumo):
        anko_type = ""
        anko = 0
        if len(ko) >= 3:
            anko = len(ko) - len(fulu_ko) + len(ankan)
            if not tsumo and income in ko:
                anko -= 1
            if anko == 3:
                anko_type = "sananko"
            if anko == 4:
                if income in ko:
                    anko_type = "suanko"
                else:
                    anko_type = "4_tan"      
        return anko_type
    
    #判断场风役
    def Judge_Weather(ko,weather):
        weatheryaku = ""
        if weather in ko:
            weatheryaku += "场风："
            if weather == 31:
                weatheryaku += "东"
            if weather == 32:
                weatheryaku += "南"
            if weather == 33:
                weatheryaku += "西"
            if weather == 34:
                weatheryaku += "北"
        return weatheryaku
    
    #判断门风役
    def Judge_Menfu(ko,menfu):
        menfuyaku = ""
        if menfu in ko:
            menfuyaku += "门风："
            if menfu == 31:
                menfuyaku += "东"
            if menfu == 32:
                menfuyaku += "南"
            if menfu == 33:
                menfuyaku += "西"
            if menfu == 34:
                menfuyaku += "北"
        return menfuyaku
    
    #判断四喜和
    def Judge_Sushi(ko,jyan):
        sushi = ""
        if 31 in ko and 32 in ko and 33 in ko and 34 in ko:
            sushi = "dai"
        elif 31 in ko and 32 in ko and 33 in ko and jyan == 34:
            sushi = "syou"
        elif 31 in ko and 32 in ko and 34 in ko and jyan == 33:
            sushi = "syou"
        elif 31 in ko and 33 in ko and 34 in ko and jyan == 32:
            sushi = "syou"
        elif 32 in ko and 33 in ko and 34 in ko and jyan == 31:
            sushi = "syou"
        return sushi
    
    #判断三元和
    def Judge_Sangen(ko,jyan):
        sangen = ""
        if 35 in ko and 36 in ko and 37 in ko:
            sangen = "dai"
        elif 35 in ko and 36 in ko and jyan == 37:
            sangen = "syou"
        elif 35 in ko and 37 in ko and jyan == 36:
            sangen = "syou"
        elif 36 in ko and 37 in ko and jyan == 35:
            sangen = "syou"
        return sangen
    
    #判断三色同顺
    def Judge_Sansyoku(syun):
        sansyoku = False
        syun = Dazi_Calc.Tenpai_Arrange(syun)
        for num in syun:
            if num + 10 in syun and num + 20 in syun:
                sansyoku = True
                break
        return sansyoku

    #判断三色同刻
    def Judge_Douko(ko):
        douko = False
        ko = Dazi_Calc.Tenpai_Arrange(ko)
        for num in ko:
            if num + 10 in ko and num + 20 in ko and num + 20 < 30:
                douko = True
                break
        return douko
    
    #判断全带幺
    def Judge_Cyanta(syun,ko,jyan):
        cyanta = "jyuncyan"
        for num in syun:
            if num not in [1,7,11,17,21,27]:
                cyanta = ""
                break
        for num in ko:
            if num not in [1,9,11,19,21,29,31,32,33,34,35,36,37]:
                cyanta = ""
                break
        if jyan not in [1,9,11,19,21,29,31,32,33,34,35,36,37]:
            cyanta = ""
        if cyanta == "jyuncyan":
            for num in ko:
                if num in [31,32,33,34,35,36,37]:
                    cyanta = "cyanta"
                    break
            if jyan in [31,32,33,34,35,36,37]:
                cyanta = "cyanta"
        return cyanta
        
                       

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
    def Han_Calc(maj,income,fulu,tsumo,weather,menfu):
        han = 0
        fu = 20
        agari_type = ""
        yaku = []
        yakuman = []
        maj.append(income)
        if Dazi_Calc.Maj_Agari(maj) == True:
            maj = Dazi_Calc.Tenpai_Arrange(maj)
            agari_type = Han_Judge.Judge_Type(maj,income)
            if agari_type == "kokushi":
                han += 1000
                fu = 25
                yakuman.append("国士无双")
            elif agari_type == "kokushi_13":
                han += 2000
                fu = 25
                yakuman.append("国士无双十三面")
            elif agari_type == "7_tai":
                han += 2
                fu = 25
                yaku.append("七对子")
                if tsumo == True:
                    han += 1
                    yaku.append("门前清自摸和")
                somete = Han_Judge.Judge_Somete(maj,[],[])
                if somete == "tsuiso":
                    han += 1000
                    yakuman.append("字一色")
                if somete == "koniso":
                    han += 3
                    yaku.append("混一色")
                if somete == "chiniso":
                    han += 6
                    yaku.append("清一色")
                laotou = Han_Judge.Judge_Laotou(maj,[],[])
                if laotou == "konlaotou":
                    han += 2
                    yaku.append("混老头")
            else:
                syun = []
                ko = []
                kan = []
                ankan = []
                #门清判定，副露注册
                menchin = True
                for n in range(1,5):
                    fulu_temp = fulu[n]
                    if fulu_temp[0] == 1:
                        syun.append(fulu_temp[1])
                        menchin = False
                    elif fulu_temp[0] == 2:
                        ko.append(fulu_temp[1])
                        menchin = False
                    elif fulu_temp[0] == 3:
                        ko.append(fulu_temp[1])
                        kan.append(fulu_temp[1])
                        menchin = False
                    elif fulu_temp[0] == 4:
                        ko.append(fulu_temp[1])
                        kan.append(fulu_temp[1])
                        ankan.append(fulu_temp[1])
                #所有牌种类带来的加番写在这里
                if menchin == True and tsumo == True:
                    han += 1
                    yaku.append("门前清自摸和")
                somete = Han_Judge.Judge_Somete(maj,syun,ko)
                if somete == "tsuiso":
                    han += 1000
                    yakuman.append("字一色")
                if somete == "koniso":
                    if menchin == True:
                        han += 3
                    else:
                        han += 2
                    yaku.append("混一色")
                if somete == "chiniso":
                    if menchin == True:
                        han += 6
                    else:
                        han += 5
                    yaku.append("清一色")
                laotou = Han_Judge.Judge_Laotou(maj,syun,ko)
                if laotou == "konlaotou":
                    han += 2
                    yaku.append("混老头")
                if laotou == "chinlaotou":
                    han += 1000
                    yakuman.append("清老头")
                if somete == "koniso" or somete == "chiniso":
                    if Han_Judge.Judge_Ryu(maj,syun,ko) == True:
                        han += 1000
                        yakuman.append("绿一色")
                if Han_Judge.Judge_Tanyao(maj,syun,ko) == True:
                    #if menchin == True:   食断
                        han += 1
                        yaku.append("断幺九")
                cyuren = Han_Judge.Judge_Cyuren(maj,income)
                if cyuren == "cyuren":
                    han += 1000
                    yakuman.append("九莲宝灯")
                if cyuren == "cyuren_9":
                    han += 2000
                    yakuman.append("纯正九莲宝灯")
                if len(kan) == 3:
                    han += 2
                    yaku.append("三杠子")
                if len(kan) == 4:
                    han += 1000
                    yakuman.append("四杠子")

                #同一组牌选取不同牌为雀头时，可能出现符数和番数变化，取最高者
                han_temp_higher = 0
                fu_temp_higher = 0
                yaku_temp_higher = []
                yakuman_temp_higher = []
                
                #仿和了判定，穷举雀头
                maj_jyan = Dazi_Calc.Maj_GetJyan(maj)
                for num in maj_jyan:
                    jyan_temp = maj[num]
                    maj_temp = []
                    maj_temp += maj
                    maj_temp.remove(maj[num])
                    maj_temp.remove(maj[num])
                    lenth = len(maj_temp)
                    syun_temp = []
                    ko_temp = []
                    syun_temp += syun
                    ko_temp += ko
                    for num in range(0,lenth-2):
                        #照和了判定抄的，懒得模块化了，这也太长了orz
                        if maj_temp[num] != 99:
                            if maj_temp[num] != maj_temp[num+1] and maj_temp[num] +1 not in maj_temp:
                                break
                            if maj_temp[num] == maj_temp[num+1] and maj_temp[num] == maj_temp[num+2]:
                                ko_temp.append(maj_temp[num])
                                maj_temp[num] = 99
                                maj_temp[num+1] = 99
                                maj_temp[num+2] = 99
                            if maj_temp[num] + 1 in maj_temp and maj_temp[num] + 2 in maj_temp and maj_temp[num] < 30:
                                syun_remove = maj_temp[num]
                                syun_temp.append(maj_temp[num])
                                maj_temp.remove(syun_remove)
                                maj_temp.remove(syun_remove + 1)
                                maj_temp.remove(syun_remove + 2)
                                maj_temp.insert(0,99)
                                maj_temp.insert(0,99)
                                maj_temp.insert(0,99)
                    maj_temp = [num for num in maj_temp if num != 99]
                    han_temp = 0
                    fu_temp = 0
                    yaku_temp = []
                    yakuman_temp = []
                    if not maj_temp:
                        #所有面子引发的加番写在这里
                        if len(syun_temp) == 4 and menchin == True and jyan_temp != weather and jyan_temp != menfu and jyan_temp not in [35,36,37]:
                            for num in syun_temp:
                                if income == num or income -2 == num:
                                    #12居然不听0，麻将，很奇妙吧
                                    if num in [1,1,21] and income in [3,13,23]:
                                        None
                                    elif num in [7,17,27] and income in [7,17,27]:
                                        None
                                    else:
                                        han_temp +=1
                                        yaku_temp.append("平和")
                                        break
                        if Han_Judge.Judge_2pai(syun_temp,menchin,agari_type) == True:
                            han_temp += 3
                            yaku_temp.append("二杯口")
                        if Han_Judge.Judge_1pai(syun_temp,menchin,agari_type) == True and Han_Judge.Judge_2pai(syun_temp,menchin,agari_type) == False:
                            han_temp += 1
                            yaku_temp.append("一杯口")
                        if Han_Judge.Judge_Taitai(ko_temp) == True:
                            han_temp += 2
                            yaku_temp.append("对对和")
                        #暗刻型判定
                        anko = Han_Judge.Judge_Anko(ko_temp,ko,ankan,income,tsumo)
                        if anko == "sananko":
                            han_temp += 2
                            yaku_temp.append("三暗刻")
                        if anko == "suanko":
                            han_temp += 1000
                            yakuman_temp.append("四暗刻")
                        if anko == "4_tan":
                            han_temp += 2000
                            yakuman_temp.append("四暗刻单骑")
                        #门风场风判定
                        weatheryaku = Han_Judge.Judge_Weather(ko_temp,weather)
                        if weatheryaku != "":
                            han_temp += 1
                            yaku_temp.append(weatheryaku)
                        menfuyaku = Han_Judge.Judge_Menfu(ko_temp,menfu)
                        if menfuyaku != "":
                            han_temp += 1
                            yaku_temp.append(menfuyaku)
                        #四喜和判定
                        sushi = Han_Judge.Judge_Sushi(ko_temp,jyan_temp)
                        if sushi == "syou":
                            han_temp += 1000
                            yakuman_temp.append("小四喜")
                        if sushi == "dai":
                            han_temp += 2000
                            yakuman_temp.append("大四喜")
                        #役牌判定
                        if 35 in ko_temp:
                            han_temp += 1
                            yaku_temp.append("役牌：中")
                        if 36 in ko_temp:
                            han_temp += 1
                            yaku_temp.append("役牌：发")
                        if 37 in ko_temp:
                            han_temp += 1
                            yaku_temp.append("役牌：白")
                        #三元和判定
                        sangen = Han_Judge.Judge_Sangen(ko_temp,jyan_temp)
                        if sangen == "syou":
                            han_temp += 2
                            yaku_temp.append("小三元")
                        if sangen == "dai":
                            han_temp += 1000
                            yakuman_temp.append("大三元")
                        #三色同顺判定
                        if Han_Judge.Judge_Sansyoku(syun_temp) == True:
                            if menchin == True:
                                han_temp += 2
                            else:
                                han_temp += 1
                            yaku_temp.append("三色同顺")
                        #三色同刻判定
                        if Han_Judge.Judge_Douko(ko_temp) == True:
                            han_temp +=2
                            yaku_temp.append("三色同刻")
                        #沙雕役判定
                        cyanta = Han_Judge.Judge_Cyanta(syun_temp,ko_temp,jyan_temp)
                        if cyanta == "cyanta":
                            if laotou != "konlaotou":
                                if menchin == True:
                                    han_temp += 2
                                else:
                                    han_temp += 1
                                yaku_temp.append("混全带幺九")
                        if cyanta == "jyuncyan":
                            #这种奇怪的判定真的有必要写吗
                            if laotou != "chinlaotou":
                                if menchin == True:
                                    han_temp += 3
                                else:
                                    han_temp += 2
                                yaku_temp.append("纯全带幺九")
                        #算符
                        anko_count = [num for num in ko_temp if num not in ko]
                        if income in anko_count and tsumo == False:
                            anko_count.remove(income)
                        meiko_count = []
                        for num in ko_temp:
                            if num not in anko_count and num not in kan:
                                meiko_count.append(num)
                        ankan_count = ankan
                        meikan_count = [num for num in kan if num not in ankan]
                        #刻杠加符
                        for num in anko_count:
                            if num in yaocyu_list:
                                fu_temp += 8
                            else:
                                fu_temp += 4
                        for num in meiko_count:
                            if num in yaocyu_list:
                                fu_temp += 4
                            else:
                                fu_temp += 2
                        for num in ankan_count:
                            if num in yaocyu_list:
                                fu_temp += 32
                            else:
                                fu_temp += 16
                        for num in meikan_count:
                            if num in yaocyu_list:
                                fu_temp += 16
                            else:
                                fu_temp += 8
                        #雀头加符
                        if jyan_temp == weather:
                            fu_temp += 2
                        if jyan_temp == menfu:
                            fu_temp += 2
                        if jyan_temp in [35,36,37]:
                            fu_temp += 2
                        #门清食和加符
                        if tsumo == False and menchin == True:
                            fu_temp +=10
                        #自摸加符
                        if tsumo == True and "平和" not in yaku_temp:
                            fu_temp += 2
                        #单钓，边张，坎张加符
                        if "平和" not in yaku_temp:
                            if income == jyan_temp:
                                fu_temp += 2
                            elif income - 2 in syun_temp and income in [3,13,23]:
                                fu_temp += 2
                            elif income in syun_temp and income in [7,17,27]:
                                fu_temp += 2
                            elif income - 1 in syun_temp:
                                fu_temp += 2
                            elif menchin == False and len(syun_temp) == 4 and tsumo == False:
                                fu_temp += 2
                        #选取番数最高的一面返回
                        if han_temp > han_temp_higher:
                            han_temp_higher = han_temp
                            fu_temp_higher = fu_temp
                            yaku_temp_higher = yaku_temp
                            yakuman_temp_higher = yakuman_temp
                        elif han_temp == han_temp_higher and fu_temp > fu_temp_higher:
                            han_temp_higher = han_temp
                            fu_temp_higher = fu_temp
                            yaku_temp_higher = yaku_temp
                            yakuman_temp_higher = yakuman_temp
                #结算拆解番符
                han += han_temp_higher
                fu += fu_temp_higher
                yaku += yaku_temp_higher
                yakuman += yakuman_temp_higher
       
                
        else:
            han = 0
            fu = 0
        return han,fu,yaku,yakuman,agari_type

    #算点
    def Point_Calc(input_maj,fulu):
        maj = input_maj["raw_maj"]
        income = input_maj["income_maj"]
        weather = input_maj["weather"]
        menfu = input_maj["menfu"]
        dora = input_maj["dora"]
        additional_yaku = input_maj["additional_yaku"]
        han = 0
        fu = 0
        yaku = []
        yakuman = []
        if "立直" in additional_yaku:
            han += 1
            yaku.append("立直")
        if "两立直" in additional_yaku:
            han += 2
            yaku.append("两立直")
        if "一发" in additional_yaku:
            han += 1
            yaku.append("一发")            
        if "海底摸月" in additional_yaku:
            han += 1
            yaku.append("海底摸月")            
        if "河底捞鱼" in additional_yaku:
            han += 1
            yaku.append("河底捞鱼")
            tsumo = False
        if "岭上开花" in additional_yaku:
            han += 1
            yaku.append("岭上开花")
        if "枪杠" in additional_yaku:
            han += 1
            yaku.append("枪杠")
            tsumo = False
        if "天和" in additional_yaku:
            han += 1000
            yakuman.append("天和")            
        if "地和" in additional_yaku:
            han += 1000
            yakuman.append("地和")
        if "自摸" in additional_yaku:
            tsumo = True
        if "荣和" in additional_yaku:
            tsumo = False
        else:
            tsumo = True
        hanfu_list = Tenpai_Calc.Han_Calc(maj,income,fulu,tsumo,weather,menfu)
        han += hanfu_list[0]
        fu += hanfu_list[1]
        yaku += hanfu_list[2]
        yakuman += hanfu_list[3]
        agari_type = hanfu_list[4]
        point = ""
        if agari_type == "mentsu":
            fu = fu / 10
            fu = int(math.ceil(fu))*10
        if fu < 20:
            point = "这副牌不是和了型，请仔细确认。"
        if fu >= 20:
            if not yaku and han < 1000:
                yaku.append("无役")
                point += "有无役怪啊！\n" + str(fu) +"符。"
            else:
                if yakuman != []:
                    yaku = []
                    yaku += yakuman
                if dora >0 and han < 1000:
                    han += dora
                    dora_count = "宝牌：" + str(dora)
                    yaku.append(dora_count)
                if yakuman == []:
                    if menfu == 31:
                        point += "亲"
                    else:
                        point += "子"
                    point += "家的"
                    if tsumo == True:
                        point += "自摸"
                    else:
                        point += "荣"
                    point += "和。\n"
                    point += "番："
                    for x in yaku: 
                        point += str(x) + " "
                    point += "\n"
                    point += str(han) + "番，" + str(fu) + "符。"
                    point += "\n"
                    if han <= 4:
                        basic_point = fu * 2 ** (han + 2)
                        if menfu ==31:
                            basic_point = basic_point *6
                            if tsumo == True:
                                basic_point = int(math.ceil(basic_point/3/100)*100)
                                if basic_point >=12000:
                                    basic_point = 12000
                                    point += "满贯\n"
                                point += "子家各支付:"+ str(basic_point) + "点"
                            else:
                                basic_point_ron = int(math.ceil(basic_point/100)*100)
                                if basic_point_ron >=12000:
                                    basic_point_ron = 12000
                                    point += "满贯\n"
                                point += "放铳者支付:"+ str(basic_point_ron) + "点。" 
                        else:
                            basic_point = basic_point *4
                            if tsumo == True:
                                basic_point = int(math.ceil(basic_point/100)*100)
                                if basic_point >= 8000:
                                    basic_point_oya = 4000
                                    basic_point_other = 2000
                                    point += "满贯\n"
                                else:
                                    basic_point_oya = int(math.ceil(basic_point/2/100)*100)
                                    basic_point_other = int(math.ceil(basic_point/4/100)*100)
                                point += "亲家支付:"+ str(basic_point_oya) + "点，" + "子家各支付:"+ str(basic_point_other) + "点。"
                            else:
                                basic_point_ron = int(math.ceil(basic_point/100)*100)
                                if basic_point_ron >=8000:
                                    basic_point_ron = 8000
                                    point += "满贯\n"
                                point += "放铳者支付:"+ str(basic_point_ron) + "点。"
                    elif han >= 5:
                        basic_point = 8000
                        if menfu == 31:
                            if han == 5:
                                basic_point = 12000
                                point += "满贯\n"
                            elif han in [6,7]:
                                basic_point = 18000
                                point += "跳满\n"
                            elif han in [8,9,10]:
                                basic_point = 24000
                                point += "倍满\n"
                            elif han in [11,12]:
                                basic_point = 36000
                                point += "三倍满\n"
                            else:
                                basic_point = 48000
                                point += "累计役满\n"
                            if tsumo == True:
                                point += "子家各支付:"+ str(int(basic_point/3)) + "点"
                            else:
                                point += "放铳者支付:"+ str(basic_point) + "点。" 
                                
                        else:
                            if han == 5:
                                basic_point = 8000
                                point += "满贯\n"
                            elif han in [6,7]:
                                basic_point = 12000
                                point += "跳满\n"
                            elif han in [8,9,10]:
                                basic_point = 16000
                                point += "倍满\n"
                            elif han in [11,12]:
                                basic_point = 24000
                                point += "三倍满\n"
                            else:
                                basic_point = 32000
                                point += "累计役满\n"
                            if tsumo == True:
                                point += "亲家支付:"+ str(int(basic_point/2)) + "点，" + "子家各支付:"+ str(int(basic_point/4)) + "点。"
                            else:
                                point += "放铳者支付:"+ str(basic_point) + "点。" 
                            
                else:
                    if menfu == 31:
                        point += "亲"
                    else:
                        point += "子"
                    point += "家的"
                    if tsumo == True:
                        point += "自摸"
                    else:
                        point += "荣"
                    point += "和。\n"
                    point += "番："
                    for x in yakuman: 
                        point += str(x) + " "
                    point += "\n"
                    yakuman_bai = int(han/1000)
                    basic_point = 32000
                    if menfu == 31:
                        if yakuman_bai == 1:
                            basic_point = 48000
                            point += "役满\n"
                        elif yakuman_bai == 2:
                            basic_point = 96000
                            point += "两倍役满\n"
                        elif yakuman_bai == 3:
                            basic_point = 144000
                            point += "三倍役满\n"
                        elif yakuman_bai == 4:
                            basic_point = 192000
                            point += "四倍役满\n"
                        elif yakuman_bai == 5:
                            basic_point = 240000
                            point += "五倍役满\n"
                        elif yakuman_bai == 6:
                            basic_point = 288000
                            point += "六倍役满\n"
                        elif yakuman_bai == 7:
                            basic_point = 336000
                            point += "七...倍役满???你在做梦吧？"
                        if tsumo == True:
                            point += "子家各支付:"+ str(int(basic_point/3)) + "点"
                        else:
                            point += "放铳者支付:"+ str(basic_point) + "点。"
                    else:
                        if yakuman_bai == 1:
                            basic_point = 32000
                            point += "役满\n"
                        elif yakuman_bai == 2:
                            basic_point = 64000
                            point += "两倍役满\n"
                        elif yakuman_bai == 3:
                            basic_point = 96000
                            point += "三倍役满\n"
                        elif yakuman_bai == 4:
                            basic_point = 128000
                            point += "四倍役满\n"
                        elif yakuman_bai == 5:
                            basic_point = 160000
                            point += "五倍役满\n"
                        elif yakuman_bai == 6:
                            basic_point = 192000
                            point += "六倍役满\n"
                        elif yakuman_bai == 7:
                            basic_point = 224000
                            point += "七...倍役满???你在做梦吧？"
                        if tsumo == True:
                            point += "亲家支付:"+ str(int(basic_point/2)) + "点，" + "子家各支付:"+ str(int(basic_point/4)) + "点。"
                        else:
                            point += "放铳者支付:"+ str(basic_point) + "点。" 
                        
                        
        return point
            
        
        



    
#point = Tenpai_Calc.Point_Calc(input_maj,fulu)
#print(point)

#kiru = Tenpai_Calc.Nani_Giru(raw_maj)
#print(kiru)




