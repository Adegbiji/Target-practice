import pygame
import random
import json
import sys

pygame.init()

game_window_size = (600, 400)
game_icon = pygame.image.load(r'game assets/imgs/target.png')
game_icon = pygame.transform.scale(game_icon, (32, 32))
game_icon.set_colorkey((0,0,0))
window = pygame.display.set_mode(game_window_size)
pygame.display.set_caption("Target practice")
pygame.display.set_icon(game_icon)
game_clock = pygame.time.Clock()
FPS = 60
game_state = 0 #0-menu, 1-game, 2-pause
targets = []
num_of_targets = random.randint(60, 70)
num_of_times_target_clicked = 0
game_timer = 0
load_timer = 0
json_file_path = r'game assets/other/data.json'
font_path = r'game assets/other/fonts/LovelyMadness.ttf'
game_background = pygame.image.load(r'game assets/imgs/background.png')
game_background = pygame.transform.scale(game_background, game_window_size)

def read_high_score():
  with open(json_file_path) as data_file:
    all_data = json.load(data_file)
    high_score = all_data['player_score']
    
    return high_score
    
def save_high_score(num_of_times_target_clicked):
  if num_of_times_target_clicked > read_high_score():
    data = {"player_score":num_of_times_target_clicked}
    with open(json_file_path, 'w') as json_file:
      json.dump(data, json_file, indent = 4, sort_keys = True)
      
def draw_text(size, anti_aliased, text, position):
  font = pygame.font.Font(font_path, size)
  text_surface = font.render(text, anti_aliased, (209, 0, 0))
  window.blit(text_surface, position)

class Target():
  def __init__(self, position):
    self.size = [55, 55]
    self.sprite = pygame.image.load(r'game assets/imgs/target.png')
    self.sprite = pygame.transform.scale(self.sprite, self.size)
    self.surf = pygame.Surface([55, 55])
    self.surf.set_colorkey((0, 0, 0))
    self.surf.blit(self.sprite, (0,0))
    self.rect = self.surf.get_rect(x=position[0], y=position[1])
    self.shot_sound_effect = pygame.mixer.Sound(r'game assets/audio/gunshot sound effect.mp3')
    
  def draw(self):
    window.blit(self.surf, self.rect)
    
  def update(self):
    global num_of_times_target_clicked
    
    mx, my = pygame.mouse.get_pos()
    
    if self.rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
      num_of_times_target_clicked += 1
      self.shot_sound_effect.play()
      self.rect.x = random.randint(0, 550)
      self.rect.y = random.randint(0, 330)
      
for x in range(num_of_targets):
  targets.insert(x, Target([random.randint(0, 550), random.randint(0, 330)]))
  
while game_state == 0:
  #reseting----play again
  num_of_times_target_clicked = 0
  
  window.blit(game_background, (0, 0))
  draw_text(45, True, "TARGET PRACTICE", [60,100])
  draw_text(30, True, f"HIGH SCORE: {read_high_score()}", [140,200])
  draw_text(25, True, f"PRESS 'SPACE' TO PLAY", [110, 280])
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_state = 1
      
  pygame.display.update()
  game_clock.tick(FPS)
  
  while game_state == 1:
    window.blit(game_background, (0,0))
    draw_text(25, True, f'{num_of_times_target_clicked}', [540, 0])
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          game_state = 2
    
    #target group
    for target in targets:
      target.draw()
      target.update()
        
    #game timer
    time_limit = 1500
    game_timer += 10
    draw_text(25, True, f"{time_limit - game_timer}", [0,0])
    if game_timer > time_limit:
      save_high_score(num_of_times_target_clicked)
      game_timer = 0
      game_state = 0

    pygame.display.update()
    game_clock.tick(FPS)

    while game_state == 2:
      window.blit(game_background, (0,0))
      draw_text(45, True, "GAME PAUSED", [100,150])
      draw_text(25, True, "PRESS 'ESC' TO UNPAUSE.", [95, 240])

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            game_state = 1

      pygame.display.update()
      game_clock.tick(FPS)