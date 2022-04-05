import pygame
import pygame_gui
import time
from random import choice
from vars import from_russian_letters_id_to_english_letters_id_capslock_off, cera_pro_book_size
from kreekly_com_parser import word_couples_updater


class Game:
    def __init__(self):
        pygame.init()
        self.SIZE = 900, 600
        self.TEXT_POS = 120, 250
        self.FPS = 30
        self.BACKGROUND = pygame.Color('#08592e')
        self.TEXT_COLOR = pygame.Color('#b383dd')
        self.FONT = pygame.font.Font('data/cera_pro_fonts_forms/CeraPro-Regular.ttf', 60)
        self.error = False
        self.shift = 0
        self.count = 0
        self.is_running = True
        self.clock = pygame.time.Clock()
        game_icon = pygame.image.load('data/images/icon2.png')
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption('Need for nicotine')
        self.screen = pygame.display.set_mode(self.SIZE)
        with open('data/word_couples.txt', encoding='utf-8') as file:
            unstripped_words_couples = file.readlines()
            self.words_couples = [i.rstrip('\n') for i in unstripped_words_couples]

    def choice_word_couple(self):
        self.word_couple = choice(self.words_couples)

    def reset(self):
        self.choice_word_couple()
        self.count = 0
        self.shift = 0
        self.error = False

    def render_text(self):
        # text to write
        text = self.FONT.render(self.word_couple, True, self.TEXT_COLOR)
        text_under = self.FONT.render(self.word_couple[:self.count], True, pygame.Color(250, 167, 0))
        # text with error number
        # text_error = self.FONT.render(f'Количество ошибок: {self.error_count}', True, pygame.Color(250, 167, 0))
        self.screen.blit(text, self.TEXT_POS)
        self.screen.blit(text_under, self.TEXT_POS)
        # self.screen.blit(text_error, (self.TEXT_POS[0], self.TEXT_POS[1] + 100))
        pygame.display.update()

    def render_subline(self):
        subline = pygame.Surface((cera_pro_book_size[self.word_couple[self.count]], 4))
        if self.error:
            subline.fill(pygame.Color('red'))
        else:
            subline.fill(pygame.Color(250, 167, 0))
        self.screen.blit(subline, (self.TEXT_POS[0] + self.shift + 5 * self.count,
                                   self.TEXT_POS[1] + 65))

    def render_time_text(self, time_delta):
        time_text = self.FONT.render(f'Осталось времени: {int(60 - time_delta)}', True, pygame.Color(250, 167, 0))
        self.screen.blit(time_text, (140, 50))

    def render_end_game_text_right_couples_count(self, count):
        time_text = self.FONT.render(f'Ваш итоговый счёт: {count}', True, pygame.Color(250, 167, 0))
        self.screen.blit(time_text, (140, 50))

    def render_end_game_text_error_count(self):
        time_text = self.FONT.render(f'Кол-во ошибок: {self.error_count}', True, pygame.Color(250, 167, 0))
        self.screen.blit(time_text, (140, 125))

    def main_window_scene(self):
        manager = pygame_gui.UIManager(self.SIZE, 'data/theme.json')
        background = pygame.Surface(self.SIZE)
        background.fill(self.BACKGROUND)
        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (150, 75)),
                                                    text='START',
                                                    manager=manager)
        update_couples_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 350), (150, 75)),
                                                             text='UPDATE WORDS',
                                                             manager=manager)
        self.reset()
        self.error_count = 0
        while self.is_running:
            time_delta = self.clock.tick(self.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        self.write_word_scene()
                    elif event.ui_element == update_couples_button:
                        word_couples_updater()
                manager.process_events(event)
            manager.update(time_delta)
            self.screen.blit(background, (0, 0))
            manager.draw_ui(self.screen)
            pygame.display.update()

    def write_word_scene(self):
        start_time = time.time()
        right_word_couples_count = 0
        self.reset()
        self.error_count = 0
        while self.is_running:
            self.clock.tick(self.FPS)
            time_delta = time.time() - start_time
            if int(time_delta) == 60:
                self.end_game_scene(right_word_couples_count)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                # KEYBOARD EVENTS
                if event.type == pygame.KEYDOWN:
                    need_button = pygame.key.key_code(self.word_couple[self.count])  # NEED_BUTTON_ID
                    '''Если буква русская, то ее id заменяют на id той буквы, с которой она находиться на клавиатуре
                       Прописана логика для CAPSLOCK'''
                    if need_button in from_russian_letters_id_to_english_letters_id_capslock_off.keys():
                        need_button = from_russian_letters_id_to_english_letters_id_capslock_off[need_button]
                    keys = pygame.key.get_pressed()
                    #  ПРОВЕРКА НА НАЖАТИЕ ID ТОЙ БУКВЫ, ЧТО УКАЗАНА В ТЕКСТЕ
                    if keys[need_button]:
                        self.shift += cera_pro_book_size[self.word_couple[self.count]]
                        self.count += 1
                        self.error = False
                    elif keys[8]:
                        self.count = len(self.word_couple)
                    elif not keys[need_button] and (event.key != pygame.K_LSHIFT and event.key != pygame.K_LALT):
                        self.error = True
                        self.error_count += 1
            #  RESET
            if self.count == len(self.word_couple):
                right_word_couples_count += 1
                self.reset()
            self.screen.fill(self.BACKGROUND)
            self.render_subline()
            self.render_time_text(time_delta)
            self.render_text()
            pygame.display.flip()

    def end_game_scene(self, right_word_couples_count):
        manager = pygame_gui.UIManager(self.SIZE, 'data/theme.json')
        restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 200), (150, 75)),
                                                      text='RESTART',
                                                      manager=manager)
        exit_to_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (150, 75)),
                                                           text='EXIT TO MENU',
                                                           manager=manager)
        while self.is_running:
            time_delta = self.clock.tick(self.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        self.write_word_scene()
                    elif event.ui_element == exit_to_menu_button:
                        self.main_window_scene()
                manager.process_events(event)
            manager.update(time_delta)
            self.screen.fill(self.BACKGROUND)
            manager.draw_ui(self.screen)
            self.render_end_game_text_error_count()
            self.render_end_game_text_right_couples_count(right_word_couples_count)
            pygame.display.flip()


Game().main_window_scene()
