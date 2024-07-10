import pygame
from os import listdir  # 列出指定目錄中的所有文件和目錄
from os.path import isfile, join  # isfile() 檢查指定的路徑是否對應到一個文件
import random  # 提供生成隨機數

pygame.init()  # 初始化pygame
pygame.mixer.init()
pygame.display.set_caption("pixel game")  # 設定視窗標題

BG_COLOR = (190, 190, 190)  # 設定背景顏色
WIDTH, HEIGHT = 1000, 600  # 視窗大小
FPS = 60
PLAYER_VEL = 5  # 角色速度
scroll_area_width = 525  # 滾動區域寬度

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.music.load(join("the pygame/python platform game/assets/background music", "鹿.mp3"))
pygame.mixer.music.play(-1)  # -1 表示循環播放
pygame.mixer.music.set_volume(0.1)  #調整聲音大小


#遊戲開始畫面
def show_start_screen(window):
    start_image = pygame.image.load(join("the pygame/python platform game/assets/web background", "the start.png")).convert()
    window.blit(start_image, (0,-80))

    
    button_color = (0, 255, 0)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 50)
    pygame.draw.rect(window, button_color, button_rect)

    font = pygame.font.SysFont('comicsans', 30)
    button_text = font.render('Click to Start', True, (0, 0, 0))
    window.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

    selected_character = show_character_select_screen(window)
    return selected_character

#用於水平翻轉sprites列表中的每一個圖像
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
#在點擊Click to start後顯示選角畫面
def show_character_select_screen(window):
    window.fill(BG_COLOR)  

    font = pygame.font.SysFont('comicsans', 50)
    title_surface = font.render('select your character', True, (0, 0, 0))
    window.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 50))

    character1_rect = pygame.Rect(WIDTH // 3 +60 , HEIGHT //3 , 200, 20)
    
    

    char1_text = pygame.image.load(join("the pygame/python platform game/assets/select character", "idle單.png")).convert_alpha()
    char1_text = pygame.transform.scale2x(char1_text)
    
    window.blit(char1_text, (character1_rect.x + (character1_rect.width - char1_text.get_width()) // 2, character1_rect.y + (character1_rect.height - char1_text.get_height()) // 2))
    
    pygame.display.update()

    selected_character = None
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if character1_rect.collidepoint(event.pos):
                    selected_character = 1
                    waiting = False
               
    return selected_character
#點擊角色後顯示選顏色的畫面
def show_skin_select_screen(window):
    window.fill(BG_COLOR)  

    font = pygame.font.SysFont('comicsans', 50)
    font_1 = pygame.font.SysFont('comicsans', 30)
    title_surface = font.render('choose your skin color', True, (0, 190, 190))
    
    window.blit(title_surface, (WIDTH //2 - title_surface.get_width()//2, 50))
   
    skin_rects = []

   
    skin_colors = [(255, 240, 220), (255, 218, 185), (240, 200, 160), (205, 160, 120), (165, 120, 85),(130,90,60),(100,70,50),(70,50,30),(50,30,10),(20,10,5),(0,0,0)] # 創建膚色矩形
    for i, color in enumerate(skin_colors):
        rect = pygame.Rect(50+ i * 80, HEIGHT // 2 - 100, 100, 100)
        pygame.draw.rect(window, color, rect)
        skin_rects.append(rect)

    pygame.display.update()

    selected_skin_color = None
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(skin_rects):
                    if rect.collidepoint(event.pos):
                        selected_skin_color = skin_colors[i]
                        waiting = False
                        break
               
    return selected_skin_color

#從指定目錄加載精靈表，將它們分割成單個精靈圖像，並根據需要水平翻轉這些圖像，最後將這些圖像存儲在一個dictionary中return
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    #找到包含精靈表的目錄
    path = join("the pygame/python platform game/assets", dir1, dir2) 
    #列出目錄中的所有文件
    images = [f for f in listdir(path) if isfile(join(path, f))]
    #創建一個dictionary來儲存所有的精靈圖像
    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        #將精靈表分割成單個圖像
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        # 如果需要方向翻轉，則將精圖像水平翻轉後儲存在dictinary中
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

#繪製遊戲裡的地板
def get_block(size):
    path = join("the pygame/python platform game/assets", "terrain", "grass_dirt.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

#設計角色的動作
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "pinkman", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.down_count = 0
        self.down_key_pressed = False  # 用於追縱向下鍵是否被按下
        self.hit = False
        self.hit_count = 0
    #擊中狀態
    def make_hit(self):
        self.hit = True
        self.hit_count = 0
    #快速下降
    def down(self):
       if self.y_vel >= self.GRAVITY:
            self.y_vel += self.GRAVITY * 3
            self.animation_count = 0
    
    def jump(self):
        self.y_vel = -self.GRAVITY * 6
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0 

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        # 根據重力和經過的時間增加垂直速度（y_vel）
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # 根據水平速度（x_vel）和垂直速度（y_vel）移動角色
        self.move(self.x_vel, self.y_vel)
        
        if self.hit:
            self.hit_count +=1
        if self.hit_count > fps*2:
            self.hit  =False

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.fall_count = 0
        self.y_vel = -1
    #用以定義動作時該有的圖片，以製成動畫
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet ="hit"

        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    # 更新角色的矩形位置和碰撞箱
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)#用於後續碰撞檢測
    # 繪製角色到遊戲頁面
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))



class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("traps", "fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation = "off"
        self.burning_duration = 0  # 火焰燃燒持續時間
        self.extinguish_duration = 0  # 火焰燃燒持續時間
        self.burning = False  # 火焰是否在燃燒
        self.timer_started = False  # 計時器是否已經啟動
        self.death_screen_shown = False  # 死亡畫面是否已經顯示

    def on(self):
        self.animation = "on"
        self.burning = True
        self.burning_duration = 0  # 重新開始燃燒的計時
        self.extinguish_duration = 0  # 重新開始熄滅的計時
        self.timer_started = True  # 啟動計時器

    def off(self):
        self.animation = "off"
        self.burning = False
        self.extinguish_duration = 0  # 重新開始熄滅的計時
        self.burning_duration = 0  # 重新開始燃燒的計時
        self.timer_started = False  # 計時器停止

    def loop(self):
        if self.burning:
            self.burning_duration += 1
            if self.burning_duration >= FPS * 2:  # 持續兩秒
                self.off()  # 熄滅火焰
        else:
            self.extinguish_duration += 1
            if self.extinguish_duration >= FPS * 2:  # 熄滅兩秒
                self.on()  # 重新燃燒火焰

        sprites = self.fire[self.animation]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    

def get_background(name):
    path = join("the pygame/python platform game/assets", "background", name)
    image = pygame.image.load(path).convert_alpha()
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
    return tiles, image

#繪製不同的遊戲元素到遊戲視窗上
def draw(window, background, bg_image, player, objects, offset_x):
    #繪製背景
    for tile in background:
        window.blit(bg_image, tile)
    #繪製所有遊戲物件
    for obj in objects:
        obj.draw(window, offset_x)
    #繪製角色
    player.draw(window, offset_x)
    #更新視窗
    pygame.display.update()

#用於處理角色垂直碰撞
def handle_verticle_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top 
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)

    return collided_objects

#用於處理水平碰撞
def handle_horizontal_collision(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed() #取得當前所有按鍵狀態
    
    player.x_vel = 0
    collide_left = handle_horizontal_collision(player, objects, -8)# 檢測向左移動時的碰撞
    collide_right = handle_horizontal_collision(player, objects, 8)# 檢測向右移動時的碰撞
    
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_objects.append(obj)

    #根據按鍵狀態處理角色的移動
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_DOWN]:
        player.down()  # 使向下加速

    if keys[pygame.K_DOWN]:
        if not player.down_key_pressed and player.y_vel != 0:  # 僅在 y_vel 不等於0時使用
            player.down()
            player.down_key_pressed = True
    else:
        player.down_key_pressed = False #當未按下向下鍵時，重置 down_key_pressed 為 False

    #再次處理水平碰撞，以確保角色移動方向正確
    handle_horizontal_collision(player, objects, player.x_vel)
    #檢查垂直碰撞，並處理相應的碰撞物件
    vertical_collide = handle_verticle_collision(player, objects, player.y_vel)
    to_check = [*vertical_collide]
    #如果角色碰到名為fire的且動畫為 "on" 的物件，則觸發角色受傷狀態
    for obj in to_check:
        if obj and obj.name == "fire" and obj.animation == "on":  # 確認火焰是開啟狀態
            player.make_hit()

def main(window):
    clock = pygame.time.Clock() #用於控制遊戲速度
    
    block_size = 60
    background, bg_image = get_background("blue.png") #獲取背景圖像和背景圖片
    player = Player(100, 100, 50, 50) #角色物件，初始位置和大小
    #建立fire物件並啟動
    fire = Fire(60, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    #建立地板和柱子物件列表
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size, (WIDTH * 3) // block_size)]
    column_blocks_head = [Block(0, HEIGHT - block_size * (i + 1), block_size) for i in range(HEIGHT // block_size)]

    floor = []
    for i in range(-WIDTH // block_size, (WIDTH * 3) // block_size):
        if not ( 600 <= i * block_size <= 1500):# 排除特定範圍的地板
            floor.append(Block(i * block_size, HEIGHT - block_size, block_size))
    
    # 建立漂浮的地板物件列表
    floating_floor1 = [Block(WIDTH - block_size * (i), block_size*7, block_size) for i in range(1,5)]
    floating_floor2 = [Block(WIDTH + block_size * (i), block_size*6, block_size) for i in range(5,10)]
    #合併所有物件到物件列表中
    objects = [*floor, *column_blocks_head ,*floating_floor1,*floating_floor2,fire ]
    offset_x = 0

    selected_character = show_start_screen(window)  
    selected_skin_color = show_skin_select_screen(window)  

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        
        player.loop(FPS)#角色的迴圈函式，處理角色的重力和移動
        fire.loop()#控制fire的動畫和效果
        
        handle_move(player, objects) #處理角色的移動和與物件的碰撞

        

        draw(window, background, bg_image, player, objects, offset_x)
        #控制視角的x軸偏移，使畫面跟隨角色移動
        if ((player.rect.x - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel #根據角色的速度調整x軸偏移

    pygame.quit()


if __name__ == "__main__":
    main(window)