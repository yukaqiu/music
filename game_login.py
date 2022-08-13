import pygame
from game_items import *
import os
import csv
import numpy as np


class LOGINGPanel(object):

    def __init__(self, button_group):

        start_button = ChangePanelButton("login/start_button.png","login/start_button_touch.png","select",button_group)
        start_button.rect.center = (700,200)

        setting_button = ChangePanelButton("login/setting_button.png", "login/setting_button_touch.png", "setting",button_group)
        setting_button.rect.center = (700,330)

        exit_button = ChangePanelButton("login/exit_button.png", "login/exit_button_touch.png", "exit",button_group)
        exit_button.rect.center = (700,460)


class Login_Background(GameSprite):
    def __init__(self, is_alt, *group):
        super(Login_Background, self).__init__("login/login_bg.png", *group)
        if is_alt:
            self.rect.y = SCREEN_RECT.h

    def update(self, *args):
        super(Login_Background, self).update(*args)
        self.rect.y -= 1

        if self.rect.y < -SCREEN_RECT.h:
            self.rect.y = SCREEN_RECT.h
