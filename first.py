import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)

def draw_intro():
    img = pygame.image.load('data/og_image.jpg')
    font = pygame.font.SysFont("stxingkai", 70)
    text = font.render("Приветствую вас в", True, (255, 255, 255))
    text2 = font.render("футбольном симуляторе", True, (255, 255, 255))
    name = "Введите название команды"
    find_name = False
    while not find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == "Введите название команды":
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        find_name = True
                        break

        screen.fill(BLACK)
        text_name = font.render(name, True, (255, 255, 255))
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img, [200, 200]), [10, 10])
        screen.blit(text, (230, 80))
        screen.blit(text2, (230, 120))
        screen.blit(text_name, rect_name)
        pygame.display.update()

draw_intro()


while True:

    pygame.display.update()
    clock.tick(60)
