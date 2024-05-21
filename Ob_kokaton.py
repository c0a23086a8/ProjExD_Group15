import os
import sys
import pygame as pg



os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gamengai_rect(rect, screen_rect): # 追加
    rect.left = max(rect.left, screen_rect.left)
    rect.right = min(rect.right, screen_rect.right)
    rect.top = max(rect.top, screen_rect.top)
    rect.bottom = min(rect.bottom, screen_rect.bottom)


def time(seconds): #追加
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    screen_rect = screen.get_rect()# 追加
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    font = pg.font.Font(None, 36) #追加
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        key_lst = pg.key.get_pressed()
        x = -1
        y = 0
        if key_lst[pg.K_UP]:
            y = -1
        elif key_lst[pg.K_DOWN]:
            y = 1
        elif key_lst[pg.K_RIGHT]:
            x = 1
        elif key_lst[pg.K_LEFT]:
            x = -2
        kk_rct.move_ip([x, y])
        gamengai_rect(kk_rct, screen_rect) #追加
        z = tmr%3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z+1600, 0])
        screen.blit(bg_img, [-z+3200, 0])
        screen.blit(bg_img2, [-z+4800, 0])
        screen.blit(kk_img, kk_rct)
        #追加↓
        hours, minutes, seconds = time(tmr // 60)  
        time_text = font.render("Time: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), True, (255, 255, 255)) 
        screen.blit(time_text, (20, 20)) 
        #追加↑
        pg.display.update()
        tmr += 1        
        clock.tick(200)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()