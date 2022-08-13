import pygame
import csv
from game_items import *


class SUMPanel(object):
    record_filename = 'data/record.csv'
    summary_folder = 'summary/'

    def __init__(self, display_group):
        # 背景
        self.summary_bg = GameSprite(self.summary_folder + "sum_bg.png", display_group)
        self.display_group = display_group
        # 基本数据
        self.score = 0
        self.best_score = 0
        self.level_score = [0, 0, 0, 0, 0]
        self.level_score_label = []
        self.level_image_sprite = []

        self.music_name = 'xxx！'
        self.combo = 0

        # 乐曲名字
        self.music_name_label = Label('%s' % self.music_name, 25, white, 'HGDBS_CNKI.TTF', display_group)

        # 本次等级图片
        self.score_image = GameSprite(self.summary_folder + "d_rank.png", display_group)
        self.score_image.rect.center = (220,260)

        # 本次成绩&最好成绩的得分和文字标签
        self.score_label = Label('%d %%' % self.score, 33, black, 'MarkerFelt.ttf', display_group)
        self.best_score_label = Label('%d %%' % self.best_score, 25, gray, 'MarkerFelt.ttf', display_group)

        # 五个等级们
        self.set_five_level_image(display_group)
        for i in range(5):
            self.level_score_label.append(Label('%d' % self.level_score[i], 30, black, 'MarkerFelt.ttf', display_group))

        # combo数
        self.combo_label = Label('%04d' % self.combo, 40, black, 'MarkerFelt.ttf', display_group)

        # fc_image
        self.fc_image = GameSprite(self.summary_folder + "fc_image.png", display_group)
        self.fc_image.rect.center = (880,335)

        # next_button
        self.next_button = GameSprite(self.summary_folder + "next_button.png", display_group)
        self.next_button.rect.center = (840,510)

    def increase_score(self,level_score):
        # 赋值各个等级分
        self.level_score = level_score
        total_note = sum(self.level_score)
        # 计算最新得分
        score = (self.level_score[0] * 100 + self.level_score[1] * 85 + self.level_score[2] * 75 + self.level_score[3] * 50) / total_note
        # 更新总分等级图片
        if score > 95:
            self.score_image.image = pygame.image.load("picture/summary/s_rank.png")
        elif score >80:
            self.score_image.image = pygame.image.load("picture/summary/a_rank.png")
        elif score > 60:
            self.score_image.image = pygame.image.load("picture/summary/b_rank.png")
        elif score > 40:
            self.score_image.image = pygame.image.load("picture/summary/c_rank.png")

        #     更新combo
        self.combo_label.set_text('%04d' % self.combo)
        self.combo_label.rect.center = (835, SCREEN_RECT.centery + 37)

        #     是否fc
        if total_note == self.combo:
            self.save_best_score(1)
            self.display_group.add(self.fc_image)
        else:
            self.display_group.remove(self.fc_image)

        # 更新最好成绩
        self.load_best_score()
        if score > self.best_score:
            self.best_score = score
            self.save_best_score()

        # 最好得分显示位置
        self.score_label.set_text('%.2f %%' % score)
        self.score_label.rect.midright = (370, 447)

        self.best_score_label.set_text('%.2f %%' % self.best_score)
        self.best_score_label.rect.midright = (370, 508)



        # 各个level数更新
        for i in range(5):
            self.level_score_label[i].set_text('%d' % self.level_score[i])
            self.level_score_label[i].rect.midright = (
                self.level_image_sprite[i].rect.right + 80, self.level_image_sprite[i].rect.centery + 5)
        # 曲名更新
        self.music_name_label.set_text('%s' % self.music_name)
        self.music_name_label.rect.midleft = (15, 75)



    def set_five_level_image(self, display_group):

        image_list = ["perfect", "great", "good", "bad", "miss"]
        i = 0
        for image in image_list:
            self.level_image_sprite.append(GameSprite(self.summary_folder + image + ".png", display_group))
            self.level_image_sprite[i].rect.midleft = (450, 170 + 60 * i)
            i += 1

    def save_best_score(self, fc=0):
        # 保存最好得分记录
        data = []
        with open(self.record_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                data.append(row)
                if row[0] == self.music_name:
                    data[i][4] = self.best_score
                    if fc:
                        data[i][1] = 1


        with open(self.record_filename, "w",newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def load_best_score(self):
        with open(self.record_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if self.music_name == row[0]:
                    self.best_score = float(row[4])

