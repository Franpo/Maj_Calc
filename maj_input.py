from maj import *
import re

#所有牌的编码，固定内容
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
ryu_list = [12,13,14,16,18,36]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白



maj = "2233334444556s 自摸6s"

class Maj_Convert:
    def Char_Convert(maj):
        maj_dict = {"raw_maj":[],"income_maj":99,"weather":31,"menfu":31,"dora":0,"additional_yaku":[]}
        fulu = {1:[0,0],2:[0,0],3:[0,0],4:[0,0]}
        additional_yaku = []
        result = ""
        m = re.findall("(?<!吃|碰|杠|和|摸|进|恰)\d+(?=m)", maj)
        m_all = ""
        for num in m:
            m_all += str(num)
        s = re.findall("(?<!吃|碰|杠|和|摸|进|恰)\d+(?=s)", maj)
        s_all = ""
        for num in s:
            s_all += str(num)        
        p = re.findall("(?<!吃|碰|杠|和|摸|进|恰)\d+(?=p)", maj)
        p_all = ""
        for num in p:
            p_all += str(num)
        z = re.findall("(?<!风|摸|和|进|碰|杠|一)(东|南|西|北|中|发|白)", maj)          
        m = list(m_all)
        s = list(s_all)
        p = list(p_all)
        raw_maj = []
        for num in m:
            raw_maj.append(int(num))
        for num in s:
            raw_maj.append(int(num)+10)
        for num in p:
            raw_maj.append(int(num)+20)
        for num in z:
            if num == "东":
                raw_maj.append(31)
            if num == "南":
                raw_maj.append(32)
            if num == "西":
                raw_maj.append(33)
            if num == "北":
                raw_maj.append(34)
            if num == "中":
                raw_maj.append(35)
            if num == "发":
                raw_maj.append(36)
            if num == "白":
                raw_maj.append(37)
        raw_maj = Dazi_Calc.Tenpai_Arrange(raw_maj)
        income_maj = 0
        if re.findall("(?<=荣|摸|和|进)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj):
            income = re.findall("(?<=荣|摸|和|进)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj)[0]
            if income == "东":
                income_maj = 31
            if income == "南":
                income_maj = 32
            if income == "西":
                income_maj = 33
            if income == "北":
                income_maj = 34
            if income == "中":
                income_maj = 35
            if income == "发":
                income_maj = 36
            if income == "白":
                income_maj = 37
            if re.findall("\d(?=m)", income):
                income_maj = int(re.findall("\d(?=m)", income)[0])
            if re.findall("\d(?=s)", income):
                income_maj = int(re.findall("\d(?=s)", income)[0]) + 10
            if re.findall("\d(?=p)", income):
                income_maj = int(re.findall("\d(?=p)", income)[0]) + 20
        weather = 31
        menfu = 31
        if re.findall("(?<=场风)(.)", maj):
            if re.findall("(?<=场风)(.)", maj)[0] == "东":
                weather = 31
            elif re.findall("(?<=场风)(.)", maj)[0] == "南":
                weather = 32
            elif re.findall("(?<=场风)(.)", maj)[0] == "西":
                weather = 33
            elif re.findall("(?<=场风)(.)", maj)[0] == "北":
                weather = 34
        if re.findall("(?<=自风|门风)(.)", maj):
            if re.findall("(?<=自风|门风)(.)", maj)[0] == "东":
                menfu = 31
            elif re.findall("(?<=自风|门风)(.)", maj)[0] == "南":
                menfu = 32
            elif re.findall("(?<=自风|门风)(.)", maj)[0] == "西":
                menfu = 33
            elif re.findall("(?<=自风|门风)(.)", maj)[0] == "北":
                menfu = 34
        dora = 0
        if re.findall("(?<=dora)\d+", maj):
            dora += int(re.findall("(?<=dora)\d+", maj)[0])
        if dora > 200:
            dora = 200
            
        #明杠副露
        meikan = []
        if re.findall("(?<!暗杠)(?<=杠)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj):
            meikan_list = re.findall("(?<!暗杠)(?<=杠)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj)
            for num in range(0,len(meikan_list)):
                if meikan_list[num] == "东":
                    meikan.append(31)
                if meikan_list[num] == "南":
                    meikan.append(32)
                if meikan_list[num] == "西":
                    meikan.append(33)
                if meikan_list[num] == "北":
                    meikan.append(34)
                if meikan_list[num] == "中":
                    meikan.append(35)
                if meikan_list[num] == "发":
                    meikan.append(36)
                if meikan_list[num] == "白":
                    meikan.append(37)
                if re.findall("\d(?=m)", meikan_list[num]):
                    meikan.append(int(re.findall("\d(?=m)", meikan_list[num])[0]))
                if re.findall("\d(?=s)", meikan_list[num]):
                    meikan.append(int(re.findall("\d(?=s)", meikan_list[num])[0]) + 10)
                if re.findall("\d(?=p)", meikan_list[num]):
                    meikan.append(int(re.findall("\d(?=p)", meikan_list[num])[0]) + 20)

        #暗杠副露
        ankan = []
        if re.findall("(?<=暗杠)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj):
            ankan_list = re.findall("(?<=暗杠)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj)
            for num in range(0,len(ankan_list)):
                if ankan_list[num] == "东":
                    ankan.append(31)
                if ankan_list[num] == "南":
                    ankan.append(32)
                if ankan_list[num] == "西":
                    ankan.append(33)
                if ankan_list[num] == "北":
                    ankan.append(34)
                if ankan_list[num] == "中":
                    ankan.append(35)
                if ankan_list[num] == "发":
                    ankan.append(36)
                if ankan_list[num] == "白":
                    ankan.append(37)
                if re.findall("\d(?=m)", ankan_list[num]):
                    ankan.append(int(re.findall("\d(?=m)", ankan_list[num])[0]))
                if re.findall("\d(?=s)", ankan_list[num]):
                    ankan.append(int(re.findall("\d(?=s)", ankan_list[num])[0]) + 10)
                if re.findall("\d(?=p)", ankan_list[num]):
                    ankan.append(int(re.findall("\d(?=p)", ankan_list[num])[0]) + 20)

        #明刻副露
        meiko = []
        if re.findall("(?<=碰)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj):
            meiko_list = re.findall("(?<=碰)(东|南|西|北|中|发|白|\dm|\ds|\dp)", maj)
            for num in range(0,len(meiko_list)):
                if meiko_list[num] == "东":
                    meiko.append(31)
                if meiko_list[num] == "南":
                    meiko.append(32)
                if meiko_list[num] == "西":
                    meiko.append(33)
                if meiko_list[num] == "北":
                    meiko.append(34)
                if meiko_list[num] == "中":
                    meiko.append(35)
                if meiko_list[num] == "发":
                    meiko.append(36)
                if meiko_list[num] == "白":
                    meiko.append(37)
                if re.findall("\d(?=m)", meiko_list[num]):
                    meiko.append(int(re.findall("\d(?=m)", meiko_list[num])[0]))
                if re.findall("\d(?=s)", meiko_list[num]):
                    meiko.append(int(re.findall("\d(?=s)", meiko_list[num])[0]) + 10)
                if re.findall("\d(?=p)", meiko_list[num]):
                    meiko.append(int(re.findall("\d(?=p)", meiko_list[num])[0]) + 20)
                    
        #顺子副露
        meisyun = []
        if re.findall("(?<=吃|恰)(\dm|\ds|\dp)", maj):
            meisyun_list = re.findall("(?<=吃|恰)(\dm|\ds|\dp)", maj)
            for num in range(0,len(meisyun_list)):
                if re.findall("\d(?=m)", meisyun_list[num]):
                    meisyun.append(int(re.findall("\d(?=m)", meisyun_list[num])[0]))
                if re.findall("\d(?=s)", meisyun_list[num]):
                    meisyun.append(int(re.findall("\d(?=s)", meisyun_list[num])[0]) + 10)
                if re.findall("\d(?=p)", meisyun_list[num]):
                    meisyun.append(int(re.findall("\d(?=p)", meisyun_list[num])[0]) + 20)
        maj_all = []
        maj_all += raw_maj
        for num in meikan:
            maj_all.append(num)
            maj_all.append(num)
            maj_all.append(num)
            maj_all.append(num)
        for num in ankan:
            maj_all.append(num)
            maj_all.append(num)
            maj_all.append(num)
            maj_all.append(num)
        for num in meiko:
            maj_all.append(num)
            maj_all.append(num)
            maj_all.append(num)
        for num in meisyun:
            maj_all.append(num)
            maj_all.append(num+1)
            maj_all.append(num+2)
        maj_all.append(income_maj)
        maj_all = Dazi_Calc.Tenpai_Arrange(maj_all)
        for num in maj_all:
            if num not in maj_list:
                result += "输入不合法！"
                break
        if len(maj_all) -len(meikan) -len(ankan) !=14 and result == "":
            result += "和牌也要讲究基本法，您输入的牌数量不对。"
        lenth = len(maj_all)
        for num in range(0,lenth-4):
            if maj_all[num] == maj_all[num+4]:
                result += "您的牌型中包含大量重复牌，系统提醒您，文明麻将，请勿印牌。"
                break
        tsumo_count = 0
        ron_count = 0        
        if re.findall("天和", maj):
            additional_yaku.append("天和")
            tsumo_count += 1
        if re.findall("立直", maj) and not re.findall("两立直", maj):
            additional_yaku.append("立直")
        if re.findall("地和", maj):
            additional_yaku.append("地和")
            tsumo_count += 1
        if re.findall("海底", maj):
            additional_yaku.append("海底摸月")
            tsumo_count += 1
        if re.findall("一发", maj):
            additional_yaku.append("一发")
        if re.findall("河底", maj):
            additional_yaku.append("河底捞鱼")
            ron_count += 1
        if re.findall("岭上", maj):
            additional_yaku.append("岭上开花")
            tsumo_count += 1
        if re.findall("两立直", maj):
            additional_yaku.append("两立直")
        if re.findall("枪杠", maj):
            additional_yaku.append("枪杠")
            ron_count += 1
        if re.findall("(?<!天|地)(荣|和)", maj):
            additional_yaku.append("荣和")
            ron_count += 1
        if re.findall("自摸", maj):
            additional_yaku.append("自摸")
            tsumo_count += 1
        if tsumo_count != 0 and ron_count !=0 and result == "":
            result += "您输入的附加信息中包含冲突内容，请检查后重新输入。"        
        maj_dict["raw_maj"] = raw_maj
        maj_dict["income_maj"] = income_maj
        maj_dict["weather"] = weather
        maj_dict["menfu"] = menfu
        maj_dict["dora"] = dora
        maj_dict["additional_yaku"] = additional_yaku
        count = 1
        for num in range(0,len(ankan)):
            fulu[count] = [4,ankan[num]]
            count += 1
        for num in range(0,len(meikan)):
            fulu[count] = [3,meikan[num]]
            count += 1
        for num in range(0,len(meiko)):
            fulu[count] = [2,meiko[num]]
            count += 1
        for num in range(0,len(meisyun)):
            fulu[count] = [1,meisyun[num]]
            count += 1
        if result == "":
            result_calc = Tenpai_Calc.Point_Calc(maj_dict,fulu)
            result += result_calc
        print(fulu)
        return result


 

maj = Maj_Convert.Char_Convert(maj)
print(maj)



