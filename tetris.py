import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
BLACK,WHITE,RED, GREEN, BLUE,YELLOW = (0,0,0),(255,255,255), (255, 0, 0), (0, 255, 0), (0, 0, 255),(255,255,0)
INITAL_SPEED = 1000
# Shapes
SHAPES = [
    [[1, 1, 1, 1]],             # I
    [[1, 1], [1, 1]],           # O
    [[0, 1, 0], [1, 1, 1]],     # T
    [[1, 1, 0], [0, 1, 1]],     # Z
    [[0, 1, 1], [1, 1, 0]],     # S
    [[1, 0, 0], [1, 1, 1]],     # L
    [[0, 0, 1], [1, 1, 1]]      # J
]

# Global variables
global speed
global score
global row_count
speed = 0
score = 0
row_count = 0

class Tetromino:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.shape = random.choice(SHAPES)
        self.color = random.choice([RED, GREEN, BLUE,YELLOW])
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid_row = y // GRID_SIZE
                    grid_col = x // GRID_SIZE
                    if grid[grid_row + i][grid_col + j]:  # checking collision with another piece
                        pygame.event.post(pygame.event.Event(game_over))

    def rotate(self, grid):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]

        # check for collisions when rotating
        for i, row in enumerate(rotated_shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = (self.x // GRID_SIZE) + j
                    new_y = (self.y // GRID_SIZE) + i

                    
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x]):
                        return

        
        self.shape = rotated_shape

    def go_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if current_piece.can_move(0, 1, grid):
                current_piece.y += GRID_SIZE
        

    def has_reached_bottom(self, grid):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_y = self.y // GRID_SIZE + i + 1
                    new_x = self.x // GRID_SIZE + j

                    if new_y >= ROWS or grid[new_y][new_x]:
                        return True
        return False
    

    def can_move(self, dx, dy, grid):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = (self.x // GRID_SIZE) + j + dx
                    new_y = (self.y // GRID_SIZE) + i + dy

                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and grid[new_y][new_x]:  # Collision with another piece
                        return False
        return True
    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, 
                                     (self.x + j * GRID_SIZE, self.y + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def update_score(screen):
    font_size = 20
    myfont = pygame.font.SysFont("monospace", font_size)

    # render text
    score_txt = myfont.render("Score: "+str(score) ,1, WHITE)
    speed_txt = myfont.render("Speed: "+str(speed) ,1, WHITE)
    row_count_txt = myfont.render("Rows: "+ str(row_count),1,WHITE)

    screen.blit(score_txt, (WIDTH+5, 20))
    screen.blit(speed_txt, (WIDTH+5, 20+font_size))
    screen.blit(row_count_txt, (WIDTH+5, 20+font_size * 2))

def clear_rows(grid):
    global speed
    global score
    global row_count
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    if len(full_rows) > 0:
        row_count += len(full_rows)
        speed = min(10,speed+1)
        velocity = max(100, int(INITAL_SPEED - (speed*90)))
        pygame.time.set_timer(drop, velocity)
        score = score + int(100000*len(full_rows) / velocity)
        
    for row in full_rows:
        del grid[row]  
        grid.insert(0, [0] * COLUMNS)  # Add an empty row at the top to compensate for deleted row

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
    clock = pygame.time.Clock()
    drop = pygame.USEREVENT + 1
    game_over = pygame.USEREVENT +2
    
    pygame.time.set_timer(drop, INITAL_SPEED)
    running = True
    grid = [[0] * COLUMNS for _ in range(ROWS)]
    current_piece = Tetromino(WIDTH // 2 - GRID_SIZE, 0)

    while running:       
        current_piece.go_down()
        screen.fill(BLACK)
        score_board = pygame.Rect(WIDTH,0,200,HEIGHT)
        pygame.draw.rect(screen,(50,50,50),score_board)
        update_score(screen)
        
        for event in pygame.event.get():
            
            # User movement for current piece except down key which is in go_down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_piece.rotate(grid)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if current_piece.can_move(-1, 0, grid):
                        current_piece.x -= GRID_SIZE
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if current_piece.can_move(1, 0, grid):
                        current_piece.x += GRID_SIZE
            if event.type == drop:
                if current_piece.has_reached_bottom(grid):
                    for i, row in enumerate(current_piece.shape):
                        for j, cell in enumerate(row):
                            if cell:
                                grid[(current_piece.y // GRID_SIZE) + i][(current_piece.x // GRID_SIZE) + j] = current_piece.color
                    clear_rows(grid)
                    current_piece = Tetromino(WIDTH // 2 - GRID_SIZE, 0)
                else:
                    current_piece.y += GRID_SIZE
            
            # Exit conditions
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == game_over:
                # Will replace this with game over screen
                running = False

        # Adding existing pieces to the draw call
        for i in range(ROWS):
            for j in range(COLUMNS):
                if grid[i][j]:
                    pygame.draw.rect(screen, grid[i][j], (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Drawing
        current_piece.draw(screen)
        pygame.display.flip()
        clock.tick(100)

    pygame.quit()
