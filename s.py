import os
import sys
import pygame as pg
import random as rm

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Obstacle:
    def __init__(self, image_path, x, y, width, height):
        self.image = pg.transform.scale(pg.image.load(image_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.rect.left = 1600  # 再度右端から登場する
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pg.init()
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    # Load images
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)

    # Get rect for the character image
    kk_rct = kk_img.get_rect()
    kk_rct.center = (300, 200)

    # Initialize obstacle list and timer
    obstacles = []
    obstacle_timer = 0
    obstacle_interval = 120  # Interval for obstacle generation (in frames)
    max_obstacles = 10
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # Handle character movement
        key_lst = pg.key.get_pressed()
        x, y = 0, 0
        if key_lst[pg.K_UP]:
            y = -1
        if key_lst[pg.K_DOWN]:
            y = 1
        if key_lst[pg.K_RIGHT]:
            x = 1
        if key_lst[pg.K_LEFT]:
            x = -1
        kk_rct.move_ip(x, y)

        # Scroll background
        z = tmr % 1600
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [1600 - z, 0])

        if z > 800:  # Fixes issue with background discontinuity
            screen.blit(bg_img, [1600 - z + 1600, 0])

        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(screen)

        # Generate new obstacle at regular intervals
        if obstacle_timer <= 0 and len(obstacle) < max_obstacles:
            x = rm.randint(800, 1600)
            y = rm.randint(100, 500)
            width = rm.randint(100, 300)
            height = 50
            obstacles.append(Obstacle("fig/obstacle.png", x, y, width, height))
            obstacle_timer = obstacle_interval
        else:
            obstacle_timer -= 1

        # Draw the character
        screen.blit(kk_img, kk_rct)

        # Update display and tick clock
        pg.display.update()
        tmr += 1
        clock.tick(60)  # Standard FPS

if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()