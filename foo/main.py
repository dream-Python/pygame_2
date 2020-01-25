# _*_ coding  ：  UTF-8 _*_
# 开发团队    ：  dream
# 开发人员    ：  刘育彬
# 开发时间    ：  2020/1/25  14:59
# 文件名称    ：  main.py
# 开发工具    ：  PyCharm


import pygame             # 导入 pygame 库
from pygame.locals import *               # 导入 pygame 库中的一些常量
from sys import exit      # 导入 sys 库中的 exit 函数
import random
import codecs


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        # 调用父类的初始化方法初始化 sprite 的属性
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, player_rect, init_pos):
        # 调用父类的初始化方法初始化 sprite 的属性
        pygame.sprite.Sprite.__init__(self)
        self.image = []            # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(player_rect[i].convert_alpha())

        self.rect = player_rect[0].get_rect()            # 初始化图片所在的矩形
        self.rect.topleft = init_pos                     # 初始化矩形的左上角坐标
        self.speed = 8                                   # 初始化玩家飞机速度，这里是一个固定的值
        self.bullets = pygame.sprite.Group()               # 玩家飞机所发射的子弹的集合
        self.img_index = 0                               # 玩家飞机图片索引
        self.is_hit = False                              # 玩家是否被击中

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
        # 调用父类的初始化方法初始化 sprite 的属性
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed


# 设置游戏屏幕大小
screen_width = 480
screen_height = 800

# 初始化 pygame
pygame.init()
# 设置游戏界面大小
screen = pygame.display.set_mode((screen_width, screen_height))                # surface 对象，初始化一个准备显示的界面
# 游戏界面标题
pygame.display.set_caption('彩图版飞机大战')
# 设置游戏界面图标
ic_launcher = pygame.image.load('image/ic_launcher.png').convert_alpha()       # surface 对象
pygame.display.set_icon(ic_launcher)
# 背景图
background = pygame.image.load('image/background.png').convert_alpha()         # surface 对象
# 游戏结束背景图片
game_over = pygame.image.load('image/gameover.png')
# 子弹图片
plane_bullet = pygame.image.load('image/bullet.png')
# 飞机图片
player_img1 = pygame.image.load('image/player1.png')
player_img2 = pygame.image.load('image/player2.png')
player_img3 = pygame.image.load('image/player_off1.png')
player_img4 = pygame.image.load('image/player_off2.png')
player_img5 = pygame.image.load('image/player_off3.png')
# 敌机图片
enemy_img1 = pygame.image.load('image/enemy1.png')
enemy_img2 = pygame.image.load('image/enemy2.png')
enemy_img3 = pygame.image.load('image/enemy3.png')
enemy_img4 = pygame.image.load('image/enemy4.png')


def start_game():
    # 游戏循环帧频设置
    clock = pygame.time.Clock()               # pygame.time     管理时间和帧信息
    # 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
    player_rect = []
    # 玩家飞机图片
    player_rect.append(player_img1)
    player_rect.append(player_img2)
    # 玩家爆炸图片
    player_rect.append(player_img2)
    player_rect.append(player_img3)
    player_rect.append(player_img4)
    player_rect.append(player_img5)
    player_pos = [200, 600]
    # 初始化玩家飞机
    player = Player(player_rect, player_pos)
    # 子弹图片
    bullet_img = plane_bullet
    # 敌机不同状态的图片列表，多张图片展示为动画效果
    enemy1_img = enemy_img1
    enemy1_rect = enemy1_img.get_rect()
    enemy1_down_imgs = []
    enemy1_down_imgs.append(enemy_img1)
    enemy1_down_imgs.append(enemy_img2)
    enemy1_down_imgs.append(enemy_img3)
    enemy1_down_imgs.append(enemy_img4)
    # 储存敌机
    enemies1 = pygame.sprite.Group()
    # 存储被击毁的飞机，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()
    # 初始化射击及敌机移动频率
    shoot_frequency = 0
    enemy_frequency = 0
    # 玩家飞机被击中后的效果处理
    player_down_index = 16
    # 初始化分数
    score = 0

    # 判断游戏循环退出的参数
    running = True
    # 游戏主循环
    while running:
        # 生成子弹，需要控制发射频率
        # 首先判断玩家飞机没有被击中
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0
        for bullet in player.bullets:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # 显示子弹
        player.bullets.draw(screen)

        # 绘制背景
        screen.fill(0)                 # 使用颜色填充 surface
        screen.blit(background, (0, 0))
        # 控制游戏最大帧频为 60
        clock.tick(60)
        # 更新屏幕
        pygame.display.update()
        # 退出游戏
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


start_game()
