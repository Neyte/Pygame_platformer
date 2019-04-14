import pygame
from params import *
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
        '''        if self.on_ground:
            self.acc = vec(0, 0)
        else:
            self.acc = vec(0, GRAVITY_ACC)  '''
        self.acc = vec(0, GRAVITY_ACC)

        keys = pygame.key.get_pressed()
        if self.on_ground:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.acc.x = PLAYER_ACC

        # jump
        if self.on_ground and keys[pygame.K_SPACE]:
            self.jump()

        # apply friction
        if self.on_ground:
            self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen
        '''if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH  #'''

        # check ground
        cur_plat = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if cur_plat:
            self.on_ground = True
            self.vel.y = 0
            self.pos.y = cur_plat[0].rect.top + self.game.screen_offset.y

        screen_offset = vec(0, 0)
        if self.pos.x > WIDTH / 2:
            screen_offset.x = int(self.pos.x - WIDTH / 2)
        if self.pos.x > len(self.game.lmap.level_array[0])*20 - WIDTH / 2:
            screen_offset.x = int(len(self.game.lmap.level_array[0])*20 - WIDTH)

        if self.pos.y > HEIGHT / 2:
            screen_offset.y = int(self.pos.y - HEIGHT / 2)
        if self.pos.y > len(self.game.lmap.level_array)*20 - HEIGHT / 2:
            screen_offset.y = int(len(self.game.lmap.level_array)*20 - HEIGHT)  #'''


        self.rect.midbottom = self.pos - screen_offset
        for sprite in self.game.platforms:
            sprite.rect.center += self.game.screen_offset - screen_offset
        self.game.screen_offset = screen_offset


        self.animate()

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
