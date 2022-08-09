import json
import random

with open('common.txt') as f:
    content = f.read()


words = [word.upper() for word in content.split("\n") if len(word) >= 3]


size = 30, 30
words_len = 20
chosen_words = []

directions = ["HOR", "VERT", "DIAG-LEFT-RIGHT", "DIAG-RIGHT-LEFT"]#, "DIAG-LEFT-RIGHT", "DIAG-RIGHT-LEFT"]

def make_grid():
    grid = [[" " for _ in range(size[0])] for _ in range(size[1])]
    for _ in range(words_len):
        
        chose_word = False
        while not chose_word:
            word = random.choice(words)
            if (len(word) < size[0] or len(word) < size[1]) and not word in chosen_words:
                chosen_words.append(word)            
                chose_word = True

    for word in chosen_words:
        
        placed = False
        while not placed:

            direction = random.choice(directions)
            if direction == "HOR":
                start_x = random.randrange(0, size[0] - len(word))
                start_y = random.randrange(0, size[1])
                step_x = 1
                step_y = 0

            elif direction == "VERT":
                start_x = random.randrange(0, size[1])
                start_y = random.randrange(0, size[0] - len(word))
                step_x = 0
                step_y = 1

            elif direction == "DIAG-LEFT-RIGHT":
                start_x = random.randrange(0, size[0] - len(word))
                start_y = random.randrange(0, size[1] - len(word))
                step_x = 1
                step_y = 1

            elif direction == "DIAG-RIGHT-LEFT":
                start_x = random.randrange(len(word), size[0])
                start_y = random.randrange(0, size[1] - len(word))
                step_x = -1
                step_y = 1

            pointer = [start_x, start_y]
            letter_positions = []
            must_continue = False
            for i, letter in enumerate(word):
                if grid[pointer[0]][pointer[1]] not in [" ", word[i]]:
                    must_continue = True
                    break

                letter_positions.append(pointer)
                pointer = [pointer[0] + step_x, pointer[1] + step_y]
                    
            else:
                for letter, pos in list(zip(word, letter_positions)):
                    grid[pos[0]][pos[1]] = letter
                placed = True

            if must_continue:
                continue

    return grid

def fill_grid(grid):
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for l, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == " ":
                grid[l][c] = random.choice(letters)
    
    return grid



def print_board(board):
    for line in board:
        print(line)
    
    print('\n\n\n', chosen_words)


def make_json(grid, words):
    with open('wordsearch.json', 'w') as f:
        f.write(json.dumps({"wordsearch": [grid, words]}))


def make_png(grid, words):
    import pygame
    pygame.init()
    w, h = (50 * size[0], 50 * size[1])
    board = pygame.Surface((w, h))

    board.fill((255, 255, 255))

    font = pygame.font.SysFont('ubuntu mono', 50)
    words_font = pygame.font.SysFont('ubuntu mono', 25)
    letters = {letter: font.render(letter, True, (0, 0, 0)) for letter in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ ')}

    lines = [words[0]]
    rendered_lines = []
    curr_size = 0
    for word in words[1:]:
        if curr_size + words_font.size(word)[0] < w:
            lines[-1] += ', ' + word
            curr_size = words_font.size(lines[-1])[0]
        else:
            lines.append(word)
            curr_size = words_font.size(lines[-1])[0]

    for line in lines:
        rendered_lines.append(words_font.render(line, True, (0, 0, 0)))

    vert_off = 5
    words_surf = pygame.Surface((w, len(lines) * words_font.get_height() + len(lines) * vert_off))
    words_surf.fill((255, 255, 255))

    wi_off = w/10
    he_off = h/10

    screen = pygame.Surface((w + wi_off, wi_off + h + he_off * 1 + words_surf.get_height()))
    screen.fill((255, 255, 255))
        
    for l, line in enumerate(grid):
        for c, char in enumerate(line):
            board.blit(letters[char], (w / size[0] * c, h / size[1] * l))

    for l, line in enumerate(rendered_lines):
        words_surf.blit(line, (0, words_surf.get_height() / len(lines) * l))

    screen.blit(board, (wi_off/2, wi_off/2))
    screen.blit(words_surf, (wi_off/2, h + he_off + wi_off/2))
    
    pygame.image.save(screen, 'wordsearch.png')
    
grid = make_grid()
grid = fill_grid(grid)
print_board(grid)
make_json(grid, chosen_words)