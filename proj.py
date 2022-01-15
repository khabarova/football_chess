import pygame
import sys

size = width, height = (500, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

def load_image(name):
    fullname = 'data'+'/'+name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image:', name)
        raise SystemExit()
    
    return image

def terminate():
    pygame.quit()
    sys.exit()

def load_level(name):
    fullname = "data/" + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map

def draw_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('grass.png', x, y)
            elif level_map[y][x] == '#':
                Tile('stones.png', x, y)
                dragon = Dragon(x, y)
            elif level_map[y][x] == '@':
                Tile('grass.png', x, y)
                new_player = Player(x, y)
            #цветок будет обозначен на карте уровня знаком "&"
            elif level_map[y][x] == '&':
                Tile('grass.png', x, y)
                morty = Morty(x, y)
            elif level_map[y][x] == '%':
                Tile('grass.png', x, y)
                bottle = Bottle(x, y)
    return new_player, x, y, dragon, morty, bottle


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)
        
        if tile_type == 'дракон.png':
            self.add(dragon_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


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
            

class Bottle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('bottle.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(bottle_group, all_sprites)


class Morty(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('морти.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(morty_group, all_sprites)


class Dragon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('дракон.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(dragon_group, all_sprites)

#особый класс камеры, которая будет постоянно
#рисовать нашего героя в центре уровня,
#следя за его координатами и пересчитывая их
class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size
    
    #метод пересчёта координат спрайтов всех тайлов,
    #всключая тайл главного героя
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

    #метод пересчёта координат главного героя
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

        
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
dragon_group = pygame.sprite.Group()
bottle_group = pygame.sprite.Group()
morty_group = pygame.sprite.Group()


def level_1():
    player, level_x, level_y, bottle, morty, dragon = draw_level(load_level("level_2_0.txt"))
    camera = Camera((level_x, level_y))

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

        # обновление камеры (строки 158-160)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        if not pygame.sprite.groupcollide(player_group, bottle_group, False, False):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            bottle_group.draw(screen)
            morty_group.draw(screen)
            dragon_group.draw(screen)

        else:
            gameover = load_image('gameover.png')
            screen.blit(gameover, (75, 100))


        pygame.display.flip()
        clock.tick(fps)


def level_2():
    player, level_x, level_y, bottle, morty, dragon = draw_level(load_level("level_2_0.txt"))
    camera = Camera((level_x, level_y))

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

        # обновление камеры (строки 158-160)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        if not pygame.sprite.groupcollide(player_group, bottle_group, False, False):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            bottle_group.draw(screen)
            morty_group.draw(screen)
            dragon_group.draw(screen)

        else:
            gameover = load_image('gameover.png')
            screen.blit(gameover, (75, 100))


        pygame.display.flip()
        clock.tick(fps)


level_1()
level_2()

terminate()
