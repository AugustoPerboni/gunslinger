from gunslinger_package.config import window_width
from gunslinger_package.objects_classes.element import Element
import pygame

import sys
sys.path.append(
    'C:\\Users\\augus\\Desktop\\pythonScripts\\General\\myProjects\\gunslinger-division')


class Enemy(Element):
    ''' Define the game enemies. '''

    def __init__(self, x, speed, power, images, name, max_life):
        Element.__init__(self, x, 515, 128, 128, speed, power)  # 3

        self.hitbox = (self.x + 25, self.y + 55, 65, 70)
        self.max_life = max_life
        self.life = max_life
        self.walk_count = 0
        self.walk_right = False
        self.walk_left = True
        self.dead_count = 0
        self.is_hitting = False
        self.hitting_count = 0

        self.dying_sound = pygame.mixer.Sound('sounds\dying-zombie.wav')

        # Used to differentiate each kind of enemy
        self.images = images
        self.name = name
        self.life_bar_x = self.x + 15
        self.life_bar_y = self.y + 35

    def draw(self, window, enemy, enemies, origin_background, player):
        if (player.in_window_second_half and (enemy.x > -50)) or (not player.in_window_second_half and enemy.x < window_width + 50):
            if self.life <= 0:
                if self.dead_count + 1 <= len(self.images[1]) and self.walk_right:
                    window.blit(
                        self.images[1][self.dead_count], (self.x, self.y))
                    self.dead_count += 1
                elif self.dead_count + 1 <= len(self.images[3]) and self.walk_left:
                    window.blit(
                        self.images[3][self.dead_count], (self.x, self.y))
                    self.dead_count += 1
                else:
                    player.money += 5
                    self.dying_sound.play()
                    del enemies[enemies.index(enemy)]

            else:
                # Life bar plot and positioning
                self.life_bar_x = self.x + 15
                self.life_bar_y = self.y + 35
                self.life_bar(window)

                if self.is_hitting:
                    if self.hitting_count + 1 >= 36:
                        self.hitting_count = 0
                    else:
                        self.hitting_count += 1
                    window.blit(
                        self.images[4][self.hitting_count//3], (self.x, self.y + self.height/3))
                else:
                    # Each image will be used in 3 frames
                    if self.walk_count + 1 >= 54:
                        self.walk_count = 0

                    if self.walk_right:
                        window.blit(
                            self.images[0][self.walk_count//3], (self.x, self.y + self.height/3))
                        self.walk_count += 1
                    elif self.walk_left:
                        window.blit(
                            self.images[2][self.walk_count//3], (self.x, self.y + self.height/3))
                        self.walk_count += 1
                        # Given the irregularity of sides
                        self.hitbox = (self.x + 25, self.y + 55, 65, 70)
        # Once the enemy move autonomus we add the move in draw
        self.move(origin_background)

        self.hitbox = (self.x + 34, self.y + 55, 70, 70)

        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def window_half_correction(self, player):
        if player.in_window_second_half:
            self.x -= window_width
        else:
            self.x += window_width

    def hit(self, damage):
        # print('ENEMY HIT')
        self.life -= damage

    def move(self, origin_background):

        if self.is_hitting:
            self.walk_left = False
            self.walk_right = False
        elif self.x <= origin_background[0]:
            self.walk_left = False
            self.walk_right = True
            self.walk_count = 0
        elif self.x >= origin_background[0] + 2 * window_width:
            self.walk_left = True
            self.walk_right = False
            self.walk_count = 0

        if self.walk_left:
            self.x -= self.velocity
        elif self.walk_right:
            self.x += self.velocity
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
