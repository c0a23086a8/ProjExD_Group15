import os
import sys
import pygame as pg
import random

screen_width, screen_height = 800, 600

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
NUM_OF_BOMBS = 5  # 爆弾の数

kkx=40
kky=40

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    global kkx,kky
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.scale(kk_img, (kkx, kky))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    tmr = 0

    kuki_img = pg.image.load("fig/kuki.png")
    kuki_img = pg.transform.scale(kuki_img, (100, 130))
    kuki_rct = kuki_img.get_rect()
    kuki_rct.topleft = (screen_width, random.randint(0, screen_height - kuki_rct.height))
    kuki_speed = -2

    kinoko_img = pg.image.load("fig/kinoko.png")
    kinoko_img = pg.transform.scale(kinoko_img, (100, 130))
    kinoko_rct = kinoko_img.get_rect()
    kinoko_rct.topleft = (screen_width, random.randint(0, screen_height - kinoko_rct.height))
    kinoko_speed = -3

    speed = 2
    kuki_timer = 0
    kuki_active = False
    kinoko_timer = 0
    kinoko_active = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_lst = pg.key.get_pressed()
        x, y = 0, 0
        if key_lst[pg.K_UP]:
            y = -1 * speed
        elif key_lst[pg.K_DOWN]:
            y = 1 * speed
        if key_lst[pg.K_RIGHT]:
            x = 1 * speed
        elif key_lst[pg.K_LEFT]:
            x = -1 * speed
        if key_lst[pg.K_q]:  # キャラ変
            kk_img = pg.image.load("fig/aitemu.gif")
            kk_img = pg.transform.scale(kk_img, (kkx, kky))
            kk_rct = kk_img.get_rect(center=kk_rct.center)
        if key_lst[pg.K_w]:  # キャラ変
            kk_img = pg.image.load("fig/3.png")
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.scale(kk_img, (kkx, kky))
            kk_rct = kk_img.get_rect(center=kk_rct.center)

        kk_rct.move_ip(x, y)

        if kk_rct.colliderect(kuki_rct):
            speed += 3
            kuki_rct.topleft = (-100, -100)  # アイテムを画面外に移動して消す

        if tmr % (20 * 60) == 0:  # 20秒ごとに
            kuki_active = True
            kuki_rct.topleft = (screen_width, random.randint(0, screen_height - kuki_rct.height))
            kuki_timer = 0

        if kuki_active:
            kuki_rct.move_ip(kuki_speed, 0)
            if kuki_rct.right < 0:
                kuki_active = False

        if tmr % (5 * 60) == 0:  # 5秒ごとに
            kinoko_active = True
            kinoko_rct.topleft = (screen_width, random.randint(0, screen_height - kinoko_rct.height))
            kinoko_timer = 0

        if kinoko_active:
            kinoko_rct.move_ip(kinoko_speed, 0)
            if kinoko_rct.right < 0:
                kinoko_active = False

        if kk_rct.colliderect(kinoko_rct):
            #kk_img = pg.transform.scale(kk_img, (kk_rct.width + 1, kk_rct.height + 1))
            kkx+=10
            kky+=10
            kk_img = pg.transform.scale(kk_img, (kkx, kky))
            
            
            kk_rct = kk_img.get_rect(center=kk_rct.center)
            kinoko_rct.topleft = (-100, -100)  # アイテムを画面外に移動して消す
            kinoko_active = False

        z = tmr % 3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z + 1600, 0])
        screen.blit(bg_img, [-z + 3200, 0])
        screen.blit(bg_img2, [-z + 4800, 0])
        screen.blit(kk_img, kk_rct)
        if kuki_active:
            screen.blit(kuki_img, kuki_rct)
        if kinoko_active:
            screen.blit(kinoko_img, kinoko_rct)

        pg.display.update()
        tmr += 1
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()