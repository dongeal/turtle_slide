import pygame
import random
import time
from sprite import *
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ''
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.tiles =[]
        self.high_score_easy = float(self.get_high_score()[0])
        self.high_score_medium = float(self.get_high_score()[1])
        self.high_score_hard = float(self.get_high_score()[2])

    def get_high_score(self):
        with open('high_score.txt','r') as file :
            scores = file.read().splitlines()
        return scores
  
    def save_score(self):
        with open('high_score.txt','w') as file :
            file.write(str("%.3f\n" % self.high_score_easy))
            file.write(str("%.3f\n" % self.high_score_medium))
            file.write(str("%.3f\n" % self.high_score_hard))

    def create_game(self):
        grid =[[x + y *self.game_size for x in range(1, self.game_size + 1)] \
               for y in range(self.game_size)]
        grid[-1][-1] = 0
        return grid  # self.grid = [[1,2,3],[4,5,6],[7,8,0]]
    
    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == 'empty':
                    if tile.right():
                        possible_moves.append('right')
                    if tile.left():
                        possible_moves.append('left')
                    if tile.up():
                        possible_moves.append('up')
                    if tile.down():
                        possible_moves.append('down') 
                    break  
            if len(possible_moves) > 0 :
                break
        
        if self.previous_choice == 'left':
            possible_moves.remove('right') if 'right' in possible_moves else possible_moves

        elif self.previous_choice == 'right':
            possible_moves.remove('left') if 'left' in possible_moves else possible_moves
    
        elif self.previous_choice == 'up':
            possible_moves.remove('down') if 'down' in possible_moves else possible_moves
        
        elif self.previous_choice == 'down':
            possible_moves.remove('up') if 'up' in possible_moves else possible_moves
  
        choice = random.choice(possible_moves)
        self.previous_choice = choice

        if choice == 'right':    
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = \
                                self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

        elif choice == 'left':
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = \
                                self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

        elif choice == 'up':
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = \
                                self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

        elif choice == 'down':                         
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = \
                                self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            
    
    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile !=0:          # sprite (game, x , y , text)
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))
 
    def new(self):
        
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list =[]
        self.buttons_list.append(Button(775, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(775, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(680, 240, 120, 50, "Easy", WHITE, BLACK))
        self.buttons_list.append(Button(820, 240, 120, 50, "Medium", WHITE, BLACK))
        self.buttons_list.append(Button(960, 240, 120, 50, "Hard", WHITE, BLACK))

        self.draw_tiles()
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
           
    def update(self):
        self.all_sprites.update() 

        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.game_choice == 'EASY':
                    if self.high_score_easy >0 :
                        self.high_score_easy = self.elapsed_time if self.elapsed_time < self.high_score_easy else self.high_score_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif self.game_choice == 'MEDIUM':
                    if self.high_score_medium >0 :
                        self.high_score_medium = self.elapsed_time if self.elapsed_time < self.high_score_medium else self.high_score_medium
                    else:
                        self.high_score_medium = self.elapsed_time
                elif self.game_choice == 'HARD':
                    if self.high_score_hard >0 :
                        self.high_score_hard = self.elapsed_time if self.elapsed_time < self.high_score_hard else self.high_score_hard
                    else:
                        self.high_score_hard = self.elapsed_time
                
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer



        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 100:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

    def draw_grid(self):
        for row in range(-1, self.game_size * TILESIZE, TILESIZE): # 세로 줄
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, self.game_size * TILESIZE))    
        for col in range(-1, self.game_size * TILESIZE, TILESIZE): # 가로 줄
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (self.game_size * TILESIZE, col))  

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        if self.game_choice == 'EASY':
            UIElement(840,320, "Easy").draw(self.screen)
            UIElement(710, 380, "High Score - %.3f" % (self.high_score_easy if self.high_score_easy >0 else 0)).draw(self.screen)
        elif self.game_choice == 'MEDIUM':
            UIElement(840,320, "Medium").draw(self.screen)
            UIElement(710, 380, "High Score - %.3f" % (self.high_score_medium if self.high_score_medium >0 else 0)).draw(self.screen)
        elif self.game_choice == 'HARD':
            UIElement(840,320, "Hard").draw(self.screen)
            UIElement(710, 380, "High Score - %.3f" % (self.high_score_hard if self.high_score_hard >0 else 0)).draw(self.screen)


        for button in self.buttons_list:
            button.draw(self.screen)

        UIElement(825, 35, "%.3f" % self.elapsed_time).draw(self.screen)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = \
                                self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
                            
                            elif tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = \
                                self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            elif tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = \
                                self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            
                            elif tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = \
                                self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            
                            self.draw_tiles()

                for button in self.buttons_list:
                  if button.click(mouse_x, mouse_y):
                      if button.text == "Easy":
                          self.game_choice = 'EASY'
                          self.game_size = 3
                          self.new()
                      elif button.text == "Medium":
                          self.game_choice = 'MEDIUM'
                          self.game_size = 4
                          self.new()
                      elif button.text == "Hard":
                          self.game_choice = 'HARD'
                          self.game_size = 5
                          self.new()
                      elif button.text == "Shuffle":
                          self.shuffle_time = 0
                          self.start_shuffle = True
                      elif button.text == "Reset":
                          self.new()
                          
    def show_start_screen(self):
        self.game_choice = 'EASY'
        self.game_size = 3

   
game = Game()
while True:
    game.show_start_screen()
    game.new()
    game.run()
    