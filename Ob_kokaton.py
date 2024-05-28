import os
import sys
import random
import pygame as pg



os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        if self.active == True:
            self.rect.x -= self.speed  # コインを移動させる
            if self.rect.right < 0:
                self.active = False  # コインが画面外に出たときに、非アクティブにする

    def draw(self, screen):
        if self.active == True:
            screen.blit(self.image, self.rect)  # コインを描画する

class Score:
    """
    取ったコインの数をスコアとして表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 36)  # フォントを設定
        self.score = -1  # スコアを初期化
        self.timer = 0  # 追加

    def increment(self):
        self.score += 1  # スコアを1増加
        
    def increase(self, amount):#追加
        self.score += amount

    def draw(self, screen):
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_surf, (20, 60))  # スコアのテキストを描画


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

    spawn_interval = 100  # コインの生成間隔
    spawn_timer = 0  # タイマーの初期化


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
        if key_lst[pg.K_DOWN]:
            y = 1
        if key_lst[pg.K_RIGHT]:
            x = 2
        if key_lst[pg.K_LEFT]:
            x = -1

        kk_rct.move_ip([x, y])

        if not coin.active == True:  # コインの生成を操作
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                coin.reset()
                spawn_timer = 0

        coin.update()  # コインの更新
        if coin.active == True and kk_rct.colliderect(coin.rect):  # こうかとんがコインに衝突したときの処理
            score.increment()
            coin.active = False


        dx = -0.5 #追加
        dy = 0    #追加
        gamengai_rect(kk_rct, dx, dy, screen) #追加

        z = tmr%3200
        screen.blit(bg_img, [-z, 0])
        screen.blit(bg_img2, [-z+1600, 0])
        screen.blit(bg_img, [-z+3200, 0])
        screen.blit(bg_img2, [-z+4800, 0])
        screen.blit(kk_img, kk_rct)


        coin.draw(screen)  # コインの描画
        score.draw(screen)  # スコアの描画


        #追加↓
        hours, minutes, seconds = time(tmr // 60)  
        time_text = font.render("Time: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), True, (255, 255, 255)) 
        screen.blit(time_text, (20, 20)) 
        #追加↑
        if tmr % 600 == 0: #追加    
            score.increase(1) #追加

        pg.display.update()
        tmr += 1     
        clock.tick(200)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()