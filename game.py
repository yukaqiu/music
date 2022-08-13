import pygame
from game_items import *
from game_hud import *
from game_login import *
from game_select import *
from game_summary import *
from music_score import *
from login_setting import *
from game_music import *
import csv

FRAME_INTERVAL = 2


class Game(object):
    # 游戏核心类

    def __init__(self):
        self.bpm = 0
        self.line = 0
        self.music_name = 'xxx'
        self.music_item = []
        self.frame_count = 0
        self.t_list = [[], [], [], [], [], []]
        self.level_score = [0, 0, 0, 0, 0]
        # 游戏窗口
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("enjoy music!")

        # 游戏状态
        self.is_login_interface = True  # 是否为游戏首页
        self.is_setting = False # 是否在游戏设置
        self.is_select_interface = False  # 是否为游戏选曲界面
        self.is_game_interface = False  # 是否为游戏界面
        self.is_game_over = False  # 是否为正在游戏
        self.is_game_pause = False  # 是否为暂停游戏
        self.is_summary_interface = False  # 是否为结算界面

        # 音乐播放器

        # 游戏精灵组
        self.all_group = pygame.sprite.Group()  # 存放所有精灵
        self.login_bg_group = pygame.sprite.Group()
        self.login_button_group = pygame.sprite.Group()
        self.select_interface_group = pygame.sprite.Group()
        self.music_list_group = pygame.sprite.Group()
        self.game_interface_group = pygame.sprite.Group()
        self.summary_interface_group = pygame.sprite.Group()
        self.status_group = pygame.sprite.Group()
        self.note_group = pygame.sprite.Group()  # 存放音符
        self.setting_group = pygame.sprite.Group()
        # self.
        # 游戏面板
        self.login_panel = LOGINGPanel(self.login_button_group)
        self.select_panel = SELECTPanel(self.music_list_group)
        self.music_score = MUSIC_SCORES(self.note_group)
        self.hub_panel = HUDPanel(self.status_group)
        self.login_setting_panel = LOGINGSettingPanel(self.setting_group)
        # 登录界面背景
        self.login_bg_group.add(Login_Background(True), Login_Background(False))
        # 选曲背景
        GameSprite("select/select_bg.png", self.select_interface_group)
        # 游戏背景
        GameSprite("game/game_bg.png", self.game_interface_group)
        # 暂停灰幕
        # self.gray_panel = GameSprite("game/gray_panel.png",self.game_interface_group)
        #   鼠标精灵方便判定碰撞
        self.mouse = Mouse()

    def start(self):
        """游戏主逻辑"""
        # 时钟
        clock = pygame.time.Clock()

        while True:
            # 按键等事件监听包括退出按钮
            if self.event_handler:
               return

            # 如果是某一界面，执行该执行的内容
            if self.is_login_interface:  #
                self.login_bg_group.draw(self.main_window)
                self.login_bg_group.update()
                self.login_button_group.draw(self.main_window)

                self.login_setting_panel.update_volume_and_speed()

                if self.is_setting:
                    self.check_collide(self.setting_group)
                    for item in self.setting_group:
                        if str(type(item)) == "<class 'game_items.slideBlock'>" and item.is_touch:
                            item.update(self.mouse.rect)

                    self.setting_group.draw(self.main_window)
                else:
                    self.check_collide(self.login_button_group)

            elif self.is_select_interface:
                # 显示

                self.select_interface_group.draw(self.main_window)
                self.music_list_group.draw(self.main_window)
                self.music_score = MUSIC_SCORES(self.note_group)

                self.check_collide(self.music_list_group)

                for item in self.note_group:
                    self.note_group.remove(item)
                self.frame_count = 0

            elif self.is_game_interface:
                self.check_collide(self.status_group)
                if self.is_game_pause:
                    self.hub_panel.panel_pause(True)

                else:
                    self.hub_panel.panel_pause(False)
                    change = self.music_score.load_note(pygame.time.get_ticks() - self.start_time)

                    if change:
                        self.is_game_interface = False
                        self.is_summary_interface = True

                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time)
                    # 按键沿轨道移动 & 然后显示特效
                    count = (self.frame_count + 1) % FRAME_INTERVAL
                    self.note_group.update(pygame.time.get_ticks() - self.start_time, self.note_group, count == 0)
                    self.frame_count += 1

                self.game_interface_group.draw(self.main_window)
                self.note_group.draw(self.main_window)
                self.status_group.draw(self.main_window)

            elif self.is_summary_interface:
                self.summary_panel = SUMPanel(self.summary_interface_group)

                pygame.mixer.music.stop()
                self.summary_panel.combo = self.music_score.max_combo
                self.summary_panel.music_name = self.music_name
                self.summary_panel.increase_score(self.music_score.level_score)

                self.summary_interface_group.draw(self.main_window)

            self.mouse.update()
            # 刷新界面
            pygame.display.update()
            # 刷新率
            clock.tick(60)

    @property
    def event_handler(self):
        # 获取并处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # x退出按钮点击
                return True

            if self.is_login_interface:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # esc键
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # 用户按下了空格键
                    self.is_login_interface = False
                    self.is_select_interface = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                    if not self.is_setting and self.login_panel_touch_event():
                        return True
                    if self.is_setting:
                        self.setting_touch_event()
                elif event.type == pygame.MOUSEBUTTONUP :
                    for item in self.setting_group:
                        if str(type(item)) == "<class 'game_items.slideBlock'>":
                            item.is_touch = 0

            elif self.is_select_interface:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        # esc键
                        self.is_select_interface = False
                        self.is_login_interface = True
                    elif event.key == pygame.K_RIGHT:
                        self.select_panel.update_music_list(1)
                    elif event.key == pygame.K_LEFT:
                        self.select_panel.update_music_list(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.select_panel_touch_event()

            elif self.is_game_pause:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # 切换暂停游戏状态
                    self.is_game_pause = not self.is_game_pause
                    self.start_time += (pygame.time.get_ticks() - self.pause_time)
                    pygame.mixer.music.unpause()
                # 鼠标按下播放键
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.game_panel_touch_event()

            elif (not self.is_game_pause) and self.is_game_interface:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # 切换暂停游戏状态
                    self.is_game_pause = not self.is_game_pause
                    pygame.mixer.music.pause()
                    self.pause_time = pygame.time.get_ticks()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 2)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 3)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 4)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 5)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    self.music_score.judge_time(pygame.time.get_ticks() - self.start_time, 6)
                # 鼠标按下暂停键
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.game_panel_touch_event()

            elif self.is_summary_interface:
                if event.type == pygame.KEYDOWN:
                    self.select_panel = SELECTPanel(self.music_list_group)
                    self.is_summary_interface = False
                    self.is_select_interface = True

    # 碰撞检测
    def check_collide(self, sprite_group):
        #  检测碰撞
        collide_mouse = pygame.sprite.spritecollide(self.mouse, sprite_group, False,
                                                    pygame.sprite.collide_mask)
        for item in sprite_group:

            if str(type(item)) in ["<class 'game_items.MusicListButton'>",
                                   "<class 'game_items.ArrowButton'>",
                                   "<class 'game_items.ChangePanelButton'>",
                                   "<class 'game_items.StatusButton'>"]:
                if item in collide_mouse:
                    item.is_touch = 1
                else:
                    item.is_touch = 0
                item.switch_status()
        return collide_mouse

    def select_panel_touch_event(self):
        item = self.check_collide(self.music_list_group)
        if item:
            item = item[0]
            if str(type(item)) == "<class 'game_items.ArrowButton'>":
                update_page = item.touch_event()
                self.select_panel.update_music_list(update_page)
            elif str(type(item)) == "<class 'game_items.MusicListButton'>":

                music_csv_path, music_path, self.music_name = item.touch_event()
                pygame.mixer.music.load("music/" + str(music_path))
                pygame.mixer.music.play()

                self.music_score.music_path = music_csv_path
                self.music_score.read_music_score()

                self.is_select_interface = False
                self.is_game_interface = True

                self.start_time = pygame.time.get_ticks()
            elif str(type(item)) == "<class 'game_items.ChangePanelButton'>":

                self.is_select_interface = False
                self.is_login_interface = True

    def game_panel_touch_event(self):

        item = self.check_collide(self.status_group)
        if item:
            item = item[0]
            if str(type(item)) == "<class 'game_items.StatusButton'>":
                self.is_game_pause = not self.is_game_pause

                if self.is_game_pause:
                    self.pause_time = pygame.time.get_ticks()
                    pygame.mixer.music.pause()
                else:
                    self.start_time += (pygame.time.get_ticks() - self.pause_time)
                    pygame.mixer.music.unpause()

            elif str(type(item)) == "<class 'game_items.ChangePanelButton'>" and item.target_panel == "replay":
                for item in self.note_group:
                    self.note_group.remove(item)
                music_path = self.music_score.music_path
                self.music_score = MUSIC_SCORES(self.note_group)
                self.music_score.music_path = music_path
                self.music_score.read_music_score()
                self.is_game_pause = 0
                pygame.mixer.music.play()

                self.frame_count = 0
                self.start_time = pygame.time.get_ticks()

            elif str(type(item)) == "<class 'game_items.ChangePanelButton'>" and item.target_panel == "menu":
                pygame.mixer.music.stop()
                self.is_game_pause = 0
                self.is_select_interface = True
                self.is_game_interface = False

    def login_panel_touch_event(self):
        item = self.check_collide(self.login_button_group)
        if item:
            item = item[0]
            if item.target_panel == "exit":
                return True
            # elif item.target_panel == "setting":
            elif item.target_panel == "select":
                self.is_select_interface = True
                self.is_login_interface = False
            elif item.target_panel == "setting":
                self.is_setting = True

    def setting_touch_event(self):
        items = self.check_collide(self.setting_group)
        for item in items:
            if str(type(item)) == "<class 'game_items.ChangePanelButton'>" :
                if item.target_panel == "exit":
                    self.is_setting = False
            elif str(type(item)) == "<class 'game_items.slideBlock'>" :
                item.is_touch = 1

if __name__ == '__main__':
    # 初始化游戏
    pygame.init()

    # 开始游戏
    Game().start()

    # 释放游戏资源
    pygame.quit()
