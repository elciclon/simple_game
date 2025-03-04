import random

import pgzrun
from pygame import Rect


WIDTH = 800
HEIGHT = 600

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
        self.idle_images = ['character_maleperson_idle', 'character_malePerson_duck']


hero = Actor('character_maleperson_idle')
hero.x = WIDTH // 2
hero.y = HEIGHT // 2

zombie = Actor('character_zombie_idle')
zombie.x = random.randint(20, WIDTH - 20)
zombie.y = 0

items = Actor('generic_item_color_005')
items.x = random.randint(20, WIDTH - 20)
items.y = random.randint(20, HEIGHT - 20)

def update():
    if keyboard.left:
        hero.x = hero.x - 5
    if keyboard.right:
        hero.x = hero.x + 5

    zombie.y = zombie.y + 4
    if zombie.y > HEIGHT:
        zombie.y = 0
    if zombie.colliderect(hero):
        zombie.x = random.randint(20, WIDTH - 20)
        zombie.y = 0

    if hero.colliderect(items):
        items.x = random.randint(20, WIDTH - 20)
        items.y = random.randint(20, HEIGHT - 20)



def draw():
    screen.clear()
    zombie.draw()
    hero.draw()
    items.draw()


pgzrun.go()
