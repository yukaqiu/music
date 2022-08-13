import pygame
from game_items import *
import os
import csv
import numpy as np





class MUSIC_SCORES(object):

    def __init__(self, display_group):
        self.SPEED = speed_class.get_speed()
        self.music_path = 'xxx'
        self.music_score = []
        self.track_all = [[], [], [], [], [], []]
        self.music_time = []
        self.level_score = [0, 0, 0, 0, 0]
        self.line = 0
        self.combo = 0
        self.max_combo = 0
        self.bpm = 0
        self.ms = 0
        self.show_time = 0

        self.display_group = display_group
        self.perfect_level_sprite = GameSprite("game/perfect.png")
        self.perfect_level_sprite.rect.center = SCREEN_RECT.center
        self.great_level_sprite = GameSprite("game/great.png")
        self.great_level_sprite.rect.center = SCREEN_RECT.center
        self.good_level_sprite = GameSprite("game/good.png")
        self.good_level_sprite.rect.center = SCREEN_RECT.center
        self.bad_level_sprite = GameSprite("game/bad.png")
        self.bad_level_sprite.rect.center = SCREEN_RECT.center
        self.miss_level_sprite = GameSprite("game/miss.png")
        self.miss_level_sprite.rect.center = SCREEN_RECT.center

        self.combo_label = Label('x %d \n combo' % self.combo, 70, white, 'MarkerFelt.ttf')
        self.combo_label.rect.centerx = SCREEN_RECT.centerx
        self.combo_label.rect.centery = SCREEN_RECT.centery + 100
        self.combo_string_label = Label('combo', 40, white, 'MarkerFelt.ttf')
        self.combo_string_label.rect.centery = self.combo_label.rect.centery + 50
        self.combo_string_label.rect.centerx = self.combo_label.rect.centerx

    def read_music_score(self):

        with open("data/music_scores/" + str(self.music_path), "r") as csvfile:
            reader = csv.reader(csvfile)
            rows = []
            for row in reader:
                rows.append(row)

            self.bpm = int(rows[0][0])
            self.ms = 60 / self.bpm * 1000
            for i in range(1, len(rows)):

                self.music_score.append([float(rows[i][0]), int(rows[i][1]), int(rows[i][2])])
                self.music_time.append(i)

    def load_note(self, moment):
        # 中间的图片，最长显示不超过八十帧
        self.show_time += 1
        if self.show_time > 80:
            self.display_group.remove(self.perfect_level_sprite, self.great_level_sprite, self.good_level_sprite,
                                      self.bad_level_sprite, self.miss_level_sprite)
            self.show_time = 0
        # 根据秒数加载按键
        if self.line < len(self.music_score):
            appear_time = self.music_score[self.line][0] * self.ms - self.SPEED
            # 利用帧数判断节点出现应该在第几帧
            if moment > appear_time:
                self.music_score[self.line].append(Note(float(appear_time),
                                                        int(self.music_score[self.line][1]),
                                                        int(self.music_score[self.line][2])))

                self.music_score[self.line][0] = appear_time
                self.display_group.add(self.music_score[self.line][3])
                self.track_all[self.music_score[self.line][2] - 1].append(
                    [self.music_time[self.line], appear_time])
                self.line += 1
            return False
        # 最后一个按键出现后约4.8秒后自动切换界面
        elif self.line < len(self.music_score) + 300:
            self.line += 1
            return False
        else:

            return True

    def judge_time(self, time, track=0):

        if self.combo == 3:
            self.display_group.add(self.combo_label, self.combo_string_label)

        for track_one in self.track_all:
            if track_one == []:
                continue
            # 换算应该触碰时间
            touch_time = track_one[0][1] + self.SPEED
            # 如果超出133ms，判定miss

            if time - touch_time >= 200:
                index = self.music_time.index(track_one[0][0])

                self.music_score.pop(index)
                self.music_time.pop(index)
                track_one.pop(0)

                self.level_score[4] += 1
                self.line -= 1

                self.max_combo = self.combo if self.combo > self.max_combo else self.max_combo
                self.combo = 0
                self.display_group.remove(self.combo_label, self.combo_string_label)

                self.display_group.image = pygame.image.load("picture/game/miss.png")
                self.show_level_sprite(self.miss_level_sprite)

        # 没有按键直接返回
        if track == 0:
            return

        # 如果有按键的情况
        if self.track_all[track - 1] == []:
            return
        touch_time = self.track_all[track - 1][0][1] + self.SPEED
        index = self.music_time.index(self.track_all[track - 1][0][0])
        if -50.0 < time - touch_time < 70.0:
            self.combo += 1
            self.combo_label.set_text('x %d' % self.combo)
            self.combo_label.rect.centerx = SCREEN_RECT.centerx
            self.combo_label.rect.centery = SCREEN_RECT.centery + 100
            self.level_score[0] += 1
            self.show_level_sprite(self.perfect_level_sprite)
        elif -100.0 < time - touch_time < 120.0:
            self.combo += 1
            self.combo_label.set_text('x %d' % self.combo)
            self.combo_label.rect.centerx = SCREEN_RECT.centerx
            self.combo_label.rect.centery = SCREEN_RECT.centery + 100
            self.level_score[1] += 1
            self.music_score[index][3].press_names = ["game/blue_note_%d.png" % i for i in range(1, 9)]
            self.show_level_sprite(self.great_level_sprite)
        elif -140.0 < time - touch_time < 150.0:
            self.combo = 0
            self.display_group.remove(self.combo_label, self.combo_string_label)
            self.level_score[2] += 1
            self.music_score[index][3].press_names = ["game/blue_note_%d.png" % i for i in range(1, 6)]
            self.show_level_sprite(self.good_level_sprite)
        elif -180.0 < time - touch_time < 200.0:
            self.combo = 0
            self.display_group.remove(self.combo_label, self.combo_string_label)
            self.level_score[3] += 1
            self.music_score[index][3].press_names = ["game/blue_note_%d.png" % i for i in range(1, 6)]
            self.show_level_sprite(self.bad_level_sprite)
        else:  # 不在判定范围之内
            return
        self.max_combo = self.combo if self.combo > self.max_combo else self.max_combo
        self.line -= 1
        self.music_score[index][3].is_press = 1
        self.music_score.pop(index)
        self.music_time.pop(index)
        self.track_all[track - 1].pop(0)

    def show_level_sprite(self, sprite):

        self.display_group.remove(self.perfect_level_sprite, self.great_level_sprite, self.good_level_sprite,
                                  self.bad_level_sprite, self.miss_level_sprite)
        self.display_group.add(sprite)
        self.show_time = 0
