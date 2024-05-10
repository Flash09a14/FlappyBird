import pygame
import time
import random
import webbrowser

pygame.init()
pygame.mixer.init()

class Button():
    def __init__(self, font_size, color, x, y):
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False
    def make(self, text):
        self.text = text
        self.button = self.font.render(str(self.text), True, self.color)
        self.button_rect = self.button.get_rect()
        self.button_rect.x = self.x
        self.button_rect.y = self.y

class SFX():
    def __init__(self, name):
        self.name = str(name)
        self.sound = pygame.mixer.Sound(self.name)
        self.volume = 1.0

    def sfx(self):
        self.sound.set_volume(self.volume)
        self.sound.play()

    def set_volume(self, volume):
        self.volume = volume

    def unload_sfx(self):
        self.sound.stop()
        self.sound = None


play_sfx = SFX("SFX\\select.wav")

def main_menu(last_score, time_taken, sfx_volume, audio_state):
    pygame.mixer.music.set_volume(sfx_volume)
    width = 1000
    height = 800
    
    scrn = pygame.display.set_mode((width, height), flags=pygame.SCALED, vsync=1)
    
    pygame.display.set_caption("Flappy Bird")

    # Run variable
    running = True

    # Font variables    
    sub_font = pygame.font.SysFont(None, 32)

    # Button color variables
    color = (255, 255, 255)
    play_color = (255, 255, 255)
    quit_color = (255, 255, 255)
    source_color = (255, 255, 255)
    options_color = (255, 255, 255)

    # Image variables
    image = pygame.image.load("player.png")
    image_size = (70, 50)
    flappy = pygame.transform.scale(image, image_size)
    image_rect = flappy.get_rect()
    image_rect.x = (width/2)-43
    image_rect.y = 650

    play_sound_played = False
    quit_sound_played = False
    source_sound_played = False
    options_sound_played = False

    # Set sound effect volume
    play_sfx.set_volume(sfx_volume)

    while running:
        for event in pygame.event.get():
            logo = Button(128, color, (width/2)-250, 60)
            logo.make("Flappy Bird")

            # Render sub-text
            sub = sub_font.render("Made by Aram 9C (This took me way too long I wanna die)", True, (255, 255, 255))
            sub_rect = sub.get_rect()
            sub_rect.x = (width/2)-300
            sub_rect.y = 175
            
            # Render stats text
            last = sub_font.render(f"Last Score: {last_score}, Time survived: {time_taken}s", True, (255, 0, 0))
            last_rect = last.get_rect()
            last_rect.x = (width/2)-300
            last_rect.y = 200


            # Render Play text
            play = Button(64, play_color, (width/2)-60, 250)
            play.make("Play")

            options = Button(64, options_color, (width/2)-105, 325)
            options.make("Options")

            # Render Quit text
            quit_button = Button(64, quit_color, (width/2)-60, 400)
            quit_button.make("Quit")

            # Render Source Code text
            source = Button(64, source_color, (width/2)-145, 475)
            source.make("Source Code")

            # Mouse variables
            mouse = pygame.mouse.get_pos()

            # Hover detection data
            hover = play.button_rect.collidepoint(mouse)
            easter_egg = logo.button_rect.collidepoint(mouse)
            quit_hover = quit_button.button_rect.collidepoint(mouse)
            source_hover = source.button_rect.collidepoint(mouse)
            options_hover = options.button_rect.collidepoint(mouse)
            rickroll_hover = image_rect.collidepoint(mouse)

            # First hover event
            if hover:
                if not play_sound_played:
                    play_sfx.sfx()
                    play_sound_played = True
                play_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    return main(inverted=False)
                    running = False
            else:
                play_color = (255, 255, 255)
                play_sound_played = False

            # Second hover event
            if easter_egg:
                color = (200, 200, 200)
                if event.type == pygame.MOUSEBUTTONUP:
                    return main(inverted=True)
                    running = False
            else:
                color = (255, 255, 255)

            # Third hover event
            if quit_hover:
                if not quit_sound_played:
                    play_sfx.sfx()
                    quit_sound_played = True
                quit_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    running = False
            else:
                quit_color = (255, 255, 255)
                quit_sound_played = False

            # Fourth hover event
            if source_hover:
                if not source_sound_played:
                    play_sfx.sfx()
                    source_sound_played = True
                source_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    webbrowser.open("https://github.com/Flash09a14/FlappyBird")
            else:
                source_sound_played = False
                source_color = (255, 255, 255)

            if options_hover:
                if not options_sound_played:
                    play_sfx.sfx()
                    options_sound_played = True
                options_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    return options_menu(audio_state)
            else:
                options_sound_played = False
                options_color = (255, 255, 255)

            # Fifth hover event
            if rickroll_hover and event.type == pygame.MOUSEBUTTONUP:
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            # Quit
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        scrn.fill((0, 0, 0))

        # Display buttons
        scrn.blit(logo.button, logo.button_rect)
        scrn.blit(sub, sub_rect)
        scrn.blit(play.button, play.button_rect)
        scrn.blit(last, last_rect)
        scrn.blit(quit_button.button, quit_button.button_rect)
        scrn.blit(source.button, source.button_rect)
        scrn.blit(options.button, options.button_rect)
        scrn.blit(flappy, image_rect)
        pygame.display.flip()

    play_sfx.unload_sfx()

def options_menu(toggled):
    width = 1000
    height = 700

    scrn = pygame.display.set_mode((width, height), flags=pygame.SCALED, vsync=1)

    running = True

    audio_color = (0, 255, 0) if toggled == True else (255, 0, 0)
    back_color = (255, 255, 255)
    audio_sound_played = False
    back_sound_played = False
    global_volume = 1.0
    if toggled == False:
        global_volume = 0.0
    else:
        global_volume = 1.0

    while running:
        for event in pygame.event.get():
            font = pygame.font.SysFont(None, 72)
            title = font.render("Options", True, (255, 255, 255))
            title_rect = title.get_rect()
            title_rect.x = (width/2)-100
            title_rect.y = 60

            audio = Button(50, audio_color, (width/2)-50, 150)
            audio.make("Audio")

            back = Button(32, back_color, (width/2)-32, 600)
            back.make("Back")

            mouse = pygame.mouse.get_pos()
            audio_hover = audio.button_rect.collidepoint(mouse)
            back_hover = back.button_rect.collidepoint(mouse)

            if audio_hover:
                if not audio_sound_played:
                    play_sfx.sfx()
                    audio_sound_played = True
                if event.type == pygame.MOUSEBUTTONDOWN and toggled == False:
                    audio_color = (0, 255, 0)
                    global_volume = 1.0
                    toggled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and toggled == True:
                    audio_color = (255, 0, 0)
                    global_volume = 0.0
                    toggled = False
            else:
                audio_sound_played = False

            if back_hover:
                back_color = (0, 255, 0)
                if not back_sound_played:
                    play_sfx.sfx()
                    back_sound_played = True
                if event.type == pygame.MOUSEBUTTONUP:
                    return main_menu(0, 0, global_volume, toggled)
            else:
                back_sound_played = False
                back_color = (255, 255, 255)

            scrn.blit(audio.button, audio.button_rect)
            scrn.blit(title, title_rect)
            scrn.blit(back.button, back.button_rect)
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
                

def main(inverted):
    width = 1200
    height = 720
    
    scrn = pygame.display.set_mode((width, height), flags=pygame.SCALED, vsync=1)
    
    pygame.display.set_caption("Flappy Bird")
    
    running = True

    global score
    global enemy_velocity

    score = 0
    enemy_velocity = 5
    background_color = (0, 0, 0) if inverted == False else (255, 255, 255)

    def handle_input():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

    def draw_text():
        text_color = (255, 255, 255) if inverted == False else (0, 0, 0)
        text = font.render(f'Score: {score}', True, text_color, None)
        text_rect = text.get_rect()
        text_rect.x = 20
        text_rect.y = 20
        other_text = font.render("You found an easter egg! Inverted mode", True, (0, 0, 0), None)
        other_textRect = other_text.get_rect()
        other_textRect.x = 20
        other_textRect.y = 50
        scrn.blit(text, text_rect)
        if inverted == True:
            scrn.blit(other_text, other_textRect)
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("player.png")
            self.image_size = (70, 50)
            self.flappy = pygame.transform.scale(self.image, self.image_size)
            self.invert = pygame.transform.flip(self.flappy, False, True) if inverted == True else pygame.transform.flip(self.flappy, False, False)
            self.rect = self.invert.get_rect() 
            self.rect.x = 100
            self.rect.y = height-100 if inverted == True else 100
            self.velocity = 0
            self.gravity_force = -0.5 if inverted == True else 0.5
            self.jump_force = 7 if inverted == True else -7
            self.terminal_velocity = 50
    
        def gravity(self):
            self.velocity += self.gravity_force
            self.rect.y += self.velocity
            if self.velocity > self.terminal_velocity:
                self.velocity = self.terminal_velocity
    
        def jump(self):
            self.velocity = self.jump_force
        
    
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, color, x):
            self.x = x
            self.width = 50
            self.gap = 300
            self.height_bottom = random.randint(100, height - self.gap)
            self.y_bottom = height - self.height_bottom
            self.height_top = height - self.gap - self.height_bottom
            self.y_top = 0
            self.color = color
            self.rect_bottom = pygame.Rect(self.x, self.y_bottom, self.width, self.height_bottom)
            self.rect_top = pygame.Rect(self.x, self.y_top, self.width, self.height_top)
            self.velocity = enemy_velocity
            self.score_counted = False
    
        def move(self):
            self.x -= self.velocity
            self.rect_bottom.x = self.x
            self.rect_top.x = self.x
    
        def draw(self):
            pygame.draw.rect(scrn, self.color, self.rect_bottom)
            pygame.draw.rect(scrn, self.color, self.rect_top)
            
        def accel(self):
            if self.x < 0 and not self.score_counted:
                global score
                score += 1
                global enemy_velocity
                enemy_velocity += 0.01
                self.score_counted = True
    
    font = pygame.font.SysFont(None, 32)
    
    player = Player()
    enemies = []
    spawn_timer = 0
    spawn_delay = 120
    clock = pygame.time.Clock()

    start = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        player.gravity()
        scrn.fill(background_color)
        draw_text()
        scrn.blit(player.invert, player.rect)
        if player.rect.y > height or player.rect.y < 0:
            running = False
            return main_menu(score, time.time()-start, 1, True)
    
        for enemy in enemies:
            enemy.move()
            enemy.draw()
            enemy.accel()
            enemy.velocity = enemy_velocity
            collide = pygame.Rect.colliderect(player.rect, enemy.rect_bottom) or pygame.Rect.colliderect(player.rect, enemy.rect_top)
            if collide:
                return main_menu(score, time.time()-start, 1, True)
                running = False
    
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            x = width
            enemies.append(Enemy((0, 0, 255) if inverted == True else (255, 0, 0), x))
            spawn_timer = 0
    
        enemies = [enemy for enemy in enemies if enemy.x > -enemy.width]
    
    
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu(0, 0, 1, True)

pygame.quit()
