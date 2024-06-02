import os
import sys
import random
import pygame as pg
import time
import math

kkx = 40
kky = 40

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def aitemu(kinoko_active, kinoko_rct, kinoko_img, kk_rct, kk_img, tmr):
    global kkx, kky
    if tmr % (5 * 60) == 0:  # 5秒ごとに追加
        kinoko_active = True
        kinoko_rct.topleft = (800, random.randint(0, 600 - kinoko_rct.height))

    if kinoko_active:
        kinoko_rct.move_ip(-3, 0)
        if kinoko_rct.right < 0:
            kinoko_active = False

    if kk_rct.colliderect(kinoko_rct):
        kkx += 10
        kky += 10
        kk_img = pg.transform.scale(kk_img, (kkx, kky))
        kk_rct = kk_img.get_rect(center=kk_rct.center)
        kinoko_rct.topleft = (-100, -100)
        kinoko_active = False

    return kinoko_active, kinoko_rct, kk_img

class title():
    def __init__(self):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 70)
        self.text = self.font.render("さけろ!こうかとん", True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(800 / 2, 600 / 2))
        self.bg_img = pg.image.load("fig/pg_bg.jpg")

    def update(self, screen: pg.Surface):
        screen.blit(self.bg_img, [0, 0])
        screen.blit(self.text, self.text_rect)
        pg.display.update()
        pg.display.flip()

class gameover():
    def __init__(self):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 70)
        self.text = self.font.render("Game Over", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(800 / 2, 600 / 2))

    def update(self, screen: pg.Surface):
        over_img = pg.Surface((800, 600))
        pg.draw.rect(over_img, (0, 0, 0), (0, 0, 800, 600), 0)
        over_img.set_alpha(1)
        screen.blit(over_img, [0, 0])
        screen.blit(self.text, self.text_rect)
        pg.display.update()
        pg.display.flip()

class die():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.circles = 6
        self.radius = 0
        self.angle = 2 * math.pi / self.circles

    def update(self, screen: pg.Surface):
        for i in range(self.circles):
            a = self.angle * i
            x = self.x + int(math.cos(a) * self.radius)
            y = self.y + int(math.sin(a) * self.radius)
            pg.draw.circle(screen, (255, 0, 0), (x, y), 30)
        pg.display.flip()

class zanki():
    def __init__(self):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.color = (0, 0, 255)
        self.value = 2  # 残機
        self.image = self.font.render(f"残機: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 50

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"残機: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

class Coin:
    """
    コインをランダムに生成して描画するクラス
    """
    def __init__(self, screen_width, screen_height):
        self.original_image = pg.image.load("fig/coin.png")  # コインの画像を読み込む
        self.image = pg.transform.scale(self.original_image, (80, 80))  # コインの大きさを決定
        self.rect = self.image.get_rect()  # コインの画像の短形を取得
        self.screen_width = screen_width  # 画面の幅を設定
        self.screen_height = screen_height  # 画面の高さを設定
        self.speed = 3  # コインの初期速度を設定
        self.active = False  # コインが画面に表示されているかどうかを確認する

    def reset(self):
        self.rect.x = self.screen_width  # コインの初期位置を設定
        self.rect.y = random.randint(0, self.screen_height - self.rect.height)  # コインの初期位置を画面内のランダムな高さに設定
        self.speed = 3  # コインの速度を設定
        self.active = True  # コインをアクティブにする

    def update(self):
        if self.active:
            self.rect.x -= self.speed  # コインを移動させる
            if self.rect.right < 0:
                self.active = False  # コインが画面外に出たときに、非アクティブにする

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)  # コインを描画する

class Score:
    """
    取ったコインの数をスコアとして表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 36)  # フォントを設定
        self.score = 0  # スコアを初期化
        self.timer = 0  # 追加

    def increment(self):
        self.score += 1  # スコアを1増加
        
    def increase(self, amount):  # 追加
        self.score += amount

    def draw(self, screen):
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_surf, (20, 60))  # スコアのテキストを描画

def gamengai_rect(rect, screen):
    """
    画面外に行かないようにする関数
    """
    if rect.x < 0:
        rect.x = 0
    elif rect.x > screen.get_width() - rect.width:
        rect.x = screen.get_width() - rect.width
    if rect.y < 0:
        rect.y = 0
    elif rect.y > screen.get_height() - rect.height:
        rect.y = screen.get_height() - rect.height

def time(seconds):
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
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.scale(kk_img, (kkx, kky))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    obstacles = []
    obstacle_timer = 0
    obstacle_interval = 120
    max_obstacles = 10
    title_screen = title()
    over = gameover()
    dead = die()
    start = True
    end = False
    anime = True
    frame = 0
    zan = zanki()

    coin = Coin(800, 600)
    score = Score()

    spawn_interval = 100  # コインの生成間隔
    spawn_timer = 0  # タイマーの初期化

    font = pg.font.Font(None, 36)  # 追加
    tmr = 0

    kinoko_img = pg.image.load("fig/kinoko.png")
    kinoko_img = pg.transform.scale(kinoko_img, (80, 80))
    kinoko_rct = kinoko_img.get_rect()
    kinoko_rct.topleft = (800, random.randint(0, 600 - kinoko_rct.height))
    kinoko_active = False
    speed = 2

    z = 0  # 背景スクロール用変数

    while True:
        while start:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        start = False
                        zan.value = 2
                        # Reset the game variables
                        obstacles.clear()
                        score.score = 0
                        tmr = 0
                        z = 0
            title_screen.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    zan.value -= 1

        if zan.value == 0:
            while anime:
                screen.blit(bg_img, [-z, 0])
                screen.blit(bg_img2, [-z + 1600, 0])
                screen.blit(bg_img, [-z + 3200, 0])
                screen.blit(bg_img2, [-z + 4800, 0])
                frame += 1
                if frame == 80:
                    anime = False
                    frame = 0
                dead.update(screen)
                dead.radius += 2
                pg.time.Clock().tick(60)
            dead.radius = 0
            anime = True
            end = True

        while end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        start = True
                        end = False
            over.update(screen)
        
        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP]:
            kk_rct.move_ip(0, -3)
        if key_lst[pg.K_DOWN]:
            kk_rct.move_ip(0, 3)
        if key_lst[pg.K_RIGHT]:
            kk_rct.move_ip(3, 0)
        if key_lst[pg.K_LEFT]:
            kk_rct.move_ip(-3, 0)

        kinoko_active, kinoko_rct, kk_img = aitemu(kinoko_active, kinoko_rct, kinoko_img, kk_rct, kk_img, tmr)

        if not coin.active:
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                coin.reset()
                spawn_timer = 0

        coin.update()
        if coin.active and kk_rct.colliderect(coin.rect):
            score.increment()
            coin.active = False

        gamengai_rect(kk_rct, screen)

        z = tmr % 3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z + 1600, 0])
        screen.blit(bg_img, [-z + 3200, 0])
        screen.blit(bg_img2, [-z + 4800, 0])
        screen.blit(kk_img, kk_rct)
        if kinoko_active:
            screen.blit(kinoko_img, kinoko_rct)
        if zan.value != 0:
            if obstacle_timer <= 0 and len(obstacles) < max_obstacles:
                x = random.randint(800, 1600)
                y = random.randint(100, 500)
                width = random.randint(100, 300)
                height = 50
                obstacles.append(Obstacle("fig/obstacle.png", x, y, width, height))
                obstacle_timer = obstacle_interval
            else:
                obstacle_timer -= 1
            for obstacle in obstacles:
                obstacle.update()
                obstacle.draw(screen)
                if kk_rct.colliderect(obstacle.rect):
                    zan.value -= 1
                    obstacles.remove(obstacle)  # 追加：ぶつかった障害物をリストから削除

        coin.draw(screen)
        score.draw(screen)

        hours, minutes, seconds = time(tmr // 200)
        time_text = font.render("Time: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), True, (255, 255, 255))
        screen.blit(time_text, (20, 20))

        if tmr % 2000 == 0:
            score.increase(1)
        dead.x = kk_rct.x
        dead.y = kk_rct.y
        zan.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(60)

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
