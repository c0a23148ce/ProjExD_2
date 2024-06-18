import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


MV_DIC = {  # 移動量を表す辞書
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, +5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(+5, 0),
    pg.K_w:(+5, -5),
    pg.K_q:(-5, -5), 
    pg.K_a:(-5, +5), 
    pg.K_s:(+5, +5)
    }


MV_KK = {
    (+5, -5):135,
    (-5, -5):315, 
    (-5, +5):45, 
    (+5, +5):135,
    (0, -5):270,
    (0, +5):90, 
    (-5, 0):0, 
    (+5, 0):0
    }


#加速度のリスト
accs = [a for a in range(1, 11)]


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def roto_kk(mv) -> tuple[bool]:
     """
     MV_KKのキーを取得し、値を返す
     """
     for k, v in MV_KK.items():
         if mv is k:
             return v
        

def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def GameOver():
    return 


def bom_speed(num:int) -> tuple[bool]:
    """
    課題２：リストのタプルを返す
    """
    return tuple(accs)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bom_img = pg.Surface((20, 20))
    bom_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_img, (255, 0, 0), (10, 10), 10)
    bom_rct = bom_img.get_rect()
    bom_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    black = pg.Surface((1600, 900))
    pg.draw.rect(black,(0, 0, 0), pg.Rect(0, 0, 1600, 900))
    #Surface.set_alpha(50)

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bom_rct):
            fonto = pg.font.Font(None, 100)
            txt = fonto.render("Game Over",True, (255, 255, 255))
            screen.blit(txt, [300, 200])
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0])
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        num = 0

        for k, v in MV_DIC.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                num = roto_kk(v)
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.rotozoom(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0), num, 1.0)
        kk_rct.move_ip(sum_mv)
     
        for r in range(1, 11):
            b_img = pg.Surface((20*r, 20*r))
            pg.draw.circle(bom_img, (255, 0, 0), (10*r, 10*r), 10*r)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bom_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bom_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bom_img, bom_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
