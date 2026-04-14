import pygame, sys, random, math
from collections import deque

W, H = 1280, 720
DARK = (0, 0, 0)
BLUE_WALL = (30, 50, 200)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
RED = (220, 30, 30)
PINK = (255, 130, 200)
CYAN_C = (30, 220, 220)
ORANGE = (255, 160, 30)
SCARED = (30, 30, 200)
DOT_C = (255, 200, 150)

MAZE_W, MAZE_H = 21, 21
CELL = 32
OX = (W - MAZE_W * CELL) // 2
OY = 60

# 0=wall 1=dot 2=empty 3=power 4=ghost_house
BASE_MAZE = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,3,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,3,0],
    [0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
    [0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0],
    [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
    [0,0,0,0,1,0,0,0,2,0,0,0,2,0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,2,2,2,2,2,2,2,2,2,0,1,0,0,0,0],
    [0,0,0,0,1,0,2,0,4,4,4,4,4,0,2,0,1,0,0,0,0],
    [1,1,1,1,1,1,1,0,4,4,4,4,4,0,1,1,1,1,1,1,1],
    [0,0,0,0,1,0,2,0,2,2,2,2,2,0,2,0,1,0,0,0,0],
    [0,0,0,0,1,0,2,2,2,2,2,2,2,2,2,0,1,0,0,0,0],
    [0,0,0,0,1,0,2,0,0,0,0,0,0,0,2,0,1,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
    [0,3,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,3,0],
    [0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0],
    [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

def run_pacman(screen, clock, player_name):
    pygame.display.set_caption("Pac-Man")
    font = pygame.font.SysFont("consolas", 22, bold=True)
    font_big = pygame.font.SysFont("consolas", 48, bold=True)

    def reset_maze():
        return [row[:] for row in BASE_MAZE]

    def count_dots(maze):
        return sum(1 for r in maze for c in r if c in (1, 3))

    def bfs(maze, start, end):
        q = deque([(start, [])])
        visited = {start}
        while q:
            (r, c), path = q.popleft()
            if (r, c) == end:
                return path
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < MAZE_H and 0 <= nc < MAZE_W and (nr, nc) not in visited and maze[nr][nc] != 0:
                    visited.add((nr, nc))
                    q.append(((nr, nc), path + [(nr, nc)]))
        return []

    score, lives, level = 0, 3, 1
    maze = reset_maze()
    total_dots = count_dots(maze)

    # Pac-Man position (row, col)
    px, py = 10, 10  # grid pos
    pdx, pdy = 0, 0
    next_dx, next_dy = 0, 0
    p_anim = 0.0
    p_mouth = 0.3

    GHOST_COLORS = [RED, PINK, CYAN_C, ORANGE]
    GHOST_NAMES = ["Blinky", "Pinky", "Inky", "Clyde"]
    ghosts = [
        {'r': 9, 'c': 9+i, 'color': GHOST_COLORS[i], 'dr': 0, 'dc': 0,
         'scared': 0, 'home_r': 9+i//2, 'home_c': 9+i}
        for i in range(4)
    ]

    power_timer = 0.0
    POWER_DURATION = 8.0
    move_timer = 0.0
    MOVE_RATE = 0.18
    ghost_timer = 0.0
    GHOST_RATE = 0.22
    t = 0.0
    game_over = False
    won = False

    def can_move(maze, r, c, dr, dc):
        nr, nc = r + dr, c + dc
        if 0 <= nr < MAZE_H and 0 <= nc < MAZE_W and maze[nr][nc] != 0:
            return True
        return False

    def ghost_move(g, maze, pac_r, pac_c):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        if g['scared'] > 0:
            valid = [(dr, dc) for dr, dc in directions if can_move(maze, g['r'], g['c'], dr, dc)]
            if valid:
                g['dr'], g['dc'] = random.choice(valid)
        else:
            path = bfs(maze, (g['r'], g['c']), (pac_r, pac_c))
            if path:
                nr, nc = path[0]
                g['dr'], g['dc'] = nr - g['r'], nc - g['c']
            else:
                valid = [(dr, dc) for dr, dc in directions if can_move(maze, g['r'], g['c'], dr, dc)]
                if valid:
                    g['dr'], g['dc'] = random.choice(valid)
        nr, nc = g['r'] + g['dr'], g['c'] + g['dc']
        if 0 <= nr < MAZE_H and 0 <= nc < MAZE_W and maze[nr][nc] != 0:
            g['r'], g['c'] = nr, nc

    def draw_maze(surf, maze):
        for r in range(MAZE_H):
            for c in range(MAZE_W):
                x, y = OX + c * CELL, OY + r * CELL
                cell = maze[r][c]
                if cell == 0:
                    pygame.draw.rect(surf, BLUE_WALL, (x, y, CELL, CELL))
                    pygame.draw.rect(surf, (50, 80, 255), (x+1, y+1, CELL-2, CELL-2), 1)
                elif cell == 1:
                    pygame.draw.circle(surf, DOT_C, (x + CELL//2, y + CELL//2), 3)
                elif cell == 3:
                    r2 = int(5 + 2 * math.sin(t * 5))
                    pygame.draw.circle(surf, YELLOW, (x + CELL//2, y + CELL//2), r2)

    def draw_pacman(surf, r, c, mouth, dx, dy):
        x = OX + c * CELL + CELL // 2
        y = OY + r * CELL + CELL // 2
        rad = CELL // 2 - 3
        angle = math.degrees(math.atan2(-dy, dx)) if (dx or dy) else 0
        mouth_angle = mouth * 45
        start_a = math.radians(angle + mouth_angle)
        end_a = math.radians(angle - mouth_angle)
        pts = [(x, y)]
        steps = 30
        for i in range(steps + 1):
            a = start_a + (end_a - start_a) * i / steps
            pts.append((x + rad * math.cos(a), y - rad * math.sin(a)))
        if len(pts) > 2:
            pygame.draw.polygon(surf, YELLOW, pts)

    def draw_ghost(surf, g):
        x = OX + g['c'] * CELL + CELL // 2
        y = OY + g['r'] * CELL + CELL // 2
        rad = CELL // 2 - 2
        col = SCARED if g['scared'] > 0 else g['color']
        pygame.draw.circle(surf, col, (x, y - 2), rad)
        pygame.draw.rect(surf, col, (x - rad, y - 2, rad * 2, rad))
        # Eyes
        if g['scared'] <= 0:
            pygame.draw.circle(surf, WHITE, (x - 4, y - 4), 4)
            pygame.draw.circle(surf, WHITE, (x + 4, y - 4), 4)
            pygame.draw.circle(surf, (0, 0, 150), (x - 3, y - 4), 2)
            pygame.draw.circle(surf, (0, 0, 150), (x + 5, y - 4), 2)

    def show_msg(text, color, sub=""):
        screen.fill(DARK)
        s = font_big.render(text, True, color)
        screen.blit(s, (W//2 - s.get_width()//2, H//2 - 50))
        if sub:
            s2 = font.render(sub, True, WHITE)
            screen.blit(s2, (W//2 - s2.get_width()//2, H//2 + 20))
        pygame.display.flip()
        pygame.time.wait(2000)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt
        move_timer += dt
        ghost_timer += dt
        p_anim += dt * 4
        p_mouth = abs(math.sin(p_anim))
        if power_timer > 0:
            power_timer -= dt
            if power_timer < 0:
                power_timer = 0
                for g in ghosts:
                    g['scared'] = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score
                k = event.key
                if k == pygame.K_LEFT:  next_dx, next_dy = 0, -1
                elif k == pygame.K_RIGHT: next_dx, next_dy = 0, 1
                elif k == pygame.K_UP:   next_dx, next_dy = -1, 0
                elif k == pygame.K_DOWN: next_dx, next_dy = 1, 0

        if game_over or won:
            screen.fill(DARK)
            draw_maze(screen, maze)
            if won:
                show_msg(f"YOU WIN! Score: {score}", YELLOW)
            else:
                show_msg("GAME OVER", RED, f"Score: {score}")
            return score

        # Move pacman
        if move_timer >= MOVE_RATE:
            move_timer = 0
            # Try next direction first
            if can_move(maze, px, py, next_dx, next_dy):
                pdx, pdy = next_dx, next_dy
            if can_move(maze, px, py, pdx, pdy):
                px += pdx
                py += pdy
                # Tunnel wrap
                py = py % MAZE_W
                cell = maze[px][py]
                if cell == 1:
                    maze[px][py] = 2
                    score += 10
                elif cell == 3:
                    maze[px][py] = 2
                    score += 50
                    power_timer = POWER_DURATION
                    for g in ghosts:
                        g['scared'] = POWER_DURATION

        # Move ghosts
        if ghost_timer >= GHOST_RATE:
            ghost_timer = 0
            for g in ghosts:
                ghost_move(g, maze, px, py)
                if g['scared'] > 0:
                    g['scared'] -= GHOST_RATE

        # Ghost-pacman collision
        for g in ghosts:
            if g['r'] == px and g['c'] == py:
                if g['scared'] > 0:
                    score += 200
                    g['r'], g['c'] = g['home_r'], g['home_c']
                    g['scared'] = 0
                else:
                    lives -= 1
                    px, py = 10, 10
                    pdx, pdy = 0, 0
                    if lives <= 0:
                        game_over = True

        # Win condition
        if count_dots(maze) == 0:
            score += level * 1000
            level += 1
            maze = reset_maze()
            px, py = 10, 10
            for i, g in enumerate(ghosts):
                g['r'], g['c'] = 9, 9 + i
                g['scared'] = 0
            show_msg(f"LEVEL {level}!", CYAN_C)

        # Draw
        screen.fill(DARK)
        draw_maze(screen, maze)
        draw_pacman(screen, px, py, p_mouth, pdy, pdx)
        for g in ghosts:
            draw_ghost(screen, g)

        # HUD
        hud = font.render(f"SCORE: {score}  LIVES: {'● ' * lives}  LEVEL: {level}", True, WHITE)
        screen.blit(hud, (10, 10))
        if power_timer > 0:
            pt = font.render(f"POWER! {power_timer:.1f}s", True, CYAN_C)
            screen.blit(pt, (W - pt.get_width() - 10, 10))

        pygame.display.flip()

    return score
