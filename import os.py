import os
import sys
import random
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Coin:
    """
    コインをランダムに生成して右から左へ流れるクラス
    """
    def __init__(self, screen_width, screen_height):
        self.original_image = pg.image.load("fig/coin.png")
        self.image = pg.transform.scale(self.original_image, (100, 100))  # コインのサイズを小さくする
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 3
        self.active = False  # コインが画面に表示されているかどうかを管理
        self.spawn_timer = 0  # コインの生成間隔を管理

    def reset(self):
        self.rect.x = self.screen_width
        self.rect.y = random.randint(0, self.screen_height - self.rect.height)
        self.speed = 3
        self.active = True

    def update(self):
        if self.active:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

class Score:
    """
    取ったコインの数をスコアとして表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 36)
        self.score = 0

    def increment(self):
        self.score += 1

    def draw(self, screen):
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

def main():
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    coin = Coin(800, 600)
    score = Score()

    spawn_interval = 100  # コインの生成間隔（フレーム数）
    spawn_timer = 0  # スポーンタイマー

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        key_lst = pg.key.get_pressed()
        x = -1
        y = 0
        if key_lst[pg.K_UP]:
            y = -1
        if key_lst[pg.K_DOWN]:
            y = 1
        if key_lst[pg.K_RIGHT]:
            x = 2
        if key_lst[pg.K_LEFT]:
            x = -1
        kk_rct.move_ip([x, y])

        # コインの生成を制御
        if not coin.active:
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                coin.reset()
                spawn_timer = 0

        coin.update()
        if coin.active and kk_rct.colliderect(coin.rect):
            score.increment()
            coin.active = False  # コインを非表示にする

        z = tmr % 3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z + 1600, 0])
        screen.blit(bg_img, [-z + 3200, 0])
        screen.blit(bg_img2, [-z + 4800, 0])
        screen.blit(kk_img, kk_rct)

        coin.draw(screen)
        score.draw(screen)

        pg.display.update()
        tmr += 1        
        clock.tick(200)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
