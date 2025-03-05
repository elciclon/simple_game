import random
import math
import pgzrun
from pygame import Rect

# Stage
WIDTH = 800
HEIGHT = 600
ROWS = 2
COLS = 4
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Global variables
state = "menu"
background_music = True
score = 0
game_over = False
zombie_speed = 0.5
game_over_sound_played = False


# Buttons class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text

    def draw(self):
        # Draw the buttons
        screen.draw.filled_rect(self.rect, "green")
        screen.draw.text(self.text, center=self.rect.center, color="black")

    def is_clicked(self, pos):
        # Check if the button is clicked
        return self.rect.collidepoint(pos)


# Create menu buttons
start_game_button = Button(300, 200, 200, 50, "Start Game")
music_button = Button(300, 270, 200, 50, "Music & sounds: On")
exit_button = Button(300, 340, 200, 50, "Exit")


class Hero:
    def __init__(self):
        self.x = 3 * CELL_WIDTH + CELL_WIDTH // 2  # Center the hero
        self.y = CELL_HEIGHT + CELL_HEIGHT // 2
        self.speed = 3
        # hero images
        self.idle_images = ["hero_1", "hero_2"]
        self.run_images = ["hero_run_1", "hero_run_2", "hero_run_3"]
        self.current_images = self.idle_images
        self.frame = 0
        self.actor = Actor(self.current_images[self.frame], center=(self.x, self.y))
        self.animation_timer = 0
        # Add step sound timer and toggle
        self.step_timer = 0
        self.step_toggle = True

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

        moving = dx != 0 or dy != 0

        # If moving, update position and play step sounds periodically.

        if moving:
            self.current_images = self.run_images
            self.x += dx
            self.y += dy

            # Update step timer and play a step sound when the timer reaches a threshold.
            self.step_timer += 1
            if self.step_timer >= 7:  # adjust this threshold for timing
                if self.step_toggle:
                    if background_music:
                        sounds.step_1.play()
                else:
                    if background_music:
                        sounds.step_2.play()
                self.step_toggle = not self.step_toggle
                self.step_timer = 0
        else:
            self.current_images = self.idle_images
            # Reset the step timer when not moving to avoid playing sounds on resume.
            self.step_timer = 0

        # Keep the hero inside the screen
        self.x = max(self.actor.width // 2, min(WIDTH - self.actor.width // 2, self.x))
        self.y = max(
            self.actor.height // 2, min(HEIGHT - self.actor.height // 2, self.y)
        )

        # Smooth animation
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Controls the animation speed
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
        # Store the base position
        self.base_x = x
        self.base_y = y

        self.speed = 0.5
        self.idle_images = ["zombie_1", "zombie_2"]
        self.move_images = ["zombie_run_1", "zombie_run_2", "zombie_run_3"]
        self.current_images = self.idle_images
        self.frame = 0
        self.actor = Actor(self.current_images[self.frame], (self.x, self.y))
        self.animation_timer = 0
        # Target to try to catch the hero
        self.target_x = x
        self.target_y = y

    def catch_target(self, hero):
        """Try to catch the hero"""
        self.target_x = hero.x
        self.target_y = hero.y

    def update(self, hero):
        # Where's the zombie
        zombie_cell_col = int(self.base_x // CELL_WIDTH)
        zombie_cell_row = int(self.base_y // CELL_HEIGHT)
        # Where's the hero
        hero_cell_col = int(hero.x // CELL_WIDTH)
        hero_cell_row = int(hero.y // CELL_HEIGHT)
        if zombie_cell_col == hero_cell_col and zombie_cell_row == hero_cell_row:
            active = True
        else:
            active = False
        if active:
            # Active state: chase the hero
            self.catch_target(hero)
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            self.current_images = self.move_images
        else:
            # Idle state: remain centered in its cell
            self.x = self.base_x
            self.y = self.base_y
            self.current_images = self.idle_images

        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= 15:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.current_images)
            self.actor.image = self.current_images[self.frame]

        # Update zombie position
        self.actor.pos = (self.x, self.y)

    def draw(self):
        self.actor.draw()


class Gem:
    def __init__(self, cell_row, cell_col, item):
        # Stores the position in the cell
        self.cell_row = cell_row
        self.cell_col = cell_col

        # Define a padding
        padding = 30
        # Calculate the boundaries of the cell
        left = cell_col * CELL_WIDTH + padding
        right = (cell_col + 1) * CELL_WIDTH - padding
        top = cell_row * CELL_HEIGHT + padding
        bottom = (cell_row + 1) * CELL_HEIGHT - padding

        # Calculate the center of the cell
        center_x = cell_col * CELL_WIDTH + CELL_WIDTH // 2
        center_y = cell_row * CELL_HEIGHT + CELL_HEIGHT // 2
        threshold = 50  # Minimum distance from the center

        # Randomly choose a position for the gem, re-sample if it's too close to the center
        while True:
            self.x = random.randint(left, right)
            self.y = random.randint(top, bottom)
            if not (
                abs(self.x - center_x) < threshold
                and abs(self.y - center_y) < threshold
            ):
                break

        self.actor = Actor(item, (self.x, self.y))
        self.collected = False

    def draw(self):
        if not self.collected:
            self.actor.draw()


hero = Hero()

zombies = []
for r in range(2):  # 2 files
    for c in range(4):  # 4 col
        # Check if hero cell
        if r == 1 and c == 3:
            continue
        # Center the zombie
        center_x = c * CELL_WIDTH + CELL_WIDTH // 2
        center_y = r * CELL_HEIGHT + CELL_HEIGHT // 2
        zombies.append(Zombie(center_x, center_y, hero))

item_names = ["item_1", "item_2", "item_3", "item_4", "item_5", "item_6", "item_7"]
gems = []
item_index = 0
for r in range(ROWS):
    for c in range(COLS):
        # Skip the hero's cell; assume hero is at cell (1,3) (0-indexed: row 1, col 3)
        if r == 1 and c == 3:
            continue
        # Use the next item name from the list (wrap around if needed)
        item_name = item_names[item_index % len(item_names)]
        gems.append(Gem(r, c, item_name))
        item_index += 1


def update():
    global score, game_over, music, state, zombie_speed, game_over_sound_played

    if state == "menu":
        return  # Do not update game logic in menu state

    if game_over:
        if not game_over_sound_played:
            if background_music:
                sounds.game_over.play()
            game_over_sound_played = True
        return

    hero.update()
    for zombie in zombies:
        zombie.update(hero)
        if zombie.actor.colliderect(hero.actor):
            game_over = True
            break  # Stop checking further once game over

    # Check if the hero collects any gem
    for gem in gems:
        if not gem.collected and gem.actor.colliderect(hero.actor):
            gem.collected = True
            score += 1
            if background_music:
                sounds.collect.play()
    # If all gems are collected, restart the level
    if all(gem.collected for gem in gems):
        # Increase zombie speed multiplier
        zombie_speed += 0.5

        # Reset hero to starting cell (row 2, col 4; indices: row 1, col 3)
        hero.x = 3 * CELL_WIDTH + CELL_WIDTH // 2
        hero.y = CELL_HEIGHT + CELL_HEIGHT // 2
        hero.actor.pos = (hero.x, hero.y)

        # Regenerate each gem in its cell (avoiding the center)
        for gem in gems:
            gem.collected = False
            padding = 20
            left = gem.cell_col * CELL_WIDTH + padding
            right = (gem.cell_col + 1) * CELL_WIDTH - padding
            top = gem.cell_row * CELL_HEIGHT + padding
            bottom = (gem.cell_row + 1) * CELL_HEIGHT - padding

            center_x = gem.cell_col * CELL_WIDTH + CELL_WIDTH // 2
            center_y = gem.cell_row * CELL_HEIGHT + CELL_HEIGHT // 2
            threshold = 30  # Minimum distance from cell center

            while True:
                gem.x = random.randint(left, right)
                gem.y = random.randint(top, bottom)
                if not (
                    abs(gem.x - center_x) < threshold
                    and abs(gem.y - center_y) < threshold
                ):
                    break
            gem.actor.pos = (gem.x, gem.y)

        # Update zombies' speed (each zombie's base speed is multiplied by zombie_speed)
        for zombie in zombies:
            zombie.speed = 1.5 * zombie_speed

    if background_music:
        if not music.is_playing("music"):
            music.play("music")

    else:
        music.stop()


def on_mouse_down(pos):
    global state, background_music
    if state == "menu":
        if start_game_button.is_clicked(pos):
            sounds.start.play()
            state = "game"
        elif exit_button.is_clicked(pos):
            sounds.close.play()
            exit()
        elif music_button.is_clicked(pos):
            sounds.select.play()
            if background_music:
                background_music = False
                music_button.text = "Music & sounds: Off"
            else:
                background_music = True
                music_button.text = "Music & sounds: On"


def draw_grid():
    # Define a list of colors for each cell
    cell_colors = [
        "lightblue",
        "lightgreen",
        "lightyellow",
        "lightpink",
        "lightsalmon",
        "lightcyan",
        "lightgoldenrod",
        "lightgray",
    ]
    color_index = 0

    # Fill each cell with a different color
    for r in range(ROWS):
        for c in range(COLS):
            cell_rect = Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            screen.draw.filled_rect(
                cell_rect, cell_colors[color_index % len(cell_colors)]
            )
            color_index += 1


def draw():
    if state == "menu":
        screen.fill("black")
        start_game_button.draw()
        music_button.draw()
        exit_button.draw()
        screen.draw.text(
            "Zombies Nightmare", center=(WIDTH // 2, 100), fontsize=60, color="white"
        )
    else:
        screen.clear()
        draw_grid()
        if game_over:
            screen.clear()
            music.stop()
            screen.draw.text(
                "Game Over", (WIDTH // 2 - 100, 300), color=(192, 31, 31), fontsize=50
            )
            screen.draw.text(
                "Score: " + str(score),
                (WIDTH // 2 - 100, 350),
                color=(255, 255, 255),
                fontsize=60,
            )
        else:
            for zombie in zombies:
                zombie.draw()

            hero.draw()
            for gem in gems:
                gem.draw()

            screen.draw.text(
                "Score: " + str(score), (15, 10), color=(255, 255, 255), fontsize=30
            )


pgzrun.go()
