import pickle
import pygame as pg
from os import path


pg.init()

clock = pg.time.Clock()
fps = 60

screen_w = 1000
screen_h = 1000

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption('Platformer')
icon = pg.image.load('Platformer/Assets/icon.png')
pg.display.set_icon(icon)

tile_size = 50
game_over = 0

load_level = True
level = 2

bg_img = pg.image.load('Platformer/Assets/background.png')
class World():
    def __init__(self,data):
        self.tile_list = []
        border_img = pg.image.load('Platformer/Assets/Border.png')
        block_img = pg.image.load('platformer/Assets/block.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pg.transform.scale(border_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pg.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count*tile_size, row_count*tile_size)
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                col_count += 1
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pg.draw.rect(screen, (255, 255, 255), tile[1], 2)

        self.images_right = []
        self.images_left = []
        img = pg.image.load('platformer/assets/player.png')
        img_right = pg.transform.scale(img, (40, 80))
        img_left = pg.transform.flip(img, True, False)
        self.images_right.append(img_right)
        self.images_left.append(img_left)

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        img = pg.image.load('platformer/assets/player.png')
        self.image = pg.transform.scale(img, (40, 80))
        img_right = self.image
        img_left = pg.transform.flip(img_right, True, False)
        self.images_right.append(img_right)
        self.images_left.append(img_left)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
    
    def update(self, game_over):
        
        dx = 0
        dy = 0

        if game_over == 0:

            key = pg.key.get_pressed()
            if key[pg.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pg.K_SPACE] == False:
                self.jumped = False
            if key[pg.K_LEFT]:
                dx -= 5
                self.direction = -1
            if key[pg.K_RIGHT]:
                dx += 5
                self.direction = 1
            if key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0 
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0 
            
            if pg.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pg.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

class Enemy(pg.sprite.Sprite):
    def __init__(self,x, y):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load('platformer/assets/shredder.png')
        self.image = pg.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('platformer/assets/lava.png')
        self.image = pg.transform.scale(img, (tile_size, tile_size //2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = pickle.load(open('Platformer/level1_data','rb'))
    

player = Player(100, screen_h - 130)

lava_group = pg.sprite.Group()
blob_group = pg.sprite.Group()

world = World(world_data)

run = True
while run:

    clock.tick(fps)
    
    screen.blit(bg_img, (0,0))
    
    world.draw()
    if game_over == 0:
        blob_group.update()
    
    blob_group.draw(screen)
    lava_group.draw(screen)

    game_over = player.update(game_over)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()

pg.quit()