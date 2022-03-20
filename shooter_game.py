#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
 
font2 = font.Font(None, 36)
 

mixer.init()
mixer.music.load('imperial_march.mp3')
mixer.music.play()
fire_sound = mixer.Sound('ochen-gromkiy-zvuk-vyistrela1.ogg')
 

img_back = "galaxy.jpg" 
img_bullet = "bullet.png" 
img_hero = "rocket.png" 
img_enemy = "ufo.png" 
img_health = 'pngtree-red-heart-icon-isolated-png-image_1726594.jpg'
img_asteroid = 'asteroid.png'
score = 0 
goal = 10 
lost = 0 
max_lost = 3 
class GameSprite(sprite.Sprite):
 
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       
       sprite.Sprite.__init__(self)
 
       
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, health):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = health
    
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
    
    def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
  
class Enemy(GameSprite):
   
   def update(self):
       self.rect.y += self.speed
       global lost
       
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
  
class Bullet(GameSprite):
   
    def update(self):
       self.rect.y += self.speed
       
       if self.rect.y < 0:
           self.kill()

class BonusLive(GameSprite):
    def update(self):
       self.rect.y += self.speed
       
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0

class Asteroid(GameSprite):
    def update(self):
       self.rect.y += self.speed
       
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           
    



win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 3)
bonus_live = BonusLive(img_health, randint(80, win_width - 80), -40, 50, 50, randint(1, 5))

monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(3):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
bullets = sprite.Group()

finish = False

run = True 
while run:
   
   for e in event.get():
       if e.type == QUIT:
           run = False
       
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 
   if not finish:
       
       window.blit(background,(0,0))
 
       
       ship.update()
       monsters.update()
       bullets.update()
       bonus_live.update()
       asteroids.update()
 
       
       ship.reset()
       bonus_live.reset()
       asteroids.draw(window)
       monsters.draw(window)
       bullets.draw(window)
       
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
 
       
       if  lost >= max_lost or ship.health <= 0:
           finish = True 
           window.blit(lose, (200, 200))
       
       if sprite.spritecollide(ship, monsters, True):
           if ship.health>0:
               ship.health -= 1
               monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
               monsters.add(monster)
       
       if sprite.spritecollide(ship, asteroids, True):
           if ship.health>0:
               ship.health -= 2
               asteroid = Asteroid(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
               asteroids.add(asteroid)
       

       if sprite.spritecollide(bonus_live, bullets, True): 
           ship.health += 1
           bonus_live.rect.x = randint(80, win_width - 80)
           bonus_live.rect.y = -40
           
       
       
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))
 
       
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
 
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       text_health = font2.render("Жизней осталось: " + str(ship.health), 1, (255, 255, 255))
       window.blit(text_health, (10, 80))
 
       display.update()
   
   else:
       finish = False
       score = 0
       lost = 0
       ship.health = 3
       bonus_live.rect.x = randint(80, win_width - 80)
       bonus_live.rect.y = -40
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()
 
       time.delay(1000)
       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
   time.delay(50)