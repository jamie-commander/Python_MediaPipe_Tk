# pip install pygame
import pygame
pygame.init()
pygame.mixer.init()
pygame.time.delay(1000)#等待1秒讓mixer完成初始化
soundwav=pygame.mixer.Sound('sound_5_4_3_2_1.mp3')
soundwav.play()
pygame.time.delay(1000)#等待1秒讓mixer完成初始化
for i in range(5, 0, -1):
    print(i)
    pygame.time.delay(1000)#等待1秒讓mixer完成初始化