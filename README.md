# play_game_with_your_mouth
出一張嘴來玩個遊戲吧
## 動機敘述
  前陣子天氣實在是太冷了，又因為不太需要去上課了，所以整天只想窩在被窩裡面不想出來。但是窩在被窩又太無聊了會想玩一下遊戲，恰好手邊有一個樹莓派，那就利用樹莓派來接收語音輸入的指令去玩遊戲吧。
## Implementation Resources 硬體設備
1. Raspberry Pi Model 3B
2. 一個鍵盤
3. 一個麥克風
4. 一個顯示屏幕
## Existing Library/Software 軟體架構
- Ubuntu 20.04
- Raspberry Pi OS
- python 3.9.2
## Implementation Process 實作步驟

#### 參考程式碼頁面
https://ask.hellobi.com/blog/python_shequ/19344

#### 新增的程式碼

新增語音偵測輸入方向控制指令。

```
def CheckSpeech():
    global changeDirection
    # Change
    resource = {
        r"(左)+": "left",
        r"(右)+": "right",
        r"(上)+": "up",
        r"(下)+": "down",
    }
    # engine = pyttsx3.init()
    # while True:
    r = sr.Recognizer()
    # 麥克風
    mic = sr.Microphone()
    logging.info('錄音中...')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    logging.info('錄音結束，識別中...')
    test = r.recognize_google(audio, language='cmn-Hans-CN', show_all=True)

    # 分析語音
    # logging.info('分析語音')
    if test:
        flag = False
        message = ''
        for t in test['alternative']:
            # logging.debug(t)
            for r, c in resource.items():
                # 用每個識別結果來匹配資源文件key(正則)，正確匹配則存儲回答並退出
                # logging.info(r)
                if re.search(r, t['transcript']):
                    flag = True
                    message = c
                    break
            if flag:
                break
        # 文字轉語音
        if message:
            # logging.info('bingo....')
            # logging.info('say: %s' % message)
            # engine.say(message)
            # engine.runAndWait()
            # logging.info('ok')
            print(message)
            return message
            # changeDirection = message
            # Change = True
    logging.info('end')
```

**最終的程式碼**

```
import pygame,sys,time,random
from pygame.locals import *
import re
import speech_recognition as sr
import logging
import threading
logging.basicConfig(level=logging.DEBUG)

# 定义颜色变量
redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greyColour = pygame.Color(150,150,150)

def gameOver(playSurface,score):
    gameOverFont = pygame.font.SysFont('arial.ttf',54)
    gameOverSurf = gameOverFont.render('Game Over!', True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (300, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    scoreFont = pygame.font.SysFont('arial.ttf',54)
    scoreSurf = scoreFont.render('Score:'+str(score), True, greyColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (300, 50)
    playSurface.blit(scoreSurf, scoreRect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()
    # t.stop()

Change = False

def main():
    # 初始化pygame
    pygame.init()
    fpsClock = pygame.time.Clock()
    # 创建pygame显示层
    playSurface = pygame.display.set_mode((600,460))
    pygame.display.set_caption('Snake Game')
    # 初始化变量
    snakePosition = [100,100] #贪吃蛇 蛇头的位置
    snakeSegments = [[100,100]] #贪吃蛇 蛇的身体，初始为一个单位
    raspberryPosition = [300,300] #树莓的初始位置
    raspberrySpawned = 1 #树莓的个数为1
    direction = 'right' #初始方向为右
    changeDirection = direction
    score = 0 #初始得分
    
    # t.start()
    while True:
        # 检测例如按键等pygame事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                if event.key == K_SPACE:
                    changeDirection = CheckSpeech()
                    # t = threading.Thread(target=CheckSpeech)
                    # t.start()
            # elif Change:
            #     Change = False
            #     print("yes")
        # 判断是否输入了反方向
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'left' and not direction == 'right':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection
        # 根据方向移动蛇头的坐标
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20
        # 增加蛇的长度
        snakeSegments.insert(0,list(snakePosition))
        # 判断是否吃掉了树莓
        if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
            raspberrySpawned = 0
        else:
            snakeSegments.pop()
            
        # 如果吃掉树莓，则重新生成树莓
        if raspberrySpawned == 0:
            x = random.randrange(1,30)
            y = random.randrange(1,23)
            raspberryPosition = [int(x*20),int(y*20)]
            raspberrySpawned = 1
            score += 1
        # 绘制pygame显示层
        playSurface.fill(blackColour)
        for position in snakeSegments:
            pygame.draw.rect(playSurface,whiteColour,Rect(position[0],position[1],20,20))
            pygame.draw.rect(playSurface,redColour,Rect(raspberryPosition[0], raspberryPosition[1],20,20))
        # 刷新pygame显示层
        pygame.display.flip()
        
        # 判断是否死亡
        if snakePosition[0] > 600 or snakePosition[0] < 0:
            gameOver(playSurface,score)
        if snakePosition[1] > 460 or snakePosition[1] < 0:
            gameOver(playSurface,score)
        for snakeBody in snakeSegments[1:]:
            if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
                gameOver(playSurface,score)
        # 控制游戏速度
        fpsClock.tick(5)

def CheckSpeech():
    global changeDirection
    # Change
    resource = {
        r"(左)+": "left",
        r"(右)+": "right",
        r"(上)+": "up",
        r"(下)+": "down",
    }
    # engine = pyttsx3.init()
    # while True:
    r = sr.Recognizer()
    # 麥克風
    mic = sr.Microphone()
    logging.info('錄音中...')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    logging.info('錄音結束，識別中...')
    test = r.recognize_google(audio, language='cmn-Hans-CN', show_all=True)

    # 分析語音
    # logging.info('分析語音')
    if test:
        flag = False
        message = ''
        for t in test['alternative']:
            # logging.debug(t)
            for r, c in resource.items():
                # 用每個識別結果來匹配資源文件key(正則)，正確匹配則存儲回答並退出
                # logging.info(r)
                if re.search(r, t['transcript']):
                    flag = True
                    message = c
                    break
            if flag:
                break
        # 文字轉語音
        if message:
            # logging.info('bingo....')
            # logging.info('say: %s' % message)
            # engine.say(message)
            # engine.runAndWait()
            # logging.info('ok')
            print(message)
            return message
            # changeDirection = message
            # Change = True
    logging.info('end')

if __name__ == "__main__":
    main()
```
## Installation 樹莓派預先安裝
- 安裝git
```
$ sudo apt install git
```
- 安裝python
```
$ sudo apt install python3
```
![image alt](https://i.imgur.com/wjFillO.jpg)
- 安裝pip
```
$ sudo apt install python3-pip
```
![image alt](https://i.imgur.com/0A89sMC.jpg)
- 安裝pygame
```
$ sudo apt-get install python3-pygame
```
![image alt](https://i.imgur.com/l3yNNeV.png)
- 安裝有有關聲音的庫
```
$ sudo apt install libasound-dev portaudio19-dev
```
![image alt](https://i.imgur.com/ao7PDMu.jpg)
- 安裝pyaudio
```
$ sudo pip install pyaudio
```
- 安裝Speech Recognition
```
$ pip install SheechRecognition
```
![image alt](https://i.imgur.com/IM3YFFO.png)
## Knowledge from Lecture
  Linux的基本指令 ---> [課堂教學:基本指令](https://hackmd.io/@ncnu-opensource/book/https%3A%2F%2Fhackmd.io%2F84K86TUPQi2lfspQpciACA)
  樹莓派 ---> [課堂教學:樹莓派](https://hackmd.io/@ncnu-opensource/book/https%3A%2F%2Fhackmd.io%2F2j1JjIi_Q4KFgzkRgCZclw%3Fboth)

## Usage 使用方法

1. 在樹莓派上安裝好上述所需套件
2. 修改位於/boot/config.txt
3. 下載程式碼
4. 執行py檔

需要修改的地方如下，或者查看參考資料
![image alt](https://i.imgur.com/FMc0xNN.png)
以下以ubuntu20.04來實際跑一次流程(已安裝好套件):
- 首先是把我們的專案git下來
```
$ git clone https://github.com/johnwong011010/play_game_with_your_mouth
```
![image alt](https://i.imgur.com/TtkL87t.png)

- 然後更改下載的資料夾的權限(可選做):
![image alt](https://i.imgur.com/yyMuCg2.png)

- cd進去執行就可以了:
![image alt](https://i.imgur.com/q1yVXGC.png)


### Q&A
1. 為什麼要去修改/boot/config.txt
A.因為樹莓派預設沒有螢幕，不進行修改會無法進行輸出，修改完這一行後會令樹莓派認為有螢幕進行輸出。
2. 可以不接螢幕嗎?
A.是可以但不推薦，如果真的真的沒螢幕可以考慮使用手機ssh進去樹莓派再顯示。

## Experimental results 實驗成果
https://www.youtube.com/watch?v=6IOMSk2gu0g
## Job Assignment 工作分配
題目構思：全體組員
程式編寫：沈佳龍，黃浩銘
Github：沈佳龍，黃浩銘
樹莓派使用：陳世效，吳偉勇，黃浩銘
簡報製作：陳世效，胡天維
## References 參考資料

遊戲主架構參考
https://ask.hellobi.com/blog/python_shequ/19344

語音辨識
https://blog.csdn.net/meiguanxi7878/article/details/101079647
https://www.twblogs.net/a/5c11e739bd9eee5e4183b207

How to install pyaudio ubuntu 16.04 LTS
https://gist.github.com/barseghyanartur/3f59ef89a08dfe46e307a6dc3a75ac50

讓樹莓派不用接螢幕也會有圖形介面
https://noob.tw/pygame-headless/
