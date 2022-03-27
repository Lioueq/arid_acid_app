import pygame
import pygame_gui
from random import choice
from vars import from_russian_letters_id_to_english_letters_id_capslock_off


COLORS = [i for i in range(255)]


def color():
    return choice(COLORS), choice(COLORS), choice(COLORS)


class Game:
    def __init__(self):
        self.SIZE = 900, 600
        self.TEXT_POS = 120, 250
        self.FPS = 30
        self.BACKGROUND = pygame.Color('#08592e')
        self.TEXT_COLOR = pygame.Color('#b383dd')
        self.CAPS_LOCK = False
        self.count = 0
        self.is_running = True
        pygame.init()
        self.clock = pygame.time.Clock()
        game_icon = pygame.image.load('data/icon2.png')
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption('Need for nicotine')
        self.screen = pygame.display.set_mode(self.SIZE)
        with open('words.txt', encoding='utf-8') as file:
            unstripped_words_couples = file.readlines()
            self.words_couples = [i.rstrip('\n') for i in unstripped_words_couples]

    def choice_word_couple(self):
        self.word_couple = choice(self.words_couples)

    def render_text(self):
        font = pygame.font.SysFont('cera pro', 65)
        text = font.render(self.word_couple, True, self.TEXT_COLOR)
        text_under = font.render(self.word_couple[:self.count], True, pygame.Color(250, 167, 0))
        self.screen.blit(text, self.TEXT_POS)
        self.screen.blit(text_under, self.TEXT_POS)
        pygame.display.update()

    def main_window_scene(self):
        manager = pygame_gui.UIManager(self.SIZE, 'data/theme.json')
        background = pygame.Surface(self.SIZE)
        background.fill(self.BACKGROUND)
        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (150, 75)),
                                                    text='START',
                                                    manager=manager)
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        self.write_word_scene()
                manager.process_events(event)
            manager.update(time_delta)
            self.screen.blit(background, (0, 0))
            manager.draw_ui(self.screen)
            pygame.display.update()

    def write_word_scene(self):
        self.choice_word_couple()
        while self.is_running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.MOUSEMOTION:
                    print(pygame.mouse.get_pos())
                    pass
                # KEYBOARD EVENTS
                if event.type == pygame.KEYDOWN:
                    need_button = pygame.key.key_code(self.word_couple[self.count])  # NEED_BUTTON_ID
                    '''Если буква русская, то ее id заменяют на id той буквы, с которой она находиться на клавиатуре
                       Прописана логика для CAPSLOCK'''
                    if need_button in from_russian_letters_id_to_english_letters_id_capslock_off.keys():
                        need_button = from_russian_letters_id_to_english_letters_id_capslock_off[need_button]
                    keys = pygame.key.get_pressed()
                    #  ПРОВЕРКА НА НАЖАТИЕ ID ТОЙ БУКВЫ, ЧТО УКАЗАНА В ТЕКСТЕ
                    if keys[need_button] or keys[pygame.K_RALT]:
                        self.count += 1
            #  RESET
            if self.count == len(self.word_couple):
                self.count = 0
                self.choice_word_couple()
            self.screen.fill(self.BACKGROUND)
            self.render_text()
            pygame.display.flip()


Game().main_window_scene()
