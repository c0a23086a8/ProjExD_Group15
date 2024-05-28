import os
import sys
import pygame as pg
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#タイトル画面
class title():
        def __init__(self):
            self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 70)
            self.text = self.font.render("さけろ!こうかとん", True, (0, 0, 0))
            self.text_rect = self.text.get_rect(center=(800/2,600/2))
            self.bg_img = pg.image.load("fig/pg_bg.jpg")
        def update(self,screen: pg.Surface):
            screen.blit(self.bg_img, [0, 0])
            screen.blit(self.text, self.text_rect)
            pg.display.update()
            pg.display.flip()
#ゲームオーバー画面
class gameover():
        def __init__(self):
            self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 70)
            self.text = self.font.render("Game Over", True, (255, 255, 255))
            self.text_rect = self.text.get_rect(center=(800/2,600/2))

        def update(self,screen: pg.Surface):
            over_img = pg.Surface(( 800, 600 ))
            pg.draw.rect(over_img, (0, 0, 0),(0, 0, 800, 600) , 0)
            over_img.set_alpha( 1 )
            screen.blit(over_img,[0, 0])
            screen.blit(self.text, self.text_rect)
            pg.display.update()
            pg.display.flip()
#死亡時演出
class die():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.circles = 6
        self.radius = 0
        self.angle = 2*math.pi/self.circles
    def update(self,screen:pg.Surface):
        for i in range(self.circles):
            a = self.angle * i
            x = self.x + int(math.cos(a) * self.radius)
            y = self.y + int(math.sin(a) * self.radius)
            pg.draw.circle(screen, (255, 0, 0), (x, y), 30)
        pg.display.flip()
#残機処理
class zanki():
    def __init__(self):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.color = (0, 0, 255)
        self.value = 2 #残機
        self.image = self.font.render(f"残機: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 50
    def update(self, screen:pg.surface):
        self.image = self.font.render(f"残機: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("さけろ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    title_screen = title()
    over = gameover()
    zan = zanki()
    dead = die()
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    tmr = 0
    start = True
    end = False
    anime = True
    frame = 0
    while True:
        while start:
                #タイトルスクリーンループ
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                      if event.key == pg.K_RETURN:
                        start = False
                        zan.value = 2
                        kk_rct.center = 300, 200
                title_screen.update(screen)
        #試験残機減らす試験
        for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                      if event.key == pg.K_q:
                        zan.value -= 1
        #死亡時演出
        if zan.value == 0:
            while anime:
                screen.blit(bg_img, [-z, 0])
                screen.blit(bg_img2, [-z+1600, 0])
                screen.blit(bg_img, [-z+3200, 0])
                screen.blit(bg_img2, [-z+4800, 0])
                frame +=1
                if frame == 80:
                    anime = False
                    frame = 0
                dead.update(screen)
                dead.radius += 2
                pg.time.Clock().tick(60)
            dead.radius = 0
            anime = True
            end = True
        #ゲームオーバー画面ループ
        while end:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                      if event.key == pg.K_RETURN:
                           end = False
                           start = True
            over.update(screen)
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
            x = 2
        elif key_lst[pg.K_LEFT]:
            x = -1
        kk_rct.move_ip([x, y])
        z = tmr%3200
        dead.x = kk_rct.x
        dead.y = kk_rct.y 
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z+1600, 0])
        screen.blit(bg_img, [-z+3200, 0])
        screen.blit(bg_img2, [-z+4800, 0])
        screen.blit(kk_img, kk_rct)
        zan.update(screen)
        pg.display.update()
        tmr += 1        
        clock.tick(200)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()