#所有牌的编码
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
ryu_list = [12,13,14,16,18,36]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白


#输入实例，规范化输入由前端完成
raw_maj = [3,3,3,4,4,5,5]
income_maj = 5
tsumo = True
#四副露列表，第一个元素代表副露种类，0为无，1为顺子，2为刻子，3为杠，4为暗杠，第二个元素代表副露牌，顺子情况下以顺子起点牌计算
fulu = {1:[0,0], 2:[0,0], 3:[4,7], 4:[4,8]}
print("手牌"+ str(raw_maj))
print("进张" + str(income_maj))
print("自摸" + str(tsumo)) 




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
                    agari_type = "2_pai"
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

    #判断一杯口
    def Judge_1pai(syun,menchin,agari_type):
        pai = False
        if len(list(set(syun))) != len(syun) and agari_type != "2_pai" and menchin == True:
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
            print(anko)
            if anko == 3:
                anko_type = "sananko"
            if anko == 4:
                if income in ko:
                    anko_type = "suanko"
                else:
                    anko_type = "4_tan"
                    
        return anko_type
            
            

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
    def Han_Calc(maj,income,fulu,tsumo):
        han = 0
        fu = 20
        yaku = []
        yakuman = []
        maj.append(income)
        if Dazi_Calc.Maj_Agari(maj) == True:
            maj = Dazi_Calc.Tenpai_Arrange(maj)
            agari_type = Han_Judge.Judge_Type(maj,income)
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
                print("副露顺子(起点)" + str(syun), "副露刻子" + str(ko), "其中杠为" + str(kan),"门清" + str(menchin))
                #所有牌种类带来的加番写在这里
                if agari_type == "2_pai" and menchin == True:
                    han += 3
                    yaku.append("二杯口")
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
                        han +=1
                        yaku.append("断幺九")
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
                        if len(syun_temp) == 4 and menchin == True:
                            if income in syun_temp or income -2 in syun_temp:
                                han_temp +=1
                                yaku_temp.append("平胡")
                        if Han_Judge.Judge_1pai(syun_temp,menchin,agari_type) == True:
                            han_temp += 1
                            yaku_temp.append("一杯口")
                        if Han_Judge.Judge_Taitai(ko_temp) == True:
                            han_temp += 2
                            yaku_temp.append("对对和")
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
                            
                        #选取番数最高的一面返回
                        if han_temp > han_temp_higher:
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
        if yakuman != []:
            yaku = []
            yaku += yakuman
        return han,fu,yaku
        



    
total = Tenpai_Calc.Han_Calc(raw_maj,income_maj,fulu,tsumo)
print(total)

#kiru = Tenpai_Calc.Nani_Giru(raw_maj)
#print(kiru)




