# Libraries
import pygame
import time
import random
import webbrowser
from os import name

# Initialization
pygame.init()
pygame.mixer.init()


base_width_menu = 1280
base_height_menu = 720

base_width_game = 1280
base_height_game = 720

def scale(value, axis, screen_width, screen_height, base_width, base_height):
    if axis == 'x':
        return int(value * (screen_width / base_width))
    elif axis == 'y':
        return int(value * (screen_height / base_height))

# Button class
class Button():
    def __init__(self, base_font_size, color, screen_width, screen_height, base_y, text, select_sfx, base_res_x, base_res_y):
        self.audio_toggled = True
        self.select = select_sfx
        self.sound_played = False
        self.hover = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_color = color
        self.default_color = color
        self.text = text

        # Scale font size
        self.font_size = scale(base_font_size, 'y', screen_width, screen_height, base_res_x, base_res_y)
        self.font = pygame.font.SysFont(None, self.font_size)
        self.hovered = False

        # Scale padding
        self.padding_x = scale(50, 'x', screen_width, screen_height, base_res_x, base_res_y)

        # Scale y position
        self.y = scale(base_y, 'y', screen_width, screen_height, base_res_x, base_res_y)

        self.make()

    def make(self):
        self.button = self.font.render(str(self.text), True, self.current_color)
        self.button_rect = self.button.get_rect()
        self.button_rect.x = self.padding_x
        self.button_rect.y = self.y

    def update(self, mouse_pos, hover_color):
        if self.button_rect.collidepoint(mouse_pos):
            self.hover = True
            self.current_color = hover_color
            if not self.sound_played and self.select != None:
                self.select.sfx()
                self.sound_played = True
        else:
            self.current_color = self.default_color
            self.hover = False
            self.sound_played = False
        
        self.make()
    
    def draw(self, scrn):
        scrn.blit(self.button, self.button_rect)
    

class Text():
    def __init__(self, base_font_size, color, screen_width, screen_height, base_x, base_y, text, base_res_x, base_res_y):
        self.text = text
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color

        # Scale font size
        self.font_size = scale(base_font_size, 'y', screen_width, screen_height, base_res_x, base_res_y)
        self.font = pygame.font.SysFont(None, self.font_size)

        # Scale position
        self.x = scale(base_x, 'x', screen_width, screen_height, base_res_x, base_res_y)
        self.y = scale(base_y, 'y', screen_width, screen_height, base_res_x, base_res_y)

        self.make(self.text)

    def make(self, text):
        self.text = text
        self.rendered_text = self.font.render(str(self.text), True, self.color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y
    
    def draw(self, scrn):
        scrn.blit(self.rendered_text, self.text_rect)

# SFX class
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

# SFX initialization
if name == "nt":
    select_sfx = SFX("SFX\\select.wav")
    jump_sfx = SFX("SFX\\jump.wav")
    jump_two_sfx = SFX("SFX\\jump_two.wav")
    jump_three_sfx = SFX("SFX\\jump_three.wav")
else:
    select_sfx = SFX("SFX//select.wav")
    jump_sfx = SFX("SFX//jump.wav")
    jump_two_sfx = SFX("SFX//jump_two.wav")
    jump_three_sfx = SFX("SFX//jump_three.wav")

# Jump SFX list
jump_list = [jump_sfx, jump_two_sfx, jump_three_sfx]

print("16:9 ratio recommended (1280x720, 1920x1080, etc.). Playable in other aspect ratios, but may lead to stretched textures.")
user_width = int(input("Enter width: "))
user_height = int(input("Enter height: "))
    
# Main menu
def main_menu(last_score, time_taken, sfx_volume, audio_state, fullscreen, pillarboxing):
    # Set audio volume
    pygame.mixer.music.set_volume(sfx_volume)

    # Screen
    if fullscreen:
        scrn = pygame.display.set_mode((base_width_menu, base_height_menu), pygame.FULLSCREEN)
    else:
        scrn = pygame.display.set_mode((user_width, user_height))

    current_width, current_height = scrn.get_size()
    scale_factor_x = current_width/base_width_menu
    scale_factor_y = current_height/base_height_menu
    
    # Caption
    pygame.display.set_caption("Flappy Bird")

    # Variables and colors
    running = True
    color = (255, 255, 255)
    play_color = (255, 255, 255)
    quit_color = (255, 255, 255)
    source_color = (255, 255, 255)
    options_color = (255, 255, 255)

    # Image and rect
    image = pygame.image.load("player.png")
    image_size = ((80 * scale_factor_x), (55 * scale_factor_y))
    flappy = pygame.transform.scale(image, image_size)
    image_rect = flappy.get_rect()
    image_rect.x = current_width//2
    image_rect.y = 650 * scale_factor_y

    # SFX
    select_sfx.set_volume(sfx_volume)

    # Render sub-text
    sub = Text(32, (255,0,0), current_width, current_height, base_width_menu * 0.045, 175, "This took me way too long", base_width_menu, base_height_menu)
    # Render last score
    last_score_text = Text(32, (255,0,0), current_width, current_height, base_width_menu * 0.045, 200, f"Last Score: {last_score}", base_width_menu, base_height_menu)
    # Render time taken
    time_taken_text = Text(32, (255,0,0), current_width, current_height, base_width_menu * 0.045, 250, f"Time Taken: {time_taken}", base_width_menu, base_height_menu)

    # Render buttons
    logo = Button(128, color, current_width, current_height, 60, "Flappy Bird", None, base_width_menu, base_height_menu)
    play = Button(64, play_color, current_width, current_height, 300, "Play", select_sfx, base_width_menu, base_height_menu)
    options = Button(64, options_color, current_width, current_height, 375, "Options", select_sfx, base_width_menu, base_height_menu)
    quit_button = Button(64, quit_color, current_width, current_height, 450, "Quit", select_sfx, base_width_menu, base_height_menu)
    source = Button(64, source_color, current_width, current_height, 525, "Source Code", select_sfx, base_width_menu, base_height_menu)

    # Menu loop
    while running:
        # Event check
        for event in pygame.event.get():
            # Get mouse position
            mouse = pygame.mouse.get_pos()

            # Detect button hover
            rickroll_hover = image_rect.collidepoint(mouse)

            # Update buttons
            logo.update(mouse, (230, 230, 230))
            play.update(mouse, (0, 255, 0))
            quit_button.update(mouse, (0, 255, 0))
            source.update(mouse, (0, 255, 0))
            options.update(mouse, (0, 255, 0))

            if event.type == pygame.MOUSEBUTTONUP:
                if play.hover:
                    return main(inverted=False, volume=sfx_volume, fullscreen=fullscreen, audio_toggled=audio_state, pillarboxing=pillarboxing)
                if logo.hover:
                    return main(inverted=True, volume=sfx_volume, fullscreen=fullscreen, audio_toggled=audio_state, pillarboxing=pillarboxing)
                if quit_button.hover:
                    running = False
                    quit()
                if source.hover:
                    webbrowser.open("https://github.com/Flash09a14/FlappyBird")
                if options.hover:
                    return options_menu(audio_state, fullscreen, pillarboxing)
                if rickroll_hover:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            if event.type == pygame.QUIT:
                running = False

        # Blit everything
        scrn.fill((0, 0, 0))
        logo.draw(scrn)
        play.draw(scrn)
        quit_button.draw(scrn)
        source.draw(scrn)
        options.draw(scrn)
        last_score_text.draw(scrn)
        sub.draw(scrn)
        time_taken_text.draw(scrn)
        scrn.blit(flappy, image_rect)
        pygame.display.update()

    # Clean up audio
    select_sfx.unload_sfx()

# Options menu
def options_menu(audio_toggled, fullscreen_toggled, pillarbox_toggled):
    # Screen initialization
    if fullscreen_toggled:
        scrn = pygame.display.set_mode((base_width_menu, base_height_menu), pygame.FULLSCREEN)
    else:
        scrn = pygame.display.set_mode((user_width, user_height))

    current_width, current_height = scrn.get_size()

    title = Text(72, (255, 255, 255), current_width, current_height, 50, 100, "Options Menu", base_width_menu, base_height_menu)
    audio = Button(50, (0, 255, 0) if audio_toggled == True else (255, 0, 0), current_width, current_height, 200, "Audio Toggle", select_sfx, base_width_menu, base_height_menu)
    fullscreen = Button(50, (0, 255, 0) if fullscreen_toggled == True else (255, 0, 0), current_width, current_height, 270, "Fullscreen Toggle", select_sfx, base_width_menu, base_height_menu)
    pillarbox = Button(50, (0, 255, 0) if pillarbox_toggled == True else (255, 0, 0), current_width, current_height, 340, "Black-bars Toggle", select_sfx, base_width_menu, base_height_menu)
    back = Button(32, (255, 255, 255), current_width, current_height, 650, "Back", select_sfx, base_width_menu, base_height_menu)

    # Variables and audio
    running = True
    while running:
        if audio_toggled:
            global_volume = 1
        else:
            global_volume = 0

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            audio.update(mouse, (0, 200, 0)) if audio_toggled == True else audio.update(mouse, (200, 0, 0))
            fullscreen.update(mouse, (0, 200, 0)) if fullscreen_toggled == True else fullscreen.update(mouse, (200, 0, 0))
            pillarbox.update(mouse, (0, 200, 0) if pillarbox_toggled == True else (200, 0, 0))
            back.update(mouse, (0, 255, 0))

            if event.type == pygame.MOUSEBUTTONUP:
                if audio.hover:
                    audio_toggled = not audio_toggled
                    audio.default_color = (0, 255, 0) if audio_toggled == True else (255, 0, 0)
                    audio.update(mouse, (0, 200, 0) if audio_toggled == True else (200, 0, 0))
                if fullscreen.hover:
                    fullscreen_toggled = not fullscreen_toggled
                    fullscreen.default_color = (0, 255, 0) if fullscreen_toggled == True else (255, 0, 0)
                    fullscreen.update(mouse, (0, 200, 0) if fullscreen_toggled == True else (200, 0, 0))
                if pillarbox.hover:
                    pillarbox_toggled = not pillarbox_toggled
                    pillarbox.default_color = (0, 255, 0) if pillarbox_toggled == True else (255, 0, 0)
                    pillarbox.update(mouse, (0, 200, 0) if pillarbox_toggled == True else (200, 0, 0))
                if back.hover:
                    return main_menu(0, 0, global_volume, audio_toggled, fullscreen_toggled, pillarbox_toggled)

            if event.type == pygame.QUIT:
                running = False

        title.draw(scrn)
        audio.draw(scrn)
        fullscreen.draw(scrn)
        pillarbox.draw(scrn)
        back.draw(scrn)
        pygame.display.update()
                

def main(inverted, volume, fullscreen, audio_toggled, pillarboxing):
    if audio_toggled:
        pygame.mixer.music.set_volume(volume)
    else:
        pygame.mixer.music.set_volume(0.0)

    game_aspect = base_width_game / base_height_game

    if fullscreen:
        scrn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        screen_width, screen_height = scrn.get_size()
    else:
        scrn = pygame.display.set_mode((user_width, user_height), vsync=1)
        screen_width, screen_height = user_width, user_height

    game_surface = pygame.Surface((base_width_game, base_height_game))
    current_width, current_height = base_width_game, base_height_game

    if pillarboxing:
        window_aspect = screen_width / screen_height
        if window_aspect > game_aspect:
            scale_factor = screen_height / base_height_game
        else:
            scale_factor = screen_width / base_width_game

        scaled_width = int(base_width_game * scale_factor)
        scaled_height = int(base_height_game * scale_factor)
        offset_x = (screen_width - scaled_width) // 2
        offset_y = (screen_height - scaled_height) // 2
    else:
        scaled_width = screen_width
        scaled_height = screen_height
        offset_x = 0
        offset_y = 0

    scale_factor_x = 1
    scale_factor_y = 1


    pygame.display.set_caption("Flappy Bird")
    
    running = True

    global score
    global enemy_velocity

    score = 0
    base_velocity = 5
    enemy_velocity = base_velocity * scale_factor_x
    spawn_delay = int(100 * (base_width_game / current_width))
    background_color = (0, 0, 0) if not inverted else (255, 255, 255)

    def handle_input():
        space_pressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not space_pressed:
                player.play_jump = False
                player.jump()
                space_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    def draw_text():
        text_color = (255, 255, 255) if not inverted else (0, 0, 0)
        text = font.render(f'Score: {score}', True, text_color, None)
        text_rect = text.get_rect()
        text_rect.x = int(20 * scale_factor_x)
        text_rect.y = int(20 * scale_factor_y)
        other_text = font.render("You found an easter egg! Inverted mode", True, (0, 0, 0), None)
        other_text_rect = other_text.get_rect()
        other_text_rect.x = int(20 * scale_factor_x)
        other_text_rect.y = int(50 * scale_factor_y)
        game_surface.blit(text, text_rect)
        if inverted:
            game_surface.blit(other_text, other_text_rect)
    
    class Player(pygame.sprite.Sprite):
        def __init__(self, scale_factor_x, scale_factor_y, inverted):
            super().__init__()
            self.image = pygame.image.load("player.png")
            self.image_size = (
                int(80 * scale_factor_x),
                int(55 * scale_factor_y)
            )
            self.flappy = pygame.transform.scale(self.image, self.image_size)
            self.invert = pygame.transform.flip(self.flappy, False, inverted)
            self.rect = self.invert.get_rect()
            self.rect.x = int(100 * scale_factor_x)
            base_y = base_height_game - 100 if inverted else 100
            self.rect.y = int(base_y * scale_factor_y)
            self.velocity = 0
            self.gravity_force = (0.5 * scale_factor_y) if not inverted else (-0.5 * scale_factor_y)
            self.jump_force = (-7 * scale_factor_y) if not inverted else (7 * scale_factor_y)
            self.terminal_velocity = 50 * scale_factor_y
            self.play_jump = False
    
        def gravity(self):
            self.velocity += self.gravity_force
            self.rect.y += self.velocity
            if abs(self.velocity) > self.terminal_velocity:
                self.velocity = self.terminal_velocity if self.velocity > 0 else -self.terminal_velocity
    
        def jump(self):
            self.velocity = self.jump_force
            if not self.play_jump:
                self.jump_sound = random.choice(jump_list)
                self.jump_sound.sfx()
                self.play_jump = True
        
    
    class Walls:
        def __init__(self, color, x, scale_factor_x, scale_factor_y, current_height):
            self.x = x
            self.width = int(50 * scale_factor_x)
            self.gap = int(300 * scale_factor_y)
            min_height = int(100 * scale_factor_y)
            max_height = current_height - self.gap
            self.height_bottom = random.randint(min_height, max_height)
            self.y_bottom = current_height - self.height_bottom
            self.height_top = current_height - self.gap - self.height_bottom
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
            pygame.draw.rect(game_surface, self.color, self.rect_bottom)
            pygame.draw.rect(game_surface, self.color, self.rect_top)
            
        def accel(self):
            if self.x < 0 and not self.score_counted:
                global score
                score += 1
                global enemy_velocity
                enemy_velocity += 0.1 * scale_factor_x
                self.score_counted = True

    font_size = int(32 * scale_factor_y)
    font = pygame.font.SysFont(None, font_size)
    
    player = Player(scale_factor_x, scale_factor_y, inverted)
    for i in jump_list:
        i.set_volume(volume)
    walls = []
    spawn_timer = 0
    clock = pygame.time.Clock()

    start = time.time()
    countdown_seconds = 3
    while time.time() - start < countdown_seconds:
        remaining_time = countdown_seconds - int(time.time() - start)
        countdown_text = font.render(f'Game starting in {remaining_time} seconds', True, (255, 255, 255) if not inverted else (0, 0, 0))
        countdown_rect = countdown_text.get_rect(center=(current_width / 2, current_height / 2))
        scrn.fill((0,0,0) if not inverted else (255, 255, 255))
        scrn.blit(countdown_text, countdown_rect)
        pygame.display.flip()
        clock.tick(60)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_input()

        player.gravity()
        game_surface.fill(background_color)
        draw_text()
        game_surface.blit(player.invert, player.rect)
        if player.rect.y > current_height or player.rect.y < 0:
            running = False
            return main_menu(score, f"{(time.time()-start):.2f}s", volume, True if volume > 0 else False, fullscreen, pillarboxing)
    
        for wall in walls:
            wall.move()
            wall.draw()
            wall.accel()
            wall.velocity = enemy_velocity
            collide = pygame.Rect.colliderect(player.rect, wall.rect_bottom) or pygame.Rect.colliderect(player.rect, wall.rect_top)
            if collide:
                return main_menu(score, f"{(time.time()-start):.2f}s", volume, True if volume > 0 else False, fullscreen, pillarboxing)
    
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            x = current_width
            color = (0, 0, 255) if inverted else (255, 0, 0)
            walls.append(Walls(color, x, scale_factor_x, scale_factor_y, current_height))
            spawn_timer = 0
    
        walls = [enemy for enemy in walls if enemy.x > -enemy.width]

        scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
        scrn.fill((0,0,0))
        scrn.blit(scaled_surface, (offset_x, offset_y))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu(0, 0, 1, True, False, False)

pygame.quit()
