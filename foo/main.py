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


'''
对文件的操作
写入文本
传入参数 content，strim，path；
content 为需要写入的内容，数据类型为字符串
strim 写入方式
path 为写入的位置，数据类型为字符串。
传入的 path 需如下定义：path= r'D:\text.txt'
f = codecs.open(path, strim, 'utf8') 中，codecs 为包，需要用 import 引入
strim = 'a' 表示追加写入txt，可以换成 'w' ，表示覆盖写入
'utf8'表示写入的编码，可以换成 'utf16'等
'''


def write_txt(content, strim, path):
    f = codecs.open(path, strim, 'utf8')
    f.write(str(content))
    f.close()


'''
读取 txt
表示按行读取 txt 文件，utf8 表示读取编码为 utf8 的文件，可以根据需求改成 utf16，或者 GBK 等
返回的值为数组，每一个数组的元素代表一行
若想返回字符串格式，可以改成 return '\n'.join(lines)
'''


def read_txt(path):
    with open(path,'r', encoding='utf8') as f:
        lines = f.readlines()
        return lines


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
        # 绘制背景
        screen.fill(0)  # 使用颜色填充 surface
        screen.blit(background, (0, 0))
        # 控制游戏最大帧频为 60
        clock.tick(60)
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
        # 生成敌机，需要控制生成频率
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, screen_width - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        for enemy in enemies1:
            # 移动敌机
            enemy.move()
            # 敌机与玩家飞机碰撞效果处理，两个精灵之间的圆检测
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break
            # 移动出屏幕后删除飞机
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
        # 敌机被子弹击中效果处理
        # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
        # 方法 groupcollide() 是检测两个精灵组中精灵们的矩形冲突
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        # 遍历 key 值，返回的碰撞敌机
        for enemy_down in enemies1_down:
            # 添加销毁的敌机到列表
            enemies_down.add(enemy_down)
        # 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.img_index = shoot_frequency // 8
        else:
            # 玩家飞机被击中后的效果处理
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                # 击中效果处理完成后游戏结束
                running = False
        # 敌机被子弹击中效果显示
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 10
                continue
            # 显示碰撞图片
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1
        # 显示精灵
        enemies1.draw(screen)
        # 绘制当前分数
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)
        # 更新屏幕
        pygame.display.update()
        # 退出游戏
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # 获取键盘事件（上、下、左、右）
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

    # 绘制游戏结束背景
    screen.blit(game_over, (0, 0))
    # 游戏 Game Over 后显示最终得分
    font = pygame.font.Font(None, 48)
    text = font.render('Score:' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)
    # 使用系统字体
    xtfont = pygame.font.SysFont('SimHei', 30)
    # 重新开始按钮
    textstart = xtfont.render('从新开始', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)
    # 排行榜按钮
    textstart = xtfont.render('排行榜', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)

    # 判断得分更新排行榜
    # 临时的变量在到排行榜的时候使用
    j = 0
    # 获取文件中内容转换成列表，使用 mr 分割开内容
    arrayscore = read_txt(r'score.txt')[0].split('mr')
    # 循环分数列表，在列表里排序
    for i in range(0, len(arrayscore)):
        # 判断当前获得的分数是否大于排行榜上的分数
        if score > int(arrayscore[i]):
            # 大于排行榜上的内容，把分数和当前分数进行替换
            j = arrayscore[i]
            arrayscore[i] = str(score)
            score = 0
        # 替换下来的分数向下移动一位
        if int(j) > int(arrayscore[i]):
            k = arrayscore[i]
            arrayscore[i] = str(j)
            j = k
    # 循环分数列表，写入文档
    for i in range(0, len(arrayscore)):
        # 判断列表中第一个分数
        if i == 0:
            # 覆盖写入内容，追加 mr 方便分割内容
            write_txt(arrayscore[i] + 'mr', 'w', r'score.txt')
        else:
            # 判断是否为最后一个分数
            if i == 9:
                # 最近添加内容，最后一个分数不添加 mr
                write_txt(arrayscore[i], 'a', r'score.txt')
            else:
                # 不是最后一个分数，添加的时候添加 mr
                write_txt(arrayscore[i] + 'mr', 'a', r'score.txt')


# 排行榜
def game_ranking():
    screen2 = pygame.display.set_mode((screen_width, screen_height))
    # 绘制背景
    screen2.fill(0)
    screen2.blit(background, (0, 0))
    # 使用系统字体
    xtfont = pygame.font.SysFont('SimHei', 30)
    # 排行榜按钮
    textstart = xtfont.render('排行榜', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.centery = 50
    screen2.blit(textstart, text_rect)
    # 重新开始按钮
    textstart = xtfont.render('重新开始', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.centery = screen2.get_rect().centery + 120
    screen2.blit(textstart, text_rect)
    # 获取排行榜文件内容
    arrayscore = read_txt(r'score.txt')[0].split('mr')
    # 遍历排行榜文件显示排行
    for i in range(0, len(arrayscore)):
        # 游戏 Game Over 后显示最终得分
        font = pygame.font.Font(None, 48)
        # 排名从 1 到 10
        k = i + 1
        l_k = len(str(k).encode('gbk')) - len(str(k))
        text = font.render(str(k).ljust(2 - l_k) + '  ' + arrayscore[i], True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen2.get_rect().centerx
        text_rect.centery = 80 + 30*k
        # 绘制分数内容
        screen2.blit(text, text_rect)


start_game()


# 判断点击位置以及处理游戏退出
while True:
    for event in pygame.event.get():
        # 关闭页面游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 鼠标单击
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 判断鼠标单击的位置是否为开始按钮位置范围内
            if screen.get_rect().centerx - 70 <= event.pos[0] \
                and event.pos[0] <= screen.get_rect().centerx + 50 \
                and screen.get_rect().centery + 100 <= event.pos[1] \
                and screen.get_rect().centery + 140 >= event.pos[1]:
                # 重新开始游戏
                start_game()
            if screen.get_rect().centerx - 70 <= event.pos[0] \
                and event.pos[0] <= screen.get_rect().centerx + 50 \
                and screen.get_rect().centery + 160 <= event.pos[1] \
                and screen.get_rect().centery + 200 >= event.pos[1]:
                # 显示排行榜
                game_ranking()
    # 跟新界面
    pygame.display.update()
