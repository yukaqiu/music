"""游戏元素"""

import pygame
import math

# 定义全局变量
SCREEN_RECT = pygame.Rect(0, 0, 960, 540)  # 默认游戏窗口
white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)

# 判定区
y_judge = [69, 182, 311, 648, 777, 890]

class Speed():
    def __init__(self):
        self.speed = 900
    #   默认为11，程序中speed越大，速度越慢
    #   但设定时还是按照习惯上数字越大速度越大而设定

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

speed_class = Speed()
SPEED = speed_class.get_speed()

class GameSprite(pygame.sprite.Sprite):
    res_path = "./picture/"

    def __init__(self, image_name, *group):
        """初始化精灵对象"""
        # 调用父类，把当前精灵放到精灵组里
        super(GameSprite, self).__init__(*group)
        # 创建图片
        self.image = pygame.image.load(self.res_path + image_name)
        # 获取矩形
        self.rect = self.image.get_rect()

    def update(self, *args):
        # 更新元素数据
        pass


class Label(pygame.sprite.Sprite):
    # 各类信息
    font_path = './font/'

    def __init__(self, text, size, color, font_type, *groups):
        # 初始化标签数据
        super(Label, self).__init__(*groups)
        # 创建字体对象
        self.font = pygame.font.Font(self.font_path + font_type, size)
        # 字体颜色
        self.color = color
        # 精灵属性
        self.image = self.font.render(text, True, self.color)  # 文本内容，抗锯齿，颜色
        self.rect = self.image.get_rect()

    def set_text(self, text):
        self.image = self.font.render(text, True, self.color)  # 文本内容，抗锯齿，颜色
        self.rect = self.image.get_rect()


class Note(GameSprite):
    def __init__(self, moment, note_type, track, *group):
        """note类的初始化"""
        # 基本属性
        self.moment = moment  # 对应节拍
        self.note_type = note_type  # note类型
        self.track = track  # 轨道
        self.grade = 0  # 评级
        # self.display_group = group
        self.is_press = 0  # 是否被按下
        self.SPEED = speed_class.get_speed()
        if track == 1 or track == 2 or track == 3:
            self.angle = 190
        else:
            self.angle = 260

        # 根据不同的note类型，设置图片和音效
        if self.note_type == 1:
            normal_name = "game/blue_note.png"
            self.press_names = ["game/blue_note_p_%d.png" % i for i in range(1, 11)]

            # wav_name = wav_name  # 音效
        elif self.note_type == 2:
            normal_name = "game/blue_note_left.png"
            self.press_names = ["game/blue_note_%d.png" % i for i in range(1, 11)]

        elif self.note_type == 3:
            normal_name = "game/blue_note_right.png"
            self.press_names = ["game/blue_note_%d.png" % i for i in range(1, 11)]

        else:
            # self.note_type == 6:
            normal_name = "game/yellow_note_1.png"
            self.press_names = ["game/yellow_note_%d.png" % i for i in range(1, 9)]

        super(Note, self).__init__(normal_name, *group)

        # 要显示的图片
        self.normal_image = pygame.image.load(self.res_path + normal_name)

        self.press_index = 0
        self.rect.y = -150

    def update(self, time, display_group, *args):
        """更新状态，准备下一次显示的内容"""
        # 判断是否更新
        if not args[0]:
            return

        # 切换图片
        self.image = self.normal_image
        press_images = [pygame.image.load(self.res_path + name) for name in self.press_names]

        # 是否被按下，不是就移动位置，是就炸开（？
        if not self.is_press:
            self.move_type(time, self.track, display_group)
        else:
            self.rect.centerx = y_judge[self.track - 1]
            self.rect.centery = 400

            count = len(press_images)
            # 计算下一次显示的索引
            self.image = press_images[math.floor(self.press_index)]
            if self.press_index == count - 1:
                display_group.remove(self)
                return

            self.press_index = self.press_index + 1

    def move_type(self, time, type, display_group):

        # 按键旋转
        radius = [450, 350, 250]
        if type == 1 or type == 2 or type == 3:
            change_angle = self.angle + 4 * ((time - self.moment) / (self.SPEED / 32))
            if change_angle > 345:
                display_group.remove(self)

            #     -————————————————————————————————————————————————————————

            # 保持轨道上的按键在同一高度(y值)
            self.rect.centery = math.cos(math.radians(change_angle)) * radius[2] + 215
            # 求按键的x值
            angle2 = -math.degrees(math.acos((self.rect.centery - 215) / radius[type - 1]))
            self.rect.centerx = math.sin(math.radians(angle2)) * radius[type - 1] + SCREEN_RECT.w / 2

        else:
            # elif type == 4 or type == 5 or type == 6:
            change_angle = self.angle - 4 * ((time - self.moment) / (self.SPEED / 32))
            if change_angle < 105:
                display_group.remove(self)
            # 保持轨道上的按键在同一高度(y值)
            self.rect.centery = math.sin(math.radians(change_angle)) * radius[2] + 215
            # 求按键的x值
            angle2 = math.degrees(math.asin((self.rect.centery - 215) / radius[-(type - 3)]))
            self.rect.centerx = math.cos(math.radians(angle2)) * radius[-(type - 3)] + SCREEN_RECT.w / 2


#             angle = 128

class Button(GameSprite):
    def __init__(self, normal_name, touch_name, *group):
        self.is_touch = 0
        self.normal_image = pygame.image.load(self.res_path + normal_name)
        self.touch_image = pygame.image.load(self.res_path + touch_name)
        super(Button, self).__init__(normal_name, *group)

    def switch_status(self):
        self.image = self.touch_image if self.is_touch else self.normal_image


class ArrowButton(Button):
    def __init__(self, normal_name, touch_name, update_page, *group):
        self.update_page = update_page
        super(ArrowButton, self).__init__(normal_name, touch_name, *group)

    def touch_event(self):
        return self.update_page


class MusicListButton(Button):
    def __init__(self, normal_name, touch_name, music_csv_path, music_mp3_path, music_name, *group):
        self.music_csv_path = music_csv_path
        self.music_name = music_name
        self.music_mp3_path = music_mp3_path
        super(MusicListButton, self).__init__(normal_name, touch_name, *group)

    def touch_event(self):
        return self.music_csv_path, self.music_mp3_path, self.music_name



class ChangePanelButton(Button):
    def __init__(self, normal_name, touch_name, target_panel, *group):
        self.target_panel = target_panel
        super(ChangePanelButton, self).__init__(normal_name, touch_name, *group)

    def change_panel(self):
        return self.target_panel


class StatusButton(Button):

    def __init__(self, image_names, press_names, *groups):
        super(StatusButton, self).__init__(image_names[0], press_names[0], *groups)
        # 0是暂停图片，1是继续图片,加载图片
        self.images = [pygame.image.load(self.res_path + name) for name in image_names]
        self.press_name = press_names[1]
        self.normal_names = image_names

    def switch_pause_continue(self, is_pause):
        self.image = self.images[1 if is_pause else 0]

    def switch_status(self):
        self.images[1] = pygame.image.load(self.res_path + self.press_name) \
            if self.is_touch else \
            pygame.image.load(self.res_path + self.normal_names[1])


class slideBlock(GameSprite):
    def __init__(self, normal_name, *group):
        self.move = 1
        self.is_touch = 0
        super(slideBlock, self).__init__(normal_name, *group)

    def update(self, rect, *args):
        if not self.move:
            return
        if 755 >= rect.centerx >= 205:
            self.rect.centerx = round(rect.centerx, 0)


class Mouse(pygame.sprite.Sprite):

    def __init__(self, *group):
        super(Mouse, self).__init__(*group)
        self.image = pygame.Surface((1, 1))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()  # 初始位置到鼠标指针

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # 移到鼠标指针位置
