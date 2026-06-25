import pgzrun
from pygame import Rect

# Ekran Boyutları
WIDTH = 800
HEIGHT = 600
TITLE = "Ninja Runner"

# Oyunun o anki durumunu kontrol eden değişken
# "menu", "game", "game_over", "victory"
game_state = "menu"


sound_enabled= True # Ses efektleri var ya da yok
# Oyuncu değerleri
player_lives = 3
score = 0
max_score_to_win = 5000  # Bu skora ulaşınca oyun kazanılır


class MenuButton:
    def __init__(self, text,x,y ,widthf, height,color, text_color):
        self.text = text 
        self.rect = Rect(x, y, widthf, height)
        self.color = color
        self.text_color = text_color

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color=self.text_color)
    
    def is_clicked(self,pos):
        # Fare ile tıklanan noktanın (pos) butonun içinde olup olmadığını kontrol ediyoruz
        return self.rect.collidepoint(pos)
    


class MenuButton(Actor):
    def __init__(self, image_name, pos):
        super().__init__(image_name, pos)

    def is_clicked(self, pos):

        return self.collidepoint(pos)

# Buton boyutları
button_width = 200
button_height = 50
start_x = (WIDTH - button_width) // 2
# Tüm butonların konumu
btn_start = MenuButton("btn_play", (220, 400))
btn_sound = MenuButton("btn_sound_on", (400, 400))
btn_exit = MenuButton("btn_exit", (580, 400))


class Hero(Actor):
    def __init__(self, pos):
        super().__init__("hero_idle1", pos)
        
        # Animasyon kare listeleri (images klasöründeki dosya isimleri)
        self.idle_frames = ["hero_idle1", "hero_idle2"]
        self.run_frames = ["hero_run1", "hero_run2", "hero_run3"]
        
        self.current_frame = 0
        self.animation_time = 0
        self.state = "idle" # "idle" (durma) veya "run" (koşma)
        
        # Fizik ve Hareket Değişkenleri
        self.velocity_y = 0  # Dikey hız (Yerçekimi için)
        self.is_on_ground = False
        self.speed = 5

    def animate(self):
        # Animasyon hızını kontrol etmek için zamanlayıcı
        self.animation_time += 1
        
        # Her 6 karede bir (yaklaşık 0.1 saniye) resmi değiştirir
        if self.animation_time >= 6:
            self.animation_time = 0
            
            if self.state == "idle":
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]
            elif self.state == "run":
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.image = self.run_frames[self.current_frame]

    def update_physics(self):
        if not self.is_on_ground:
            self.velocity_y += 0.5  # Aşağı doğru ivmelenme
            
        self.y += self.velocity_y
        
        # Karakter ekranın altına (örneğin y=500'e) ulaştığında dursun
        if self.y >= 500:
            self.y = 500
            self.velocity_y = 0
            self.is_on_ground = True

    def jump(self):
        # Sadece yerdeyken zıplayabilir
        if self.is_on_ground:
            self.velocity_y = -12
            self.is_on_ground = False
            self.state = "idle"
            # ses on ise zıplama sesi
            if sound_enabled:
                sounds.jump_sound.play()

class Enemy(Actor):
    def __init__(self, image_base, pos, limit_left, limit_right, speed=3):
        # İlk görselle başlatıyoruz
        super().__init__(image_base + "1", pos)
        
        self.frames = [image_base + "1", image_base + "2"]
        self.current_frame = 0
        self.animation_time = 0
        
        
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.speed = speed
        self.direction = 1  # 1: Sağa, -1: Sola hareket

    def patrol(self):
        # Sağa veya sola hareket ettiriyoruz
        self.x += self.speed * self.direction
        
        # Sınırlara ulaştıysa yönünü tersine çevir
        if self.x >= self.limit_right:
            self.direction = -1
        elif self.x <= self.limit_left:
            self.direction = 1

    def animate(self):
        self.animation_time += 1
        if self.animation_time >= 8:  # 8 karede bir resmi değiştir
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Projectile(Actor):
    def __init__(self, pos):
        super().__init__("shuriken", pos)
        self.speed = 10

    def update(self):
        self.x += self.speed # Yıldız sağa doğru uçar

def draw():

    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "victory":
        draw_victory()


def update():
    if game_state =="game":
        update_game()

def draw_menu():
    screen.fill((40,44,52))
    screen.draw.text("Ninja Runner", center=(WIDTH/2, 150), fontsize=60, color="white")
    
    btn_start.draw()
    btn_sound.draw()
    btn_exit.draw()


def draw_game():
    screen.fill((50, 50, 50))  # Oyun ekranı için gri arka plan
    # Geçici bir yer çizgisi çizelim
    screen.draw.filled_rect(Rect(0, 532, WIDTH, 68), (34, 49, 63))
    
    # Kahramanımızı ekrana çiziyoruz
    player.draw()

    # Listedeki tüm düşmanları ekrana çiziyoruz
    for enemy in enemies:
        enemy.draw()

    # Sol üste Can bilgisini kırmızı renkte yazdıralım
    screen.draw.text(f"LIVES: {player_lives}", (20, 20), fontsize=35, color="red")
    
    # Sağ üste Skor bilgisini altın/sarı renkte yazdıralım
    screen.draw.text(f"SCORE: {score}/{max_score_to_win}", (WIDTH - 250, 20), fontsize=35, color="gold")

    # Mermileri ekrana çizdir
    for proj in projectiles:
        proj.draw() 


def draw_game_over():
    screen.fill((30, 0, 0)) # Koyu kırmızı arka plan
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=70, color="red")
    screen.draw.text("Press 'R' to Restart or 'M' for Main Menu", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

def draw_victory():
    screen.fill((0, 30, 0)) # Koyu yeşil arka plan
    screen.draw.text("VICTORY!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=70, color="green")
    screen.draw.text("Press 'R' to Play Again", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

def update_game():
    global player_lives, game_state, score, projectiles
    
    player.state = "idle"
    
    # Arka planın ilerlemesi (Kamera kaydırma mantığı)
    scroll_speed = 0
    if keyboard.right or keyboard.d:
        player.state = "run"
        scroll_speed = player.speed
    elif keyboard.left or keyboard.a:
        if player.x > 50:
            player.x -= player.speed
            player.state = "run"
            
    # Dünyayı sola kaydırarak sonsuz runner hissi oluşturma
    if scroll_speed > 0:
        for enemy in enemies:
            enemy.x -= scroll_speed
            enemy.limit_left -= scroll_speed
            enemy.limit_right -= scroll_speed

    # Zıplama Kontrolü
    if keyboard.up or keyboard.space:
        player.jump()
        
    player.update_physics()
    player.animate()

    # Tüm düşmanları yürüt ve canlandır
    for enemy in enemies:
        enemy.patrol()
        enemy.animate()

    # Mermileri hareket ettir
    for proj in projectiles[:]:
        proj.update()
        if proj.x > WIDTH:
            projectiles.remove(proj)

    # Mermi ile Düşman çarpışması (Düşmanı Yok Etme)
    for proj in projectiles[:]:
        for enemy in enemies[:]:
            if proj.colliderect(enemy):
                if proj in projectiles:
                    projectiles.remove(proj)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 50 

    # Zamanla skoru artır
    score += 1
    
    # Çarpışma Kontrolü: Oyuncu ile Düşman
    for enemy in enemies:
        if player.colliderect(enemy):
            player_lives -= 1
            
            if sound_enabled:
                sounds.hit_sound.play()
                
            # Oyuncuyu başlangıç noktasına güvenle gönder
            player.x = 100
            player.y = 500
            player.velocity_y = 0
                
            # Can bittiyse oyunu sonlandır
            if player_lives <= 0:
                game_state = "game_over"
                break  # Döngüden güvenle çıkış yap
                
    # Kazanma durumu kontrolü
    if score >= max_score_to_win:
        game_state = "victory"
    


def on_mouse_down(pos):
    global game_state, sound_enabled
    
    # Eğer ana menüdeysek tıklamaları kontrol et
    if game_state == "menu":
        if btn_start.is_clicked(pos):
            game_state = "game" # Oyunu başlatır
            if sound_enabled:
                music.play("bg_music") # Oyun başlayınca müziği çal

        elif btn_sound.is_clicked(pos):
            sound_enabled = not sound_enabled
            if sound_enabled:
                btn_sound.image = "btn_sound_on"  # Resmini ses açık yap
                music.play("bg_music")
            else:
                btn_sound.image = "btn_sound_off" # Resmini ses kapalı yap
                music.stop() # Müziği sustur
                
        elif btn_exit.is_clicked(pos):
            import sys
            sys.exit() # Oyundan güvenli çıkış yap

def on_key_down(key):
    global game_state, player_lives, score, projectiles
    
    if game_state == "game":
        if key == keys.F:
            # Karakterin önünden fırlatılacak mermi ekle
            new_proj = Projectile((player.x + 20, player.y))
            projectiles.append(new_proj)
            
    # Eğer oyun bittiyse veya kazanıldıysa yeniden başlatma kontrolleri
    if game_state in ["game_over", "victory"]:
        if key == keys.R:
            player_lives = 3
            score = 0
            player.x = 100
            player.y = 500
            projectiles.clear() # Yeniden başlatınca mermileri temizle
            game_state = "game"
        elif key == keys.M:
            player_lives = 3
            score = 0
            projectiles.clear()
            game_state = "menu"

# Kahramanımızı ekranın sol tarafında, taban hizasında başlatıyoruz
player = Hero((100, 500))

# 1. Düşman: 300 ile 500 piksel arasında devriye gezecek
enemy1 = Enemy("enemy_walk", (400, 500), limit_left=300, limit_right=500, speed=2)

# 2. Düşman: 550 ile 750 piksel arasında biraz daha hızlı devriye gezecek
enemy2 = Enemy("enemy_walk", (650, 500), limit_left=550, limit_right=750, speed=4)

# Tüm düşmanları tek bir listede topluyoruz
enemies = [enemy1, enemy2]
# Mermileri tutacak listemiz
projectiles = []

pgzrun.go()