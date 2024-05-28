import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    k_img  = pg.image.load("fig/3.png")        #問2
    k_img  = pg.transform.flip(k_img,True,False)
    bg2_img= pg.transform.flip(bg_img,True,False)
    key_lst= pg.key.get_pressed()
    screen.blit(k_img, [300,200])
    k_rct  = k_img.get_rect() #rect取得
    k_rct.center = 300,200 
    a=0
    b=0
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        key_lst= pg.key.get_pressed()
        if key_lst[pg.K_UP]:
            lst=[-1,-1]
            #k_rct.move_ip((0,-1))
        elif key_lst[pg.K_LEFT]:
            lst=[-1,0]
            #k_rct.move_ip((-1,0))
        elif key_lst[pg.K_DOWN]:
            lst=[-1,+1]
            #k_rct.move_ip((0,+1,))
        elif key_lst[pg.K_RIGHT]:
            lst=[+2,0]
            #k_rct.move_ip((+2,0))
        else:
            lst=[-1,0]
            #k_rct.move_ip((-1,0))
        k_rct.move_ip(lst)
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg2_img, [-x+1600, 0])
        screen.blit(bg_img, [-x+3200, 0])
        screen.blit(bg2_img, [-x+4800, 0])
        screen.blit(k_img, k_rct)
        pg.display.update()
        if key_lst[pg.K_RIGHT]:
            tmr += 1
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()