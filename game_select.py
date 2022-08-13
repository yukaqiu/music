import pygame
import csv
from game_items import *


class SELECTPanel(object):
    music_scores_folder = 'data/music_scores'
    record_filename = 'data/record.csv'

    def __init__(self, display_group):
        # 基本数据
        self.music_list = []
        self.best_score = 0
        self.music_name = 'xxxxxx'
        self.music_path = "xxx"
        self.page = 0
        self.display_group = display_group

        for item in self.display_group:
            self.display_group.remove(item)
            
        # 获取乐曲名字列表
        self.load_music_list()

        i = 0
        for music_detail in self.music_list[0:6]:
            self.set_music_item(music_detail, i)
            i = i + 1
        if len(self.music_list)<6:
            self.set_arrow_page(0, 0)
        else:
            self.set_arrow_page(0, 1)

        back_button = ChangePanelButton("select/back.png", "select/back_touch.png", "login", self.display_group)
        back_button.rect.center = (36, 36)

    def load_music_list(self):
        with open(self.record_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for rows in reader:
                if "" in rows:
                    continue
                self.music_list.append(rows[0:4])

    def update_music_list(self, num):
        self.page += num

        if self.page < 0:
            self.page = 0
        elif self.page > len(self.music_list) // 6:
            self.page -= 1

        for item in self.display_group:
            self.display_group.remove(item)

        i = 0
        for music_detail in self.music_list[0 + self.page * 6: 6 + self.page * 6]:
            self.set_music_item(music_detail, i)
            i = i + 1

        if self.page == 0 and len(self.music_list) <= 6:
            self.set_arrow_page(0, 0)
        elif self.page == 0 and len(self.music_list) > 6:
            self.set_arrow_page(0, 1)
        elif self.page == len(self.music_list) // 6:
            self.set_arrow_page(1, 0)
        else:
            self.set_arrow_page(1, 1)
        back_button = ChangePanelButton("select/back.png", "select/back_touch.png", "login", self.display_group)
        back_button.rect.center = (36, 36)

    def set_arrow_page(self, left, right):
        # left and right == 1 or 0 ,if is 1,set a arrow
        if left:
            left_arrow = ArrowButton("select/left_arrow.png", "select/left_arrow_touch.png", -1, self.display_group)
            left_arrow.rect.center = (SCREEN_RECT.width / 2 - 30, SCREEN_RECT.height - 30)
        if right:
            right_arrow = ArrowButton("select/right_arrow.png", "select/right_arrow_touch.png", 1, self.display_group)
            right_arrow.rect.center = (SCREEN_RECT.width / 2 + 60, SCREEN_RECT.height - 30)

        music_list_page_label = Label('%s' % (self.page + 1), 20, black, 'HGDBS_CNKI.TTF', self.display_group)
        music_list_page_label.rect.center = (SCREEN_RECT.width / 2 + 15, SCREEN_RECT.height - 30)

    def set_music_item(self, music_detail, i):
        # music_detail => "music_name", is fc

        if int(music_detail[1]):
            music_item_bg = MusicListButton("select/music_item_fc_bg.png", "select/music_item_fc_bg_touch.png",
                                            music_detail[2], music_detail[3], music_detail[0], self.display_group)
        else:
            music_item_bg = MusicListButton("select/music_item_bg.png", "select/music_item_bg_touch.png",
                                            music_detail[2], music_detail[3],music_detail[0],self.display_group)
        music_item_bg.rect.center = (
            (SCREEN_RECT.width - 100) / 2 * (i // 3 + 1) - 150, (SCREEN_RECT.height - 110) / 3 * (i % 3 + 1))

        music_name_label = Label(('%s' % music_detail[0])[0:20], 25, black, 'HGDBS_CNKI.TTF', self.display_group)
        music_name_label.rect.center = (
            (SCREEN_RECT.width - 100) / 2 * (i // 3 + 1) - 150, (SCREEN_RECT.height - 110) / 3 * (i % 3 + 1))
