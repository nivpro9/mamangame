import pygame, sys, random, math

W, H = 1280, 720
DARK = (5, 5, 20)
RED = (220, 50, 50)
BLUE = (60, 100, 220)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
BROWN = (140, 80, 30)
GRAY = (120, 120, 120)
ORANGE = (230, 130, 40)
PINK = (255, 160, 160)
GREEN = (60, 200, 60)

# Platform layout: (x, y, width)
BASE_PLATFORMS = [
    (100, 650, 1080),   # ground
    (80,  540, 500),    # level 1 left
    (700, 540, 500),    # level 1 right
    (80,  430, 500),    # level 2 left
    (700, 430, 500),    # level 2 right
    (80,  320, 500),    # level 3 left
    (700, 320, 500),    # level 3 right
    (300, 210, 680),    # level 4
    (450, 100, 380),    # top (DK level)
]

# Ladder positions: (x, top_y, bottom_y)
BASE_LADDERS = [
    (200,  540, 650),
    (900,  540, 650),
    (350,  430, 540),
    (850,  430, 540),
    (200,  320, 430),
    (950,  320, 430),
    (500,  210, 320),
    (800,  210, 320),
    (550,  100, 210),
    (750,  100, 210),
]

GRAVITY = 900
JUMP_V = -520
MOVE_SPEED = 220
BARREL_SPEED_BASE = 220

def run_donkey_kong(screen, clock, player_name):
    pygame.display.set_caption("Donkey Kong")
    font = pygame.font.SysFont("consolas", 22, bold=True)
    font_big = pygame.font.SysFont("consolas", 48, bold=True)

    score = 0
    lives = 3
    level = 1
    game_over = False
    won = False

    class Mario:
        def __init__(self):
            self.x, self.y = 120.0, 590.0
            self.w, self.h = 28, 36
            self.vx, self.vy = 0.0, 0.0
            self.on_ground = False
            self.on_ladder = False
            self.anim = 0.0
            self.facing = 1
            self.hammer = 0.0

        def rect(self):
            return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

        def draw(self, surf):
            r = self.rect()
            leg = int(4 * math.sin(self.anim * 8)) if self.vx != 0 else 0
            # Body
            pygame.draw.rect(surf, BLUE, (r.x + 4, r.y + 16, 20, 16))
            # Head
            pygame.draw.rect(surf, PINK, (r.x + 6, r.y + 4, 16, 14))
            pygame.draw.rect(surf, RED, (r.x + 5, r.y, 18, 8))  # hat
            # Legs
            pygame.draw.rect(surf, BROWN, (r.x + 4, r.y + 28, 8, 8 + leg))
            pygame.draw.rect(surf, BROWN, (r.x + 16, r.y + 28, 8, 8 - leg))
            # Hammer
            if self.hammer > 0:
                hx = r.right + 2 if self.facing > 0 else r.left - 18
                pygame.draw.rect(surf, BROWN, (hx, r.y + 4, 16, 10))
                pygame.draw.rect(surf, GRAY, (hx, r.y, 16, 6))

    class DonkeyKong:
        def __init__(self):
            self.x, self.y = 500, 50
            self.anim = 0.0
            self.throw_cd = 0.0

        def draw(self, surf):
            self.anim += 0.02
            ox = int(6 * math.sin(self.anim))
            # Body
            pygame.draw.ellipse(surf, BROWN, (self.x, self.y + 20, 120, 90))
            # Head
            pygame.draw.ellipse(surf, BROWN, (self.x + 20, self.y, 80, 70))
            # Eyes
            pygame.draw.circle(surf, WHITE, (self.x + 42, self.y + 25), 8)
            pygame.draw.circle(surf, WHITE, (self.x + 78, self.y + 25), 8)
            pygame.draw.circle(surf, DARK, (self.x + 44, self.y + 27), 4)
            pygame.draw.circle(surf, DARK, (self.x + 80, self.y + 27), 4)
            # Arms
            arm_y = int(5 * math.sin(self.anim * 2))
            pygame.draw.ellipse(surf, BROWN, (self.x - 30 + ox, self.y + 40 + arm_y, 40, 24))
            pygame.draw.ellipse(surf, BROWN, (self.x + 110 - ox, self.y + 40 - arm_y, 40, 24))

    class Barrel:
        def __init__(self, x, y, vx, level):
            self.x, self.y = float(x), float(y)
            self.vx = float(vx)
            self.vy = 0.0
            self.w, self.h = 24, 20
            self.anim = 0.0
            self.on_plat = False

        def rect(self):
            return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

        def draw(self, surf):
            self.anim += 0.1
            cx = int(self.x) + self.w // 2
            cy = int(self.y) + self.h // 2
            pygame.draw.circle(surf, BROWN, (cx, cy), 12)
            angle = self.anim * 5
            for i in range(3):
                a = angle + i * math.pi * 2 / 3
                ex = cx + int(10 * math.cos(a))
                ey = cy + int(10 * math.sin(a))
                pygame.draw.line(surf, DARK, (cx, cy), (ex, ey), 3)
            pygame.draw.circle(surf, BROWN, (cx, cy), 12, 2)

    def build_platforms(lvl):
        return [pygame.Rect(x, y, w, 18) for x, y, w in BASE_PLATFORMS]

    def build_ladders(lvl):
        return [(x, top, bot) for x, top, bot in BASE_LADDERS]

    def draw_platforms(surf, platforms):
        for p in platforms:
            pygame.draw.rect(surf, GRAY, p)
            pygame.draw.rect(surf, WHITE, p, 2)

    def draw_ladders(surf, ladders):
        for x, top, bot in ladders:
            pygame.draw.rect(surf, BROWN, (x, top, 20, bot - top))
            for ry in range(top, bot, 18):
                pygame.draw.rect(surf, YELLOW, (x, ry, 20, 4))

    def draw_princess(surf):
        px, py = 590, 55
        pygame.draw.rect(surf, PINK, (px, py + 10, 24, 30))
        pygame.draw.circle(surf, PINK, (px + 12, py + 10), 12)
        pygame.draw.rect(surf, YELLOW, (px + 2, py, 20, 12))  # crown

    def show_msg(text, color, sub=""):
        screen.fill(DARK)
        s = font_big.render(text, True, color)
        screen.blit(s, (W // 2 - s.get_width() // 2, H // 2 - 50))
        if sub:
            s2 = font.render(sub, True, WHITE)
            screen.blit(s2, (W // 2 - s2.get_width() // 2, H // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(2500)

    mario = Mario()
    dk = DonkeyKong()
    platforms = build_platforms(level)
    ladders = build_ladders(level)
    barrels = []
    barrel_cd = 2.5
    hammer_pickup = pygame.Rect(900, 590, 20, 20)
    t = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt
        barrel_cd -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score
                if event.key in (pygame.K_UP, pygame.K_w) and mario.on_ladder:
                    mario.vy = -180
                if event.key in (pygame.K_DOWN, pygame.K_s) and mario.on_ladder:
                    mario.vy = 180
                if event.key in (pygame.K_SPACE, pygame.K_UP) and mario.on_ground and not mario.on_ladder:
                    mario.vy = JUMP_V

        if game_over or won:
            if won:
                show_msg(f"YOU RESCUED PAULINE!", YELLOW, f"Score: {score}")
            else:
                show_msg("GAME OVER", RED, f"Score: {score}")
            return score

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            mario.vx = -MOVE_SPEED
            mario.facing = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            mario.vx = MOVE_SPEED
            mario.facing = 1
        else:
            mario.vx = 0

        # Ladder check
        mario.on_ladder = False
        for lx, lt, lb in ladders:
            if lx <= mario.x + mario.w // 2 <= lx + 20 and lt <= mario.y + mario.h <= lb:
                mario.on_ladder = True
                break

        if not mario.on_ladder:
            mario.vy += GRAVITY * dt
        mario.vy = max(-600, min(mario.vy, 800))

        mario.x += mario.vx * dt
        mario.y += mario.vy * dt
        mario.anim += dt

        # Platform collision
        mario.on_ground = False
        mr = mario.rect()
        for p in platforms:
            if mr.colliderect(p) and mario.vy >= 0 and mr.bottom - p.top < 20:
                mario.y = p.top - mario.h
                mario.vy = 0
                mario.on_ground = True
        mario.x = max(0, min(mario.x, W - mario.w))

        # Hammer pickup
        if hammer_pickup and mario.rect().colliderect(hammer_pickup):
            mario.hammer = 5.0
            hammer_pickup = None
            score += 300

        if mario.hammer > 0:
            mario.hammer -= dt

        # Spawn barrels
        if barrel_cd <= 0:
            spd = BARREL_SPEED_BASE + level * 20
            barrels.append(Barrel(560, 120, spd * random.choice([-1, 1]), level))
            barrel_cd = max(1.0, 2.5 - level * 0.2)

        # Update barrels
        for b in barrels[:]:
            b.vy += GRAVITY * dt
            b.x += b.vx * dt
            b.y += b.vy * dt
            br = b.rect()
            b.on_plat = False
            for p in platforms:
                if br.colliderect(p) and b.vy >= 0 and br.bottom - p.top < 20:
                    b.y = p.top - b.h
                    b.vy = 0
                    b.on_plat = True
                    # Reverse at edges
                    if b.x < 80 or b.x + b.w > W - 80:
                        b.vx = -b.vx
            if b.y > H + 50:
                barrels.remove(b)
                continue
            # Barrel vs mario
            if br.colliderect(mario.rect()):
                if mario.hammer > 0:
                    barrels.remove(b)
                    score += 500
                else:
                    lives -= 1
                    barrels.clear()
                    mario.x, mario.y = 120.0, 590.0
                    mario.vx = mario.vy = 0
                    if lives <= 0:
                        game_over = True

        # Win: mario reaches princess (top)
        if mario.y < 80:
            score += level * 2000
            level += 1
            show_msg(f"LEVEL {level}!", YELLOW)
            mario.x, mario.y = 120.0, 590.0
            mario.vx = mario.vy = 0
            barrels.clear()
            barrel_cd = 2.5
            hammer_pickup = pygame.Rect(900, 590, 20, 20)

        # Draw
        screen.fill(DARK)
        draw_platforms(screen, platforms)
        draw_ladders(screen, ladders)
        draw_princess(screen)
        dk.draw(screen)
        dk.throw_cd = t  # just to animate

        for b in barrels:
            b.draw(screen)
        mario.draw(screen)

        if hammer_pickup:
            pygame.draw.rect(screen, GRAY, hammer_pickup)
            pygame.draw.rect(screen, WHITE, hammer_pickup, 2)

        # HUD
        hud = font.render(f"SCORE: {score}  LIVES: {'♥ ' * lives}  LEVEL: {level}", True, WHITE)
        screen.blit(hud, (10, 10))
        inst = font.render("Arrows: Move/Climb  SPACE/UP: Jump  ESC: Exit", True, GRAY)
        screen.blit(inst, (W // 2 - inst.get_width() // 2, H - 35))

        pygame.display.flip()

    return score
