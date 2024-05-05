import pygame
import time
import random
import webbrowser

pygame.init()

def main_menu(last_score, time_taken):
    width = 1000
    height = 700
    
    scrn = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption("Flappy Bird")
    
    running = True
    font = pygame.font.SysFont(None, 128)
    play_font = pygame.font.SysFont(None, 64)
    sub_font = pygame.font.SysFont(None, 32)
    color = (255, 255, 255)
    color_two = (255, 255, 255)
    quit_color = (255, 255, 255)
    source_color = (255, 255, 255)
    actual_source_color = (0, 0, 0)
    trolled = False
    image = pygame.image.load("player.png")
    image_size = (70, 50)
    flappy = pygame.transform.scale(image, image_size)
    image_rect = flappy.get_rect()
    image_rect.x = width//2-43
    image_rect.y = 650

    while running:
        for event in pygame.event.get():
            text = font.render("Flappy Bird", True, color_two)
            text_rect = text.get_rect()
            text_rect.x = (width/2)-250
            text_rect.y = 60

            sub = sub_font.render("Made by Aram 9C (This took me way too long I wanna die)", True, (255, 255, 255))
            sub_rect = sub.get_rect()
            sub_rect.x = (width/2)-300
            sub_rect.y = 175
            
            last = sub_font.render(f"Last Score: {last_score}, Time survived: {time_taken} (seconds)", True, (255, 0, 0))
            last_rect = last.get_rect()
            last_rect.x = (width/2)-300
            last_rect.y = 200

            play = play_font.render("Play", True, color)
            play_rect = play.get_rect()
            play_rect.x = (width/2)-60
            play_rect.y = 250

            quit_button = play_font.render("Quit", True, quit_color)
            quit_rect = quit_button.get_rect()
            quit_rect.x = (width/2)-60
            quit_rect.y = 325

            source_button = play_font.render("Source Code", True, source_color)
            source_rect = source_button.get_rect()
            source_rect.x = (width/2)-145
            source_rect.y = 400

            actual_source_button = play_font.render("ACTUAL Source Code", True, actual_source_color)
            actual_source_rect = actual_source_button.get_rect()
            actual_source_rect.x = (width/2)-240
            actual_source_rect.y = 475

            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.draw.rect(scrn, (255, 255, 255), pygame.Rect(mouse[0], mouse[1], 20, 20))
            hover = pygame.Rect.colliderect(mouse_rect, play_rect)
            easter_egg = pygame.Rect.colliderect(mouse_rect, text_rect)
            quit_hover = pygame.Rect.colliderect(mouse_rect, quit_rect)
            source_hover = pygame.Rect.colliderect(mouse_rect, source_rect)
            actual_source_hover = pygame.Rect.colliderect(mouse_rect, actual_source_rect)
            
            if hover:
                color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    return main()
                    running = False
            else:
                color = (255, 255, 255)
                    

            if easter_egg:
                color_two = (200, 200, 200)
                if event.type == pygame.MOUSEBUTTONUP:
                    return main_inverted()
                    running = False
            else:
                color_two = (255, 255, 255)
            
            if event.type == pygame.QUIT:
                running = False
                
            if quit_hover:
                quit_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    running = False
            else:
                quit_color = (255, 255, 255)
                
            if source_hover:
                source_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    actual_source_color = (255, 255, 255)
                    trolled = True
            else:
                source_color = (255, 255, 255)

            if actual_source_hover:
                actual_source_color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            elif not trolled:
                actual_source_color = (0, 0, 0)
            else:
                actual_source_color = (255, 255, 255)

        scrn.fill((0, 0, 0))
        scrn.blit(text, text_rect)
        scrn.blit(sub, sub_rect)
        scrn.blit(play, play_rect)
        scrn.blit(last, last_rect)
        scrn.blit(quit_button, quit_rect)
        scrn.blit(source_button, source_rect)
        scrn.blit(actual_source_button, actual_source_rect)
        scrn.blit(flappy, image_rect)
        pygame.display.flip()
        

def main():
    width = 1200
    height = 720
    
    scrn = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption("Flappy Bird")
    
    running = True

    global score
    global enemy_velocity

    score = 0
    enemy_velocity = 5
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("player.png")
            self.image_size = (70, 50)
            self.flappy = pygame.transform.scale(self.image, self.image_size)
            self.rect = self.flappy.get_rect() 
            self.rect.x = 100 
            self.rect.y = 100 
            self.velocity = 0
            self.gravity_force = 0.5
            self.jump_force = -7
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
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()
    
        text = font.render(f'Score: {score}', True, (255, 255, 255), None)
        textRect = text.get_rect()
        textRect.x = 20
        textRect.y = 20
        player.gravity()
        scrn.fill((0,0,0))
        scrn.blit(text, textRect)
        scrn.blit(player.flappy, player.rect)
    
        for enemy in enemies:
            enemy.move()
            enemy.draw()
            enemy.accel()
            enemy.velocity = enemy_velocity
            collide = pygame.Rect.colliderect(player.rect, enemy.rect_bottom) or pygame.Rect.colliderect(player.rect, enemy.rect_top)
            if collide:
                return main_menu(score, time.time()-start)
                running = False
    
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            x = width
            enemies.append(Enemy((255, 0, 0), x))
            spawn_timer = 0
    
        enemies = [enemy for enemy in enemies if enemy.x > -enemy.width]
    
    
        pygame.display.flip()
        clock.tick(60)

def main_inverted():
    width = 1200
    height = 720
    
    scrn = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption("Flappy Bird")
    
    running = True

    global score
    global enemy_velocity

    score = 0
    enemy_velocity = 5
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("player.png")
            self.image_size = (70, 50)
            self.flappy = pygame.transform.scale(self.image, self.image_size)
            self.invert = pygame.transform.flip(self.flappy, False, True)
            self.rect = self.invert.get_rect() 
            self.rect.x = 100
            self.rect.y = height-100
            self.velocity = 0
            self.gravity_force = -0.5
            self.jump_force = 7
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
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()
    
        text = font.render(f'Score: {score}', True, (0, 0, 0), None)
        textRect = text.get_rect()
        textRect.x = 20
        textRect.y = 20
        other_text = font.render("You found an easter egg! Inverted mode", True, (0, 0, 0), None)
        other_textRect = other_text.get_rect()
        other_textRect.x = width//2
        other_textRect.y = 20
        player.gravity()
        scrn.fill((255, 255, 255))
        scrn.blit(text, textRect)
        scrn.blit(other_text, other_textRect)
        scrn.blit(player.invert, player.rect)
    
        for enemy in enemies:
            enemy.move()
            enemy.draw()
            enemy.accel()
            enemy.velocity = enemy_velocity
            collide = pygame.Rect.colliderect(player.rect, enemy.rect_bottom) or pygame.Rect.colliderect(player.rect, enemy.rect_top)
            if collide:
                return main_menu(score, time.time()-start)
                running = False
    
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            x = width
            enemies.append(Enemy((0, 0, 255), x))
            spawn_timer = 0
    
        enemies = [enemy for enemy in enemies if enemy.x > -enemy.width]
    
    
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu(None, None)

pygame.quit()
