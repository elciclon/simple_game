import random

import pgzrun
from pygame import Rect


WIDTH = 800
HEIGHT = 600

# Global variables
state = "menu"
music = True
score = 0
game_over = False

# Buttons class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text

    def draw(self):
        # Draw the buttons
        screen.draw.filled_rect(self.rect, 'green')
        screen.draw.text(self.text, center=self.rect.center, color='black')

    def is_clicked(self, pos):
        # Check if the button is clicked
        return self.rect.collidepoint(pos)

# Create menu buttons
start_game_button = Button(300, 200, 200, 50, "Start Game")
music_button = Button(300, 270, 200, 50, "Music: On")
exit_button = Button(300, 340, 200, 50, "Exit")

class Hero:
    def __init__(self):
        self.x = WIDTH // 2 # Center the hero
        self.y = HEIGHT // 2
        self.speed = 3
        # hero images
        self.idle_images = ['hero_1', 'hero_2']

        self.current_images = self.idle_images
        self.frame = 0
        self.actor = Actor(self.current_images[self.frame], center=(self.x, self.y))
        self.animation_timer = 0

    def draw(self):
        self.actor.draw()

hero = Hero()

zombie = Actor('character_zombie_idle')
zombie.x = random.randint(20, WIDTH - 20)
zombie.y = 0

items = Actor('generic_item_color_005')
items.x = random.randint(20, WIDTH - 20)
items.y = random.randint(20, HEIGHT - 20)

def update():
    global score, game_over, music, state

    if keyboard.left:
        hero.x = hero.x - 5
    if keyboard.right:
        hero.x = hero.x + 5

    zombie.y = zombie.y + 4 + score / 10
    if zombie.y > HEIGHT:
        zombie.y = 0
    
    # if hero.colliderect(items):
    #     items.x = random.randint(20, WIDTH - 20)
    #     items.y = random.randint(20, HEIGHT - 20)
    #     score = score + 1



def draw():
    screen.clear()
    if game_over:
        screen.draw.text('Game Over', (WIDTH // 2, 300), color=(192,31,31), fontsize=50)
        screen.draw.text('Score: ' + str(score), (WIDTH // 2, 350), color=(255,255,255), fontsize=60)
    else:
        zombie.draw()
        hero.draw()
        items.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=30)
        start_game_button.draw()
        music_button.draw()
        exit_button.draw()


pgzrun.go()
