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