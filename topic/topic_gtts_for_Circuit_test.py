# -*- coding: UTF-8 -*-
import sys
import os
from time import sleep
import serial
from gtts import gTTS
from pygame import mixer
import tempfile

'''
#儲存音檔
tts = gTTS(text='上方得分', lang ='zh-tw')
tts.save("上方得分.mp3")
'''
'''
#撥放音檔
mixer.init()
mixer.music.load("上方得分.mp3")
mixer.music.play()
'''

button=0
#測定序列阜與包率
COM_PORT = 'COM3'  # 請自行修改序列埠名稱
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)

count =False


breaker = False
while True:
    while ser.in_waiting:
        mcu_feedback = ser.readline().decode('utf-8')  # 接收回應訊息並解碼
    
        print(type(mcu_feedback))
        print('控制板回應：',mcu_feedback)
        #button=str(mcu_feedback)
        #print('button：',button)
        #sleep(5)
        if mcu_feedback[1] == '0':
            print('True')
            continue
        else:
            print('False')
        if mcu_feedback[1] == '1':
            button=1
            print('button：',button)
            breaker = True
            break
        elif mcu_feedback[1] == '2':
            button=2
            breaker = True
            break
    if breaker == True:
        break

if button == 1:
    Language = 'en-us'
    count=True    

elif button== 2:
    Language = 'zh-tw'
    count =True
               
#打字輸出即音檔
def speak(sentence):
	with tempfile.NamedTemporaryFile(delete=True) as fp:
		tts = gTTS(text=sentence, lang = Language)
		tts.save("{}.mp3".format(fp.name))
		mixer.init()
		mixer.music.load('{}.mp3'.format(fp.name))
		mixer.music.play()

#報分函數
def say():
    if speak_start == 1 : 
        if button == 1:
            speak("A"+str(num_l))
            sleep(1)
            #speak('比')
            #sleep(1)
            speak("B"+str(num_r))
            sleep(2)
        elif button == 2:
            speak("A方"+str(num_l)+"分")
            sleep(2)
            #speak('比')
            #sleep(1)
            speak("B方"+str(num_r)+"分")
            sleep(2)
    elif speak_start == 2 :
        if button == 1:
            speak("B"+str(num_r))
            sleep(1)
            #speak('比')
            #sleep(1)
            speak("A"+str(num_l))
            sleep(2)
        elif button == 2:
            speak("B方"+str(num_r)+"分")
            sleep(2)
            #speak('比')
            #sleep(1)
            speak("A方"+str(num_l)+"分")
            sleep(2) 

def saydeuce():
    if button == 1:
        speak("deuce")
        sleep(0.5)
    elif button ==2:
        speak("平局")
        sleep(2)

def saygamepoint_left():
    if button == 1:
        speak("A gamepoin")
        sleep(1)
    elif button ==2:
        speak("A方局末")
        sleep(4)
def saygamepoint_right():
    if button == 1:
        speak("B gamepoin")
        sleep(1)
    elif button ==2:
        speak("B方局末")
        sleep(2)

def sayend():
    if button == 1:
        speak("End of this round")
        sleep(1)
    elif button ==2:
        speak("此局結束")
        sleep(2)

#在.txt印出終端機產生的資料
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")                  #不複寫是"a",複寫是"w"

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('ball_position.txt')

#print(path)                                            #印出所在資料夾
#print(os.path.dirname(__file__))

#f = open(r'/home/yaocong/darknet/result.txt')          #讀取檔案
#sleep(25)

#變數區
#計分器變數
num_l=0                                                 #左側計分器(程式測試用)
num_r=0                                                 #右側計分器(程式測試用)
num_left=0                                              #左側計分器
num_right=0                                             #右側計分器
#程式變數
#fall=0                                                  #落下次數
pre_x=0                                                 #設定球體過去橫向變數
now_x=0                                                 #設定球體現在橫向變數
#now_left_x=0
#pre_left_x=0
#now_right_x=0
#pre_right_x=0
pre_y=0                                                 #設定球體過去高度變數
now_y=0                                                 #設定球體現在高度變數
net_x=0                                                 #假設球網x軸位置
net_y=0                                                 #假設球網頂高度位置
#net_range=50                                            #球網判分範圍值
#net_left=0                                              #球網左側觸網帶
#net_right=0                                             #球網右側觸網帶    
table_height=0                                          #假設球桌高度
table_width_l=0                                         #假設球桌左側x 
table_width_r=0                                         #假設球桌右側x
now_action_x=0                                          #設定過去球體橫軸狀態變數(左至右；右至左)
LEFT_TO_RIGHT=1
RIGHT_TO_LEFT=2
pre_action_y=0                                          #設定過去球體高度狀態變數
now_action_y=0                                          #設定現在球體高度狀態變數
UP_TO_DOWN=1
DOWN_TO_UP=2
voice_left=1
voice_right=2
pre_num_l=0
pre_num_r=0
start_bonuce_left=0                                     #計算左邊發球後彈跳
start_bounce_right=0                                    #計算右邊發球後彈跳
bounce_left=0                                           #設定左彈跳變數
bounce_right=0                                          #設定右彈跳變數
checknetlines=0                                         #確認目前抓取球網參數第幾次
checktablelines=0                                       #確認目前抓取球桌參數第幾次
#所有抓取到的相同參數總和
sum_netleft_x=0                                         
sum_nettop_y=0
sum_netwidth=0
sum_netheight=0
sum_tableleft_x=0
sum_tabletop_y=0
sum_tablewidth=0
sum_tableheight=0
#所有抓取到的相同參數平均
avg_netleft_x=0
avg_nettop_y=0
avg_netwidth=0
avg_netheight=0
avg_tableleft_x=0
avg_tabletop_y=0
avg_tablewidth=0
avg_tableheight=0

#讀取校正檔座標值
f = filter(None, (line.rstrip() for line in open(r'C:/Users/chen5/Desktop/topic/table.txt')))     #讀取檔案，但將多餘的空行去除
lines=0
text =[]                                                #設置文字陣列
for line in f:                                          #讀取文字迴圈
    text.append(line)                                   #將文字逐行放入text陣列
    lines+=1                                            #得知最後一行是第幾次
    #print("行數",line)

#print(lines)      
#print(text[13:])                                       #取13行以後所有值

for x in range(1,lines):                                #設定讀取區間，到最後一次
    #print(text)                                        #測試
   
    if 'net:' in text[x]:                               #取內容有net:的那行
        #print(text[x])                                 #測試
        #print (text[x].split())                        #將字串依空白的部分做分割
      
        checknetlines+=1                                #每取一致次值就加1
        #print(checknetlines)
        wordleft_x=text[x].split()[3]                   #取分割後的第4項
        netleft_x= int(float(wordleft_x))               #將string轉換為int或float
        sum_netleft_x=sum_netleft_x+netleft_x           #每一次的加總
        avg_netleft_x=sum_netleft_x//checknetlines      #做所有值得平均
        #print ("netleft_x:",netleft_x)                 #印出當前數值
        #print ("avg_netleft_x:",avg_netleft_x)         #印出當前平均
        wordtop_y=text[x].split()[5]
        nettop_y= int(float(wordtop_y))
        sum_nettop_y=sum_nettop_y+nettop_y
        avg_nettop_y=sum_nettop_y//checknetlines
        #print ("nettop_y:",nettop_y)
        #print ("avg_nettop_y:",avg_nettop_y)
        wordwidth=text[x].split()[7]
        netwidth= int(float(wordwidth))
        sum_netwidth=sum_netwidth+netwidth
        avg_netwidth=sum_netwidth//checknetlines
        #print ("netwidth:",netwidth)
        #print ("avg_netwidth:",avg_netwidth)
        wordheight=text[x].split()[9].strip(')')        #取分割後的第10項，並去除')'
        netheight= int(float(wordheight))
        sum_netheight=sum_netheight+netheight
        avg_netheight=sum_netheight//checknetlines
        #print ("netheight:",netheight)
        #print ("avg_netheight:",avg_netheight)

        net_x=avg_netleft_x+avg_netwidth/2              #設定球網橫軸數值
        net_y=avg_nettop_y                              #設定球網高度數值
        #net_left=avg_netleft_x                         
        #net_right=avg_netleft_x+avg_netwidth
           
    if 'table:' in text[x]:                             #取開內容有table:的那行
        #print(text[x])                                 #測試
        #print (text[x].split())                        #將字串依空白的部分做分割

        checktablelines+=1                              #每取一致次值就加1
        #print(checktablelines)                     
        wordleft_x=text[x].split()[3]                   #取分割後的第4項
        tableleft_x= int(float(wordleft_x))             #將string轉換為int或float
        sum_tableleft_x=sum_tableleft_x+tableleft_x     #每一次的加總
        avg_tableleft_x=sum_tableleft_x//checktablelines#做所有值得平均
        #print ("tableleft_x:",tableleft_x)             #印出當前數值
        #print ("avg_tableleft_x:",avg_tableleft_x)     #印出當前平均
        wordtop_y=text[x].split()[5]
        tabletop_y= int(float(wordtop_y))
        sum_tabletop_y=sum_tabletop_y+tabletop_y
        avg_tabletop_y=sum_tabletop_y//checktablelines
        #print ("tabletop_y:",tabletop_y)
        #print ("avg_tabletop_y:",avg_tabletop_y)
        wordwidth=text[x].split()[7]
        tablewidth= int(float(wordwidth))
        sum_tablewidth=sum_tablewidth+tablewidth
        avg_tablewidth=sum_tablewidth//checktablelines
        #print ("tablewidth:",tablewidth)
        #print ("avg_tablewidth:",avg_tablewidth)
        wordheight=text[x].split()[9].strip(')')        #取分割後的第10項，並去除')'
        tableheight= int(float(wordheight))
        sum_tableheight=sum_tableheight+tableheight
        avg_tableheight=sum_tableheight//checktablelines
        #print ("tableheight:",tableheight)
        #print ("avg_tableheight:",avg_tableheight)

        table_height=avg_tabletop_y                     #設定球網高度
        table_width_l=avg_tableleft_x                   #設定球網左側邊緣
        table_width_r=avg_tableleft_x+avg_tablewidth    #設定球網右側邊緣

#讀取球體運動檔座標值
f = filter(None, (line.rstrip() for line in open(r'C:/Users/chen5/Desktop/topic/ball.txt')))     #讀取檔案，但將多餘的空行去除
lines=0
text =[]                                                #設置文字陣列
for line in f:                                          #讀取文字迴圈
    text.append(line)                                   #將文字逐行放入text陣列
    lines+=1                                            #得知最後一行是第幾次
    #print("行數",line)

#print(lines)      
#print(text[13:])                                       #取13行以後所有值



speak_stop=False
if count == True:
    for x in range(1,lines):                                #設定讀取區間，到最後一次
        #print(text[x])                                     #測試

            
        if 'ball:' in text[x]:                              #取開內容有ball:的那行

            #print(text[x])                                 #測試
            #print (text[x].split())                        #將字串依空白的部分做分割

            wordleft_x=text[x].split()[3]                   #取分割後的第4項
            ballleft_x= int(float(wordleft_x))              #將string轉換為int或float
            #print ("ballleft_x:",ballleft_x)               #印出當前數值
            wordtop_y=text[x].split()[5]
            balltop_y= int(float(wordtop_y))
            #print ("balltop_y:",balltop_y)
            wordwidth=text[x].split()[7]
            ballwidth= int(float(wordwidth))
            #print ("ballwidth:",ballwidth)
            wordheight=text[x].split()[9].strip(')')        #取分割後的第10項，並去除')'
            ballheight= int(float(wordheight))
            #print ("ballheight:",ballheight)

            now_x=ballleft_x+ballwidth/2                    #球的中心延伸垂直x軸=框的左邊加上寬的一半
            print("球體現在x位置:",now_x)
            now_y = balltop_y                               #現在高度=球體的上緣座標-球體高度
            #now_left_x=ballleft_x
            #now_right_x=ballleft_x+ballwidth
    #判斷球體目前與過去狀態
    #設定球體左右方向狀態旗標
            if  now_x > pre_x and now_y < table_height:                              
                print("由左往右")
                now_action_x=LEFT_TO_RIGHT
            elif now_x < pre_x and now_y < table_height:
                print("由右往左")    
                now_action_x=RIGHT_TO_LEFT

    #設定球體上下高度狀態旗標       
            print("球體現在高度:",now_y)                                
            print("球體過去高度:",pre_y)
            if now_y > pre_y:                               #判斷現在球體的高度是否高於或低於過去高度
                print("落下中")                             
                now_action_y=UP_TO_DOWN                              #設定現在狀態為1。 注意:不可設為0，因初始值為0未導致第一顆球誤判

                #fall+=1
                #if fall > 2:
                    #fall=0
            elif now_y < pre_y:
                print("上升中")
                now_action_y=DOWN_TO_UP                              #設定現在狀態為2。 注意:不可設為0，因初始值為0未導致第一顆球誤判

    #判斷彈跳
            if pre_action_y==UP_TO_DOWN :                             #假設過去球體狀態落下而現在上升即是發生彈跳
                if now_action_y==DOWN_TO_UP:
                    print("彈跳")
                    if now_y < table_height:
                        if now_x < net_x and now_x > table_width_l:     #如果球體的中線大於球網代表求在球往左邊，但是必須在左桌緣內的範圍
                            #bounce_right=0                             #此時右邊彈跳歸零
                            bounce_left+=1                              #發生彈跳時左邊彈跳加1
                            start_bonuce_left+=1                        #計算左邊發球後彈跳加1
                            print("左側彈跳",start_bonuce_left)
                            #if bounce_left >= 2:                       #如果左側彈跳兩次
                                #print("左側彈跳兩次")

                        elif now_x > net_x and now_x < table_width_r:   #如果球體的中線大於球網代表求在球往右邊，但是必須在右桌緣內的範圍
                            #bounce_left=0                              #此時左邊彈跳歸零
                            bounce_right+=1                             #發生彈跳時右邊彈跳加1
                            start_bounce_right+=1                       #計算右邊發球後彈跳加1
                            print("右側彈跳",start_bounce_right)
                            #if bounce_right >= 2:                      #如果右側彈跳兩次
                                #print("右側彈跳兩次")
            else:
                print("未彈跳")
    #判斷發球           
            start = False
            if now_action_x==LEFT_TO_RIGHT:                                         #如果球體左側到右側
                if start_bonuce_left == 1:                              #在左側球桌彈跳第一次
                    start_bounce_right = 0                              #右側不計算
                    start = True                                    
                    print("左側發球")
                    speak_start=voice_left                                       #告知計分器左側先報

            elif now_action_x==RIGHT_TO_LEFT:                                       #如果球體右側到左側
                if start_bounce_right == 1:                             #在左側球桌彈跳第一次
                    start_bonuce_left = 0                               #左側不計算
                    start = True
                    print("右側發球")
                    speak_start=voice_right                                       #告知計分器右側先報

            else:
                start = False

    #判斷得分 
            
                #設定低於球桌旗標，避免重複判分      
            is_lower=False                                          #剛開始狀態為False                  
            if pre_y < table_height and now_y > table_height:       #如果過去球體比球桌高但現在的球體比球桌低
                print("低於桌面")
                is_lower=True                                       #狀態轉為True

            if start == False:
                print(start)
                if now_action_x==LEFT_TO_RIGHT:            #由左往右
                    if  bounce_left == 1:                               #左側彈跳
                        num_r+=1
                        #print('num_right')
                        ser.write(b'num_right\n')                      #訊息必須是位元組類型
                        say()                                           #呼叫報分函數
                        start_bonuce_left=0                             #計算發球彈跳歸零
                        start_bounce_right=0                            #計算發球彈跳歸零      
                    elif is_lower == True:                              #球低於球桌，is_lower轉True
                        num_r+=1
                        #print('num_right')
                        ser.write(b'num_right\n')                      #傳送訊息必須是位元組類型
                        say()                                           #呼叫報分函數
                        is_lower=False                                  #分數加完後，is_lower轉False
                        start_bonuce_left=0
                        start_bounce_right=0                
                elif now_action_x==RIGHT_TO_LEFT:          #由右往左
                    if bounce_right == 1:                               #右側彈跳
                        num_l+=1
                        #print('num_left')
                        ser.write(b'num_left\n')                       #訊息必須是位元組類型
                        say()                                           #呼叫報分函數
                        start_bonuce_left=0
                        start_bounce_right=0                   
                    elif is_lower == True:                              #球低於球桌，is_lower轉True
                        num_l+=1
                        #print('num_left')
                        ser.write(b'num_left\n')                       #傳送訊息必須是位元組類型
                        say()                                           #呼叫報分函數
                        is_lower=False                                  #分數加完後，is_lower轉False
                        start_bonuce_left=0
                        start_bounce_right=0

            #while ser.in_waiting:
                #mcu_feedback = ser.readline().decode()  # 接收回應訊息並解碼
                #print('控制板回應：', mcu_feedback)

            bounce_right=0                                          #右邊彈跳歸零
            bounce_left=0                                           #左邊彈跳歸零
            pre_x = now_x                                           #將現在橫向座標存入過去高度變數                                           
            pre_y = now_y                                           #將現在高度座標存入過去高度變數
            pre_action_y = now_action_y                             #將現在高度狀態存入過去高度狀態變數
            #pre_left_x = now_left_x
            #pre_right_x= now_right_x
            print("左分:",num_l)
            print("右分:",num_r)

            if num_l == 10 and num_r < 10 and speak_stop == False:
                saygamepoint_left()
                speak_stop = True
            elif num_r == 10 and num_l < 10 and speak_stop == False:
                saygamepoint_right()
                speak_stop = True
            elif num_l >= 10 and num_r >= 10 and num_l == num_r and speak_stop == False:
                saydeuce()
                print("saydeuce")
                speak_stop = True
            elif num_l > 10 and num_l - num_r == 1 and speak_stop == False:
                saygamepoint_left()
                speak_stop = True
            elif num_r > 10 and num_r - num_l == 1 and speak_stop == False:
                saygamepoint_right()
                speak_stop = True

            if  num_l != pre_num_l or num_r != pre_num_r:
                speak_stop = False        

            pre_num_l = num_l
            pre_num_r = num_r

            if num_l == 11 and num_r < 10:
                num_l=0
                num_r=0
                sayend()
                print("此局結束，請按Enter繼續下局")
                input()
                #sys.exit()
            elif num_r == 11 and num_l < 10:
                num_l=0
                num_r=0
                sayend()
                print("此局結束，請按Enter繼續下局")
                input()
                #sys.exit()
            elif num_l > 10 and num_l - num_r ==2:
                num_l=0
                num_r=0
                sayend()
                print("此局結束，請按Enter繼續下局")
                input()
                #sys.exit()
            elif num_r > 10 and num_r - num_l ==2:
                num_l=0
                num_r=0
                sayend()
                print("此局結束，請按Enter繼續下局")
                input()
                #sys.exit()
            
#f.close()                                                      #關閉所讀取檔案
