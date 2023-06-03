import math
import pygame
from FG_model import *
import random

pygame.init()
pygame.font.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("farming game")

bg_img = pygame.image.load("images/background.png")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

cursor = pygame.mouse.get_pos()


class Tool:
    def __init__(self, name, pos_x=400, posy=300, is_active=False):
        self.name = name
        self.pos_x = pos_x
        self.posy = posy
        self.is_active = is_active

    def mouse_locate(self):
        self.pos_x = cursor[0]
        self.posy = cursor[1]


class Seed:
    def __init__(self, name, cost, seed_image):
        self.name = name
        self.cost = cost
        self.seed_IMG = seed_image


hoe = Tool("hoe")
bucket = Tool("bucket")

wheat = Seed("wheat", 10, "1")
carrot = Seed("carrot", 20, "2")
potato = Seed("potato", 15, "3")


def image_render(img, img_x, img_y, use, scale=1.0):
    img = pygame.transform.scale(img, (screen_width * scale, screen_width * scale))
    img_rect = img.get_rect()
    img_rect = img_rect.move((img_x, img_y))
    if use == 1:
        img_rect.center = pygame.mouse.get_pos()
    screen.blit(img, img_rect)
    return img_rect


unclaimed_price = 100
an = 1
active_key = 1
move = True
running = True
seed_tick = 0

# watering can variables
watering_can_max = 5
watering_can = watering_can_max

# buy and sell variables
sell_wheat = 3
buy_potato = 10
sell_potato = 15
buy_carrot = 27
sell_carrot = 35

# slowing down  key press
game_tick = 0

while running:
    screen.blit(bg_img, (0, 0))
    cursor = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)
    t, e = 1, 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # scrolling
        max_scroll = 5
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                active_key -= 0.5
                if active_key < 1:
                    active_key = max_scroll
            if event.y < 0:
                active_key += 0.5
                if active_key > max_scroll:
                    active_key = 1

        # key press
        # slowing down  key press
        game_tick = 0
        keys = pygame.key.get_pressed()
        if game_tick == 0:
            game_tick = 20
            if keys[pygame.K_LEFT]:
                active_key -= 1
                if active_key < 1:
                    active_key = max_scroll
            if keys[pygame.K_RIGHT]:
                active_key += 1
                if active_key > max_scroll:
                    active_key = 1

            if keys[pygame.K_F1]:
                print(cursor)

            # buy crops
            if keys[pygame.K_F2]:
                my_game.add('money', 100)
            if keys[pygame.K_F3]:
                if my_game.inventory_dict['Money'] >= buy_potato:
                    my_game.add('money', -1 * buy_potato)
                    my_game.add('potato', 1)
            if keys[pygame.K_F4]:
                if my_game.inventory_dict['Money'] >= buy_carrot:
                    my_game.add('money', -buy_carrot)
                    my_game.add('carrot', 1)
        if game_tick > 0:
            game_tick -= 1

        # ITEM RENDER
        if active_key == 1:
            ToolsIMG = pygame.image.load("images/hoe.png")
        if active_key == 2:
            if watering_can > 0:
                ToolsIMG = pygame.image.load("images/can_full.png")
            else:
                ToolsIMG = pygame.image.load("images/can_empty.png")
        if active_key == 3:
            ToolsIMG = pygame.image.load("images/seed_wheat.png")
        if active_key == 4 and my_game.inventory_dict["Potato"] > 0:
            ToolsIMG = pygame.image.load("images/seed_potato.png")
        if active_key == 5 and my_game.inventory_dict["Carrot"] > 0:
            ToolsIMG = pygame.image.load("images/seed_carrot.png")

    # score render
    image_render(pygame.image.load('images/menu.png'), -30, -30, e, 0.37)

    score_text = font.render(f'${my_game.inventory("money")}', True, (113, 222, 113))
    screen.blit(score_text, (90, 28))

    Wheat_count = font.render(f'inf    -     ${sell_wheat}', True, (179, 172, 48))
    screen.blit(Wheat_count, (85, 90))

    Potato_y = 132
    Potato_x = 89
    Potato_color = (196, 212, 118)
    Potato_amount = font.render(f'{my_game.inventory_dict["Potato"]}', True, Potato_color)
    screen.blit(Potato_amount, (Potato_x, Potato_y))
    Potato_cost = font.render(f'${buy_potato}', True, Potato_color)
    screen.blit(Potato_cost, (Potato_x + 40, Potato_y))
    Potato_sell = font.render(f'${sell_potato}', True, Potato_color)
    screen.blit(Potato_sell, (Potato_x + 100, Potato_y))
    Potato_key = font.render(f'[F3]', True, Potato_color)
    screen.blit(Potato_key, (Potato_x + 142, Potato_y))

    Carrot_y = 182
    Carrot_x = 89
    Carrot_color = (212, 175, 119)
    Carrot_amount = font.render(f'{my_game.inventory_dict["Carrot"]}', True, Carrot_color)
    screen.blit(Carrot_amount, (Carrot_x, Carrot_y))
    Carrot_cost = font.render(f'${buy_carrot}', True, Carrot_color)
    screen.blit(Carrot_cost, (Carrot_x + 40, Carrot_y))
    Carrot_sell = font.render(f'${sell_carrot}', True, Carrot_color)
    screen.blit(Carrot_sell, (Carrot_x + 100, Carrot_y))
    Carrot_key = font.render(f'[F4]', True, Carrot_color)
    screen.blit(Carrot_key, (Carrot_x + 142, Carrot_y))

    water_x = 89
    water_y = 242
    water_count = font.render(f'{watering_can}/{watering_can_max}', True, (15, 80, 140))
    screen.blit(water_count, (water_x, water_y))


    hoe.mouse_locate()

    # LAND RENDERER
    x, y = 0, 0
    for w in range(my_game.cords()[0]):
        y = 0
        x += screen_width / (my_game.cords()[0] + 2)
        for h in range(my_game.cords()[1]):
            y += screen_height / (my_game.cords()[1] + 2)

            if my_game.land(w, h).isClaimed:
                land_img = "land"
                if my_game.land(w, h).isWet:
                    land_img = "land_wet"
                if my_game.land(w, h).isMowed:
                    land_img = "land_mowed"
                    if my_game.land(w, h).isWet:
                        land_img = "land_mowed_wet"
            else:
                land_img = "land_unclaimed"

            # render land and seed
            rect = image_render(pygame.image.load(f"images/{land_img}.png"), x + 120, y, e, 1 / 8)
            if my_game.land(w, h).seed[2] > 0:
                seed = my_game.land(w, h).seed[0]
                age = my_game.land(w, h).seed[2]
                image_render(pygame.image.load(f"images/{seed}{age}.png"), x + 120, y, e, 1 / 8)

            lake_rect = image_render(pygame.image.load(f"images/pool.png"), screen_width - 125, 0, e, 1 / 8)

            # `inter`action with land
            touchingMouse = rect.collidepoint(cursor)
            if touchingMouse:
                # show land cost
                if not my_game.land(w, h).isClaimed:
                    land_price = font.render(f"Cost: {unclaimed_price}$", True, (113, 222, 113))
                    screen.blit(land_price, (cursor[0] - 50, cursor[1] - 35))

                # interaction
                if my_game.land(w, h).isClaimed:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        active_key = math.floor(active_key)
                        if active_key == 1:
                            if my_game.land(w, h).seed[0] == '':
                                my_game.land(w, h).mow()
                            else:
                                if my_game.land(w, h).seed[2] == my_game.max_age:  # max growth age
                                    # sell crops
                                    r = random.randint(0, 4)
                                    if my_game.land(w, h).seed[0] == 'wheat':
                                        my_game.add('money', sell_wheat)
                                    if my_game.land(w, h).seed[0] == 'potato':
                                        my_game.add('money', sell_potato)
                                        my_game.add('potato', r)
                                    if my_game.land(w, h).seed[0] == 'carrot':
                                        my_game.add('money', sell_carrot)
                                        my_game.add('carrot', r)

                                    my_game.land(w, h).plant('', age=0)

                        # water
                        if active_key == 2 and watering_can > 0:
                            if my_game.land(w, h).water():
                                watering_can -= 1
                                pass

                        # plant
                        if 3 <= active_key <= 5 and my_game.land(w, h).seed[0] == '':
                            seed = ''
                            if active_key == 3:
                                seed = 'wheat'
                            if active_key == 4:
                                if my_game.inventory_dict['Potato'] >= 1:
                                    my_game.add('potato', -1)
                                    seed = 'potato'
                            if active_key == 5:
                                if my_game.inventory_dict['Carrot'] >= 1:
                                    my_game.add('carrot', -1)
                                    seed = 'carrot'
                            if seed != '':
                                my_game.land(w, h).plant(seed, 1)

                        # buy land
                        if not my_game.land(w, h).isClaimed:
                            if my_game.inventory_dict['Money'] >= unclaimed_price:
                                my_game.add('money', unclaimed_price * -1)
                                unclaimed_price += 20
                                my_game.land(w, h).claim()

                touchingMouse = lake_rect.collidepoint(cursor)
                if touchingMouse:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        active_key = math.floor(active_key)
                        if math.floor(active_key) == 2 and watering_can == 0:
                            watering_can = watering_can_max

    # render tool
    image_render(ToolsIMG, hoe.pos_x, hoe.posy, t, 1 / 7)
    if math.floor(active_key) == 2:
        watering = font.render(f'{watering_can}/{watering_can_max}', True, (15, 80, 140))
        screen.blit(watering, (cursor[0] - 20, cursor[1] + 70))

    # wheat growth + win detection
    lands_claimed = 0
    for w in range(my_game.cords()[0]):
        for h in range(my_game.cords()[1]):
            my_game.land(w, h).grow()
            if my_game.land(w, h).isClaimed:
                lands_claimed += 1
            if my_game.land(w, h).wet > 0:
                my_game.land(w, h).wet -= 1
            else:
                my_game.land(w, h).water(False)

    if lands_claimed == my_game.cords()[0] * my_game.cords()[1]:
        you_won = font.render(f'YOU WON! You are an excellent farmer!', True, (255, 213, 0))
        screen.blit(you_won, (cursor[0] - 200, cursor[1] - 35))
    pygame.display.update()
