import cv2
import os
import numpy
import time
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]

class Maj_CV:
    #逐一模板匹配每张牌，返回数量
    def Scan_Maj(rawimage,num):
        path = os.path.join("E:\majcalc\maj")
        maj_code = str(num)+".jpg"
        maj = os.path.join(path,maj_code)
        majimage = cv2.imread(maj)
        theight, twidth = majimage.shape[:2]
        result = cv2.matchTemplate(rawimage,majimage,cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        strmin_val = str(min_val)
        temp_loc = min_loc
        other_loc = min_loc
        if num in [17,19,22,24,25,26,28,29]:
            threshold = 0.05
        elif num == 37:
            threshold = 0.005
        else:
            threshold = 0.025
        loc = numpy.where(result<threshold)
        lenth = len(loc[0])
        if lenth != 0:
            numOfloc = 1
            drawed_list = []
            cv2.rectangle(rawimage,temp_loc,(temp_loc[0]+twidth,temp_loc[1]+theight),(0,0,225),2)
            drawed_list += range(temp_loc[0]-10,temp_loc[0]+10)
            for other_loc in zip(*loc[::-1]):
                if other_loc[0] not in drawed_list:
                    numOfloc = numOfloc + 1
                    cv2.rectangle(rawimage,other_loc,(other_loc[0]+twidth,other_loc[1]+theight),(0,0,225),2)
                    drawed_list += range(other_loc[0]-10,other_loc[0]+10)
        else:
            numOfloc = 0
        return rawimage,numOfloc
    
    #整理手牌列表，返回
    def Collect_Maj(test):
        maj_output = []
        path = os.path.join("E:\majcalc\maj")
        raw = os.path.join(path,"rawimg.jpg")
        rawimage = cv2.imread(raw)
        rawheight, rawwidth = rawimage.shape[:2]
        if rawheight/rawwidth >0.25:
            rawimage = rawimage[max(0,int((1-0.25*rawwidth/rawheight)*rawheight)):rawheight]
        rawimage = Maj_CV.Find_Maj(rawimage)
        if len(rawimage) == 0:
            return "无法识别。"
        for num in maj_list:
            result = Maj_CV.Scan_Maj(rawimage,num)
            rawimage = result[0]
            numOfloc = result[1]
            for i in range(0,numOfloc):
                maj_output.append(num)
        print(maj_output)
        str_numOfloc = str(len(maj_output))
        strText = "MatchResult" + "----NumberOfPosition="+str_numOfloc
        cv2.imshow(strText,rawimage)
        cv2.waitKey()
        cv2.destroyAllWindows()

        #在截图中查找手牌边界
    def Find_Maj(rawimage):
        img_gray = cv2.cvtColor(rawimage.copy(), cv2.COLOR_BGR2GRAY)
        row_pixel_nums = []
        rawheight, rawwidth = rawimage.shape[:2]
        #统计每行的白色像素数量，裁定边界
        for i in range(rawheight):
            whitecount = 0
            for j in range(rawwidth):
                if img_gray[i][j] > 210:
                    whitecount += 1
            if whitecount != 0:
                if rawwidth/whitecount < 8:
                    row_pixel_nums.append(1)
                else:
                    row_pixel_nums.append(0)
            else:
                row_pixel_nums.append(0)
        lenth = len(row_pixel_nums)
        limit1 = -1
        limit2 = -1
        for i in range(lenth-1,0,-1):
            if row_pixel_nums[i] ==1:
                limit1 = i
                break
        if limit1 != -1:
            for i in range(limit1-1,0,-1):
                if row_pixel_nums[i] ==0 and i < limit1 -10:
                    limit2 = i
                    break
            if limit2 == -1:
                limit2 = 0
            img_crop = rawimage[limit2:limit1]
        croped_height = limit1 - limit2
        if croped_height >10:
            multi = 107 / croped_height 
            height, width = img_crop.shape[:2]
            img_scaled = cv2.resize(img_crop, (int(multi * width), int(multi * height)), interpolation=cv2.INTER_CUBIC)
        else:
            img_scaled = []
        return img_scaled



test = Maj_CV.Collect_Maj("1")






















