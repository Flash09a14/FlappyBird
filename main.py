
import pygame
import time
import random
import webbrowser

class Game:
    def __init__(self, width, height, player_start_y, gravity_force, jump_force, terminal_velocity, player_image_path, enemy_color):
        self.width = width
        self.height = height
        self.player_start_y = player_start_y
        self.gravity_force = gravity_force
        self.jump_force = jump_force
        self.terminal_velocity = terminal_velocity
        self.player_image_path = player_image_path
        self.enemy_color = enemy_color
        self.score = 0
        self.enemy_velocity = 5

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()

    def main_menu(self, last_score, time_taken):
        # Menu code here...

    def game_loop(self):
        class Player(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.image = pygame.image.load(self.player_image_path)
                self.rect = self.image.get_rect() 
                self.rect.x = 100 
                self.rect.y = self.player_start_y
                self.velocity = 0
    
            def gravity(self):
                self.velocity += self.gravity_force
                self.rect.y += self.velocity
                if self.velocity > self.terminal_velocity:
                    self.velocity = self.terminal_velocity
    
            def jump(self):
                self.velocity = self.jump_force
    
        class Enemy(pygame.sprite.Sprite):
            def __init__(self, x):
                self.x = x
                self.width = 50
                self.gap = 300
                self.height_bottom = random.randint(100, self.height - self.gap)
                self.y_bottom = self.height - self.height_bottom
                self.height_top = self.height - self.gap - self.height_bottom
                self.y_top = 0
                self.rect_bottom = pygame.Rect(self.x, self.y_bottom, self.width, self.height_bottom)
                self.rect_top = pygame.Rect(self.x, self.y_top, self.width, self.height_top)
                self.velocity = self.enemy_velocity
                self.score_counted = False
    
            def move(self):
                self.x -= self.velocity
                self.rect_bottom.x = self.x
                self.rect_top.x = self.x
    
            def draw(self):
                pygame.draw.rect(self.screen, self.enemy_color, self.rect_bottom)
                pygame.draw.rect(self.screen, self.enemy_color, self.rect_top)
                
            def accel(self):
                if self.x < 0 and not self.score_counted:
                    self.score += 1
                    self.enemy_velocity += 0.01
                    self.score_counted = True
    
        font = pygame.font.SysFont(None, 32)
        player = Player()
        enemies = []
        spawn_timer = 0
        spawn_delay = 120
        start = time.time()
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.jump()
    
            text = font.render(f'Score: {self.score}', True, (255, 255, 255), None)
            textRect = text.get_rect()
            textRect.x = 20
            textRect.y = 20
            player.gravity()
            self.screen.fill((0,0,0))
            self.screen.blit(text, textRect)
            self.screen.blit(player.image, player.rect)
    
            for enemy in enemies:
                enemy.move()
                enemy.draw()
                enemy.accel()
                enemy.velocity = self.enemy_velocity
                collide = pygame.Rect.colliderect(player.rect, enemy.rect_bottom) or pygame.Rect.colliderect(player.rect, enemy.rect_top)
                if collide:
                    self.main_menu(self.score, time.time()-start)
                    running = False
    
            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                x = self.width
                enemies.append(Enemy(x))
                spawn_timer = 0
    
            enemies = [enemy for enemy in enemies if enemy.x > -enemy.width]
    
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game(1200, 720, 100, 0.5, -7, 50, "player.png", (255, 0, 0))
    game.main_menu(None, None)
    pygame.quit()
