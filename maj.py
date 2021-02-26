#所有牌的编码
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白

#输入实例
raw_maj = [2,2,2,3,5]
print(raw_maj)

#数搭子
class Dazi_Clac:

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
        c = Dazi_Clac.Tenpai_Arrange(maj)
        maj_jyan = Dazi_Clac.Maj_GetJyan(maj)
        if len(maj_jyan) == 7:
           agari = True
        elif len(maj_jyan) != 0:
            #雀头为1时检查国土
            if  len(maj_jyan) == 1:
                agari = True
                for num in yaocyu_list:
                    if num not in maj:
                        agari = False
                        break
            for jyan_num in maj_jyan:
                maj_temp = []
                maj_temp += maj
                maj_temp.remove(maj[jyan_num])
                maj_temp.remove(maj[jyan_num])
                lenth = len(maj_temp)
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
                maj_temp = [num for num in maj_temp if num != 99]
                if not maj_temp:
                    agari = True
                    break
                else:
                    agari = False
        else:
            agari = False
        return agari

           
class Tenpai_Clac:
#13张牌的待张计算  
    def Tenpai_Machi(maj):
        machi_list = []
        for num in maj_list:
            maj_temp = []
            maj_temp += maj
            maj_temp.append(num)
            if Dazi_Clac.Maj_Agari(maj_temp) == True:
                machi_list.append(num)
        return machi_list
    
#14张牌的何切计算
    def Nani_Giru(maj):
        kire_list = list(set(maj))
        kiru_list = {}
        for num in kire_list:
            maj_temp = []
            maj_temp += maj
            maj_temp.remove(num)
            tenpai_list = Tenpai_Clac.Tenpai_Machi(maj_temp)
            if tenpai_list != []:
                kiru_list[num] = tenpai_list
        return kiru_list




kiru = Tenpai_Clac.Nani_Giru(raw_maj)

print("切牌种类：\n" + str(kiru))
