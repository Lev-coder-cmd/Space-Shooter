from pygame import *
from random import randint
import time as t
init()
mixer.init()
volume = 0.2
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')
lost_sound = mixer.Sound('lost.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (self.width, self.height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_size[0] - self.width:
            self.rect.x += self.speed
    
    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 15, 5))

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
    
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > window_size[1]:
            self.rect.y = -self.height
            self.rect.x = randint(0, window_size[0] - self.width)
            lost += 1
            lost_sound.play()

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_size[1]:
            self.rect.y = -self.height
            self.rect.x = randint(0, window_size[0] - self.width)
            
    
window_size = (700, 750)
window = display.set_mode(window_size)
display.set_caption('Космический Шутер')
background = transform.scale(image.load('galaxy.jpg'), window_size)
player = Player('rocket.png', 350, window_size[1] - 100, 65, 100, 3)
enemies = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for _ in range(5):
    enemies.add(Enemy('ufo.png', randint(0, window_size[0] - 92), 0, 92, 65, randint(1, 2)))
for i in range(3):
    asteroids.add(Asteroid('asteroid.png', randint(0, window_size[0] - 92), 0, 92, 62, randint(1, 2)))

num_fire = 0
rel_time = False
life = 3
life_color = (0, 0, 0)

finish = False
run = True
FPS = 60
clock = time.Clock()
lost = 0
score = 0
font1 = font.SysFont('Arial', 32)
font2 = font.SysFont('Arial', 48)
text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_KP_PLUS:
                if volume < 1.5:
                    volume += 0.1
            if e.key == K_KP_MINUS:
                if volume > 0:
                    volume -= 0.1
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    player.fire()
                    num_fire += 1
                elif num_fire >= 5 and not rel_time:
                    rel_time = True
                    timer_1 = t.time()


    if not finish:
        window.blit(background, (0, 0))
        if rel_time:
            timer_2 = t.time()
            if timer_2 - timer_1 < 3:
                text_reload = font1.render('Wait, reload...', True, (115, 0, 0))
                window.blit(text_reload, (275, 715))
            else:
                num_fire = 0
                rel_time = False



        collision_bullets = sprite.groupcollide(enemies, bullets, True, True)
        for collision in collision_bullets:
            score += 1
            collision.kill()
            enemies.add(Enemy('ufo.png', randint(0, window_size[0] - 92), 0, 92, 65, randint(1, 2)))

        if score >= 10:
            text_win = font2.render('YOU WIN', True, (0, 255, 0))
            window.blit(text_win, (272, 375))
            finish = True

        collision_asteroid = sprite.spritecollide(player, asteroids, False)
        for collision in collision_asteroid:
            life -= 1
            collision.kill()
            asteroids.add(Asteroid('asteroid.png', randint(0, window_size[0] - 92), 0, 92, 62, randint(1, 2)))
        
        collision_enemy = sprite.spritecollide(player, enemies, False)
        for collision in collision_enemy:
            life -= 1
            collision.kill()
            enemies.add(Enemy('ufo.png', randint(0, window_size[0] - 92), 0, 92, 65, randint(1, 2)))


        if lost >= 3 or life <= 0:
            text_lost = font2.render('YOU LOSE', True, (255, 0, 0))
            window.blit(text_lost, (272, 375))
            finish = True
        
        if life == 3:
            life_color = (0, 172, 0)
        if life == 2:
            life_color = (182, 168, 43)
        if life == 1:
            life_color = (172, 0, 0)
        lifes_counter = font2.render(str(life), True, life_color)
        window.blit(lifes_counter, (650, 47))
        
        text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        mixer.music.set_volume(volume)
        window.blit(text_lose, (5, 32))
        window.blit(text_score, (5, 5))
        bullets.update()
        bullets.draw(window)
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        player.reset()
        player.update()
            
    else:
        time.delay(3500)
        num_fire = 0
        life = 3
        score = 0
        lost = 0
        player.rect.x = 350        
        rel_time = False
        for enemy in enemies:
            enemy.kill()
        for asteroid in asteroids:
            asteroid.kill()
        for bullet in bullets:
            bullet.kill()
        for _ in range(5):
            enemies.add(Enemy('ufo.png', randint(0, window_size[0] - 92), 0, 92, 65, randint(1, 2)))
        for i in range(3):
            asteroids.add(Asteroid('asteroid.png', randint(0, window_size[0] - 92), 0, 92, 62, randint(1, 2)))
        finish = False
          
    display.update()
    clock.tick(FPS)