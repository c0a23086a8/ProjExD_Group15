import os
import sys
import pygame as pg



os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Score: #追加
    def __init__(self):
        self.value = 0
        self.timer = 0 

    def increase(self, amount):
        self.value += amount


def gamengai_rect(rect, dx, dy, screen): # 追加
    """
    画面外に行かないようにする関数
    
    """
    rect.x += dx
    rect.y += dy
    if rect.x < 0:
        rect.x = 0
    elif rect.x > screen.get_width() - rect.width:
        rect.x = screen.get_width() - rect.width
    if rect.y < 0:
        rect.y = 0
    elif rect.y > screen.get_height() - rect.height:
        rect.y = screen.get_height() - rect.height


def time(seconds): #追加
    """
    経過時間の計算をする関数
    hours   ; 時
    minutes ; 分
    seconds ; 秒
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    font = pg.font.Font(None, 36) #追加
    tmr = 0
    score = Score()#追加
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
        dx = -0.5 #追加
        dy = 0    #追加
        gamengai_rect(kk_rct, dx, dy, screen) #追加
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
        if tmr % 600 == 0: #追加    
            score.increase(1) #追加
        #追加↓
        score_text = font.render("Score: {}".format(score.value), True, (255, 255, 255))
        screen.blit(score_text, (20, 60))
        #追加↑
        pg.display.update()
        tmr += 1     
        clock.tick(200)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()