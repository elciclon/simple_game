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

def update():
    if keyboard.left:
        hero.x = hero.x - 5
    if keyboard.right:
        hero.x = hero.x + 5

def draw():
    screen.clear()
    hero.draw()


pgzrun.go()
