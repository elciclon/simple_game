import random
import math
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
        self.run_images = ['hero_run_1', 'hero_run_2','hero_run_3']
        self.current_images = self.idle_images
        self.frame = 0
        self.actor = Actor(self.current_images[self.frame], center=(self.x, self.y))
        self.animation_timer = 0

    def update(self):
        dx = 0
        dy = 0
        if keyboard.left:
            dx = -self.speed
        elif keyboard.right:
            dx = self.speed
        if keyboard.up:
            dy = -self.speed
        elif keyboard.down:
            dy = self.speed

        # Changes between idle and run animation if hero is moving
        if dx != 0 or dy != 0:
            self.current_images = self.run_images
            self.x += dx
            self.y += dy
        else:
            self.current_images = self.idle_images

        # Keep the hero inside the screen
        self.x = max(self.actor.width // 2, min(WIDTH - self.actor.width // 2, self.x))
        self.y = max(self.actor.height // 2, min(HEIGHT - self.actor.height // 2, self.y))

        # Smooth animation
        self.animation_timer += 1
        if self.animation_timer >= 10: # Controls the animation speed
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.current_images)
            self.actor.image = self.current_images[self.frame]
        self.actor.pos = (self.x, self.y)
    
    def draw(self):
        self.actor.draw()

# Enemy class with sprite animation
class Zombie:
    def __init__(self, x, y, hero):
        self.x = x
        self.y = y
        self.speed = 2
        self.move_images = ["zombie_run_1", "zombie_run_2", "zombie_run_3"]
        self.frame = 0
        self.actor = Actor(self.move_images[self.frame], (self.x, self.y))
        self.animation_timer = 0
        self.catch_target(hero)

    def catch_target(self, hero):
        # Try to catch the hero
        self.target_x = hero.x
        self.target_y = hero.y

    
    def update(self, zombies, hero):
        # Try to catch the hero
        self.catch_target(hero)
        

        # Get the distance to the target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)

        # Move towards the target        
        self.current_images = self.move_images
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed

        # Actualizar animación
        self.animation_timer += 1
        if self.animation_timer >= 15:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.current_images)
            self.actor.image = self.current_images[self.frame]

        # Actualizar posición del actor
        self.actor.pos = (self.x, self.y)

    def draw(self):
        self.actor.draw()

hero = Hero()
zombies = [Zombie(100, 100, hero)]


items = Actor('generic_item_color_005')
items.x = random.randint(20, WIDTH - 20)
items.y = random.randint(20, HEIGHT - 20)

def update():
    global score, game_over, music, state

    hero.update()
    for zombie in zombies:
        zombie.update(zombies, hero)

    
    


def draw():
    screen.clear()
    if game_over:
        screen.draw.text('Game Over', (WIDTH // 2, 300), color=(192,31,31), fontsize=50)
        screen.draw.text('Score: ' + str(score), (WIDTH // 2, 350), color=(255,255,255), fontsize=60)
    else:
        for zombie in zombies:
            zombie.draw()
        hero.draw()
        items.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=30)
        start_game_button.draw()
        music_button.draw()
        exit_button.draw()


pgzrun.go()
