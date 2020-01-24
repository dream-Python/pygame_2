# _*_ coding  ：  UTF-8 _*_
# 开发团队    ：  dream
# 开发人员    ：  刘育彬
# 开发时间    ：  2020/1/24  11:08
# 文件名称    ：  main.py
# 开发工具    ：  PyCharm


import pygame
from pygame.locals import *
from sys import exit
import random


# 设置游戏屏幕大小
screen_width = 480
screen_height = 800


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                     # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]          # 初始化图片所在的矩形
        self.rect.topleft = init_pos        # 初始化矩形的左上角坐标
        self.speed = 2                      # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()          # 玩家飞机所发射的子弹的集合
        self.img_index = 0                  # 玩家飞机图片索引
        self.is_hit = False                 # 玩家是否被击中

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    # 向上移动，需要判断边界
    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动，需要判断边界
    def move_down(self):
        if self.rect.top >= screen_height - self.rect.height:
            self.rect.top = screen_height - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，需要判断边界
    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，需要判断边界
    def move_right(self):
        if self.rect.left >= screen_width - self.rect.width:
            self.rect.left = screen_width - self.rect.width
        else:
            self.rect.left += self.speed


# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed


# 初始化pygame
pygame.init()
# 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小
screen = pygame.display.set_mode((screen_width, screen_height))
# 游戏界面标题
pygame.display.set_caption('飞机大战')
# 图标
ic_launcher = pygame.image.load('image/ic_launcher.png').convert_alpha()
pygame.display.set_icon(ic_launcher)
# 背景图
background = pygame.image.load('image/background.png').convert()
# Game Over 背景图
game_over = pygame.image.load('image/gameover.png')
# 飞机及子弹图片集合
plane_img = pygame.image.load('image/shoot.png')


def start_game():
    # 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
    player_rect = []
    # 玩家飞机图片
    player_rect.append(pygame.Rect(0, 99, 100, 120))
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    # 玩家爆炸图片
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_img, player_rect, player_pos)
    # 子弹图片
    bullet_rect = pygame.Rect(1005, 987, 10, 21)
    bullet_img = plane_img.subsurface(bullet_rect)
    # 初始化射击及敌机移动频率
    shoot_frequency = 0

    # 判断游戏循环推出的参数
    running = True
    # 游戏主循环
    while running:
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        # 子弹
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        player.bullets.draw(screen)
        # 判断玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = shoot_frequency // 8
        # 更新屏幕
        pygame.display.update()
        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # 获取键盘事件（上下左右按键）
        key_pressed = pygame.key.get_pressed()
        # 处理键盘事件（移动飞机的位置）
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.move_right()

start_game()

