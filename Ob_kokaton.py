import os
import sys
import pygame as pg
import random
kkx=40
kky=40

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def aitemu(kinoko_active, kinoko_rct, kinoko_img, kk_rct, kk_img, tmr):
    global kkx,kky
    if tmr % (5 * 60) == 0:  # 5秒ごとに 追加
        kinoko_active = True  # 追加
        kinoko_rct.topleft = (800, random.randint(0, 600 - kinoko_rct.height))  # 追加

    if kinoko_active:  # 追加
        kinoko_rct.move_ip(-3, 0)  # 追加
        if kinoko_rct.right < 0:  # 追加
            kinoko_active = False  # 追加

    if kk_rct.colliderect(kinoko_rct):  # 追加
        kkx+=10
        kky+=10
        kk_img = pg.transform.scale(kk_img, (kkx, kky))  # 追加
        kk_rct = kk_img.get_rect(center=kk_rct.center)  # 追加
        kinoko_rct.topleft = (-100, -100)  # アイテムを画面外に移動して消す 追加
        kinoko_active = False  # 追加

    return kinoko_active, kinoko_rct, kk_img

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.scale(kk_img, (kkx, kky))
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    tmr = 0

    kinoko_img = pg.image.load("fig/kinoko.png")  # 追加
    kinoko_rct = kinoko_img.get_rect()  # 追加
    kinoko_rct.topleft = (800, random.randint(0, 600 - kinoko_rct.height))  # 追加
    kinoko_active = False  # 追加

    speed = 2

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

        kk_rct.move_ip(x, y)

        kinoko_active, kinoko_rct, kk_img = aitemu(kinoko_active, kinoko_rct, kinoko_img, kk_rct, kk_img, tmr)  # 追加

        z = tmr % 3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z + 1600, 0])
        screen.blit(bg_img, [-z + 3200, 0])
        screen.blit(bg_img2, [-z + 4800, 0])
        screen.blit(kk_img, kk_rct)
        if kinoko_active:  # 追加
            screen.blit(kinoko_img, kinoko_rct)  # 追加

        pg.display.update()
        tmr += 1
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()