import pygame
from game_items import *
import os
import csv
import numpy as np


class LOGINGSettingPanel(object):

    def __init__(self, display_group):
        self.volume = 100
        self.speed = 0

        GameSprite("login/setting.png", display_group)
        self.setting_exit_button = ChangePanelButton("login/setting_exit_button.png", "login/setting_exit_button_touch"
                                                                                      ".png", "exit", display_group)
        self.setting_exit_button.rect.center = (480, 420)

        self.voice_slide_gray = GameSprite("login/slide_gray.png", display_group)
        self.voice_slide_color = GameSprite("login/slide_color.png", display_group)

        self.speed_slide_gray = GameSprite("login/slide_gray.png", display_group)
        self.speed_slide_color = GameSprite("login/slide_color.png", display_group)

        self.voice_slide_gray.rect.center = (480, 215)
        self.voice_slide_color.rect.center = (480, 215)

        self.speed_slide_gray.rect.center = (480, 360)
        self.speed_slide_color.rect.center = (480, 360)

        self.voice_slide_block = slideBlock("login/slide_block.png", display_group)
        self.speed_slide_block = slideBlock("login/slide_block.png", display_group)

        self.voice_slide_block.rect.center = (480, 215)
        self.speed_slide_block.rect.center = (480, 360)

        self.voice_label = Label('%s' % self.volume, 25, black, 'HGDBS_CNKI.TTF', display_group)
        self.speed_label = Label('%s' % self.volume, 25, black, 'HGDBS_CNKI.TTF', display_group)

    def update_volume_and_speed(self):
        volume = round((self.voice_slide_block.rect.centerx - 205) / (755 - 205), 2)
        pygame.mixer.music.set_volume(volume)

        speed_i = round((self.speed_slide_block.rect.centerx - 205) / 46, 0)
        self.speed_slide_block.rect.centerx = speed_i * 46 + 205
        self.speed = speed_i * 0.5 + 8
        speed_class.set_speed((22 - self.speed) * 100)

        self.voice_label.set_text('%.0f' % (volume * 100))
        self.voice_label.rect.center = (480, 170)

        self.speed_label.set_text('%.1f' % self.speed)
        self.speed_label.rect.center = (480, 315)
