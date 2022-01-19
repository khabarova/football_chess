import pygame
import sys

# from All_levels import Level
pygame.font.init()
# from pygame import display

size = width, height = (500, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
k = 0


class Button():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inact_col = (13, 162, 58)
        self.active_col = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_col, (x, y, self.width, self.height))
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        else:
            pygame.draw.rect(screen, self.inact_col, (x, y, self.width, self.height))
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def menu():
    menu_back = pygame.image.load('data/fon1.jpg')
    start_btn = Button(300, 70)
    text_btn = Button(300, 70)
    quit_btn = Button(300, 70)
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill("black")
        screen.blit(menu_back, (0, 0))
        print("1")
        start_btn.draw(350, 100, 'Start game', level_1)
        text_btn.draw(350, 200, 'Rules', rules)
        quit_btn.draw(400, 300, 'Quit', quit)
        pygame.display.update()
        clock.tick(60)


def rules():
    menu_back = pygame.image.load('fon2.jpg')
    # в это функии мы выводим правила с помощью работы с файлами
    screen.fill('black')
    pygame.display.set_caption("Rules")
    # создаем кнопку возвращения, чтобы после прочтения правил можно было вернуться в главное меню
    return_button = pygame.draw.rect(screen, (57, 255, 20), (150, 400, 150, 100))
    screen.blit(menu_back, (0, 0))
    document = open('pravila_DE.txt', encoding='utf8')
    document2 = document.readlines()
    y = 0
    # работа с файлом
    for el in document2:
        el = el.replace('\n', '')
        font = pygame.font.SysFont('Arial', 20)
        txt = font.render(el, True, (57, 255, 20))
        text = font.render("Вернуться в меню", True, [250, 250, 250])
        screen.blit(txt, (215, y))
        screen.blit(text, (150, 440))

        y += 20
    pygame.display.update()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 >= pygame.mouse.get_pos()[0] >= 150 and 500 >= pygame.mouse.get_pos()[1] >= 400:
                    # запускаем функцию создания меню
                    # делаем это через создание нового элемента класса
                    menu()


def print_text(message, x, y, font_color=(255, 255, 255), font_type='arial', font_size=30):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# загрузка картинок
def load_image(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image:', name)
        raise SystemExit()

    return image


# КОД ЛИИ

# выход из проги
def terminate():
    pygame.quit()
    sys.exit()


# загрузка уровня
def load_level(name):
    fullname = "data/" + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map


# составляющие файла с уровнем
def draw_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('grass.png', x, y)
            elif level_map[y][x] == '#':
                Tile('stones.png', x, y)
                dragon = Dragon(x, y)
            #     тот кто ищет(пользователь)
            elif level_map[y][x] == '@':
                Tile('grass.png', x, y)
                new_player = Player(x, y)
            #     то что нужно найти будет обозначен на карте уровня знаком "&"
            elif level_map[y][x] == '&':
                Tile('grass.png', x, y)
                morty = Morty(x, y)
            elif level_map[y][x] == '%':
                Tile('grass.png', x, y)
                bottle = Bottle(x, y)
    return new_player, x, y, dragon, morty, bottle


# тайлы
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

        if tile_type == 'дракон.png':
            self.add(dragon_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('рик.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(player_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        self.rect = self.rect.move(+50, 0)

    # класс препятствия


class Bottle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('bottle.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(bottle_group, all_sprites)


# класс того что ищут
class Morty(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('морти.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(morty_group, all_sprites)


# непроходимое препятствие
class Dragon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('дракон.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(dragon_group, all_sprites)


# особый класс камеры, которая будет постоянно
# рисовать нашего героя в центре уровня,
# следя за его координатами и пересчитывая их
class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # метод пересчёта координат спрайтов всех тайлов,
    # всключая тайл того кем играют
    def apply(self, obj):
        obj.rect.x += self.dx

        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width

        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy

        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # метод пересчёта координат гг
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
dragon_group = pygame.sprite.Group()
bottle_group = pygame.sprite.Group()
morty_group = pygame.sprite.Group()


# 1 уровень
def level_1():
    player, level_x, level_y, bottle, morty, dragon = draw_level(load_level("level_1.txt"))
    camera = Camera((level_x, level_y))
    k = 0

    # проверка на проход через дракона
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_left()

            if event.type == pygame.QUIT:
                terminate()

        # обновление камеры
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        # рисование если игрок не наступил на бутылку
        # if not pygame.sprite.groupcollide(player_group, bottle_group, False, False):
        #     screen.fill(pygame.Color(0, 0, 0))
        #     tiles_group.draw(screen)
        #     player_group.draw(screen)
        #     bottle_group.draw(screen)
        #     morty_group.draw(screen)
        #     dragon_group.draw(screen)

        # иначе игра завершается
        if pygame.sprite.groupcollide(player_group, bottle_group, False, True):
            k += 1
            print(k)
            gameover = load_image('gg.jpg')
            screen.blit(gameover, (-190, -200))

        if not pygame.sprite.collide_rect(player, morty):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            morty_group.draw(screen)
            dragon_group.draw(screen)
            bottle_group.draw(screen)

        if pygame.sprite.collide_rect(player, morty):
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            morty_group.empty()
            bottle_group.empty()
            dragon_group.empty()
            return level_2()

        pygame.display.flip()
        clock.tick(fps)


def level_2():
    player, level_x, level_y, bottle, morty, dragon = draw_level(load_level("level_2.txt"))
    camera = Camera((level_x, level_y))
    k = 0

    # проверка на проход через дракона
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_left()

            if event.type == pygame.QUIT:
                terminate()

        # обновление камеры
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        # иначе игра завершается
        if pygame.sprite.groupcollide(player_group, bottle_group, False, True):
            k += 1
            print(k)
            gameover = load_image('gg.jpg')
            screen.blit(gameover, (-190, -200))

        if not pygame.sprite.collide_rect(player, morty):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            morty_group.draw(screen)
            dragon_group.draw(screen)
            bottle_group.draw(screen)

        if pygame.sprite.collide_rect(player, morty):
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            morty_group.empty()
            bottle_group.empty()
            dragon_group.empty()
            return level_3()

        pygame.display.flip()
        clock.tick(fps)


# 3 уровень
def level_3():
    # тоже самое, что и в 1 уровне
    player, level_x, level_y, bottle, morty, dragon = draw_level(load_level("level_3.txt"))
    camera = Camera((level_x, level_y))
    k = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, dragon_group):
                    player.move_left()

            if event.type == pygame.QUIT:
                terminate()

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        if pygame.sprite.groupcollide(player_group, bottle_group, False, True):
            k += 1
            print(k)

        if not pygame.sprite.collide_rect(player, morty):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            morty_group.draw(screen)
            dragon_group.draw(screen)
            bottle_group.draw(screen)

        else:
            gameover = load_image('gg.jpg')
            screen.blit(gameover, (-190, -200))

        pygame.display.flip()
        clock.tick(fps)


menu()

terminate()
