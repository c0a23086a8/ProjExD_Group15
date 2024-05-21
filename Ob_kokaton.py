import os
import sys
import pygame as pg
import random as rm
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.init()
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    obstacles = []
    obstacle_tmr = 0
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        key_lst = pg.key.get_pressed()
        x = -1
        y = 0
        if key_lst[pg.K_UP]:
            y = -1
        elif key_lst[pg.K_DOWN]:
            y = 1
        elif key_lst[pg.K_RIGHT]:
            x = 2
        elif key_lst[pg.K_LEFT]:
            x = -1
        kk_rct.move_ip([x, y])
        z = tmr%3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z+1600, 0])
        screen.blit(bg_img, [-z+3200, 0])
        screen.blit(bg_img2, [-z+4800, 0])
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(screen)
            if kk_rct.colliderect(obstacle.rect): #障害物とこうかとんの衝突判定
                time.sleep() #終了
                return
        if obstacle_tmr <= 0 and len(obstacles) < 10:
            x = rm.randint(800, 1600)
            y = rm.randint(100, 500)
            width = rm.randint(100, 300)
            height = 50
            obstacles.append(Obstacle("fig/obstacle.png", x, y, width, height)) #障害物を描画する座標、ビットをランダムに指定
            obstacle_tmr = 200
        else:
            obstacle_tmr -= 1
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1        
        clock.tick(200)


"""""
Obstacleクラス
障害物を描画
"""""
class Obstacle:
    def __init__(self, image_path, x, y, width, height):
        self.image = pg.transform.scale(pg.image.load(image_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.rect.left = 1600
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()