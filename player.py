import pygame
from params import *
from math import sqrt
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(YELLOW)
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 0)
        self.pos = vec(WIDTH / 2, 0)

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.on_ground = False
        self.idle = True

        # animation lists
        self.last_update = 0
        self.idle_frame = 0
        idle_list_rects = [(0, 191, 67, 95),
                           (67, 191, 67, 95)]
        self.idle_list = self.game.spritesheet.get_image_list(idle_list_rects)
        self.idle_list += [self.idle_list[0],
                           pygame.transform.flip(self.idle_list[1], True, False)]

    def load_image(self):
        self.image = self.game.spritesheet.get_image(0, 0, 72, 95)

    def update(self):

        # check ground
        hit = self.is_on_ground()
        if hit:
            self.on_ground = True
        else:
            self.on_ground = False

        if self.on_ground:
            self.acc = vec(0, 0)
        else:
            self.acc = vec(0, GRAVITY_ACC)

        keys = pygame.key.get_pressed()
        if self.on_ground:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.acc.x = PLAYER_ACC
            # jump
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                self.jump()

        # apply friction
        if self.on_ground:
            self.acc.x += self.vel.x * PLAYER_FRICTION


        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        old_pos = self.pos
        new_pos = old_pos + self.vel + 0.5 * self.acc

        vec_len = int(sqrt((old_pos.x - new_pos.x)**2 + (old_pos.y - new_pos.y)**2)) + 1
        final_pos = vec(0, 0)
        for i in range(vec_len):
            self.pos = old_pos + (new_pos - old_pos) * (i + 1) / vec_len
            # смещаем плеера для проверки новой позиции...
            self.rect.centery += round(self.pos.y - old_pos.y)
            self.rect.centerx += round(self.pos.x - old_pos.x)
            platform = pygame.sprite.spritecollide(self, self.game.platforms, False)
            for plat in platform:

                if ((plat.rect.top <= self.rect.top <= plat.rect.bottom) or (plat.rect.top <= self.rect.bottom <= plat.rect.bottom)) and (self.rect.left <= plat.rect.left) and (plat.rect.right <= self.rect.right):
                    self.vel.y = 0
                if ((plat.rect.left <= self.rect.left <= plat.rect.right) or (plat.rect.left <= self.rect.right <= plat.rect.right)) and (self.rect.top <= plat.rect.top) and (plat.rect.bottom <= self.rect.bottom):
                    self.vel.x = 0
            # возвращаем плеера обратно...
            self.rect.centery -= round(self.pos.y - old_pos.y)
            self.rect.centerx -= round(self.pos.x - old_pos.x)
            if platform:
                self.pos = old_pos + (new_pos - old_pos) * i / vec_len
                #pygame.quit();
                break

        screen_offset = vec(0, 0)

        if self.pos.x > WIDTH / 2:
            screen_offset.x = int(self.pos.x - WIDTH / 2)
        if self.pos.x > len(self.game.lmap.level_array[0])*PLATFORM_WIDTH - WIDTH / 2:
            screen_offset.x = int(len(self.game.lmap.level_array[0])*20 - WIDTH)

        if self.pos.y > HEIGHT / 2:
            screen_offset.y = int(self.pos.y - HEIGHT / 2)
        if self.pos.y > len(self.game.lmap.level_array)*PLATFORM_WIDTH - HEIGHT / 2:
            screen_offset.y = int(len(self.game.lmap.level_array)*PLATFORM_WIDTH - HEIGHT)  #'''


        self.rect.midbottom = self.pos - screen_offset
        for sprite in self.game.platforms:
            sprite.rect.center = sprite.pos - screen_offset


        self.animate()


    def is_on_ground(self):
        self.rect.centery += 1
        hit = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.centery -= 1
        return hit


    def jump(self):
        self.on_ground = False
        self.acc.y = -20

    def animate(self):
        now = pygame.time.get_ticks()
        if self.idle:
            if now - self.last_update > 300:
                self.last_update = now
                self.idle_frame = (self.idle_frame + 1) % 4
                self.image = self.idle_list[self.idle_frame]
