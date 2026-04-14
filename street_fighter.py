import pygame, sys, math, random

W, H = 1280, 720
DARK = (10, 5, 20)
WHITE = (255, 255, 255)
RED = (220, 40, 40)
BLUE = (40, 80, 220)
YELLOW = (255, 220, 0)
GREEN = (40, 200, 80)
GRAY = (120, 120, 120)
ORANGE = (230, 130, 40)
PINK = (255, 160, 150)
CYAN = (0, 200, 255)
FLOOR_Y = 580

GRAVITY = 900
JUMP_V = -550

class Fighter:
    def __init__(self, x, facing, color, name, is_cpu=False):
        self.x = float(x)
        self.y = float(FLOOR_Y - 80)
        self.w, self.h = 52, 80
        self.vx, self.vy = 0.0, 0.0
        self.color = color
        self.name = name
        self.is_cpu = is_cpu
        self.facing = facing
        self.hp = 200
        self.max_hp = 200
        self.on_ground = True
        self.anim = 0.0
        self.state = "idle"  # idle, walk, jump, punch, kick, block, hurt
        self.state_timer = 0.0
        self.hit_box = None
        self.combo = 0
        self.combo_timer = 0.0
        self.cpu_cd = 0.0
        self.block = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def do_punch(self):
        if self.state not in ("punch", "kick", "hurt"):
            self.state = "punch"
            self.state_timer = 0.25
            hx = self.x + self.w if self.facing > 0 else self.x - 60
            self.hit_box = pygame.Rect(int(hx), int(self.y + 10), 60, 30)
            return True
        return False

    def do_kick(self):
        if self.state not in ("punch", "kick", "hurt"):
            self.state = "kick"
            self.state_timer = 0.3
            hx = self.x + self.w if self.facing > 0 else self.x - 70
            self.hit_box = pygame.Rect(int(hx), int(self.y + 40), 70, 35)
            return True
        return False

    def do_jump(self):
        if self.on_ground:
            self.vy = JUMP_V
            self.on_ground = False
            self.state = "jump"

    def take_hit(self, dmg, is_kick=False):
        if self.block:
            dmg = dmg // 4
        self.hp = max(0, self.hp - dmg)
        self.state = "hurt"
        self.state_timer = 0.15
        self.hit_box = None
        return dmg

    def update(self, dt, enemy):
        self.anim += dt * 3
        self.state_timer = max(0, self.state_timer - dt)
        self.combo_timer = max(0, self.combo_timer - dt)
        if self.combo_timer == 0:
            self.combo = 0

        if self.state_timer == 0 and self.state in ("punch", "kick", "hurt"):
            self.state = "idle"
            self.hit_box = None

        # CPU AI
        if self.is_cpu and self.hp > 0 and enemy.hp > 0:
            self.cpu_cd = max(0, self.cpu_cd - dt)
            if self.cpu_cd == 0:
                dx = enemy.x - self.x
                dist = abs(dx)
                self.vx = 0
                if dist > 100:
                    self.vx = -80 if dx < 0 else 80
                if dist < 120 and dist > 40:
                    r = random.random()
                    if r < 0.4:
                        self.do_punch()
                    elif r < 0.7:
                        self.do_kick()
                    elif r < 0.8:
                        self.do_jump()
                    self.block = r > 0.85
                elif dist <= 40:
                    self.vx = -self.facing * 60
                self.cpu_cd = random.uniform(0.1, 0.3)
            self.facing = -1 if enemy.x < self.x else 1

        # Physics
        if not self.on_ground:
            self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Floor
        if self.y >= FLOOR_Y - self.h:
            self.y = FLOOR_Y - self.h
            self.vy = 0
            self.on_ground = True
            if self.state == "jump":
                self.state = "idle"

        # Boundaries
        self.x = max(50, min(self.x, W - self.w - 50))

    def draw(self, surf):
        r = self.rect()
        cx = r.centerx
        bot = r.bottom
        leg = int(6 * math.sin(self.anim)) if self.state == "walk" else 0

        # Shadow
        pygame.draw.ellipse(surf, (30, 30, 50), (cx - 28, bot - 6, 56, 14))

        # Legs
        pygame.draw.rect(surf, self.color, (cx - 20, bot - 28, 16, 28 + leg))
        pygame.draw.rect(surf, self.color, (cx + 4, bot - 28, 16, 28 - leg))

        # Body
        body_col = self.color
        if self.state == "hurt":
            body_col = WHITE
        if self.block:
            body_col = CYAN
        pygame.draw.rect(surf, body_col, (cx - 22, r.top + 30, 44, 32))

        # Arms
        arm_raise = -20 if self.state == "punch" else (10 if self.state == "kick" else 0)
        pygame.draw.rect(surf, self.color, (cx - 32, r.top + 34 + arm_raise, 14, 22))
        pygame.draw.rect(surf, self.color, (cx + 18, r.top + 34 + arm_raise, 14, 22))

        # Punch fist
        if self.state == "punch":
            fx = cx + 26 if self.facing > 0 else cx - 38
            pygame.draw.rect(surf, PINK, (fx, r.top + 30, 18, 18))

        # Kick foot
        if self.state == "kick":
            kx = cx + 28 if self.facing > 0 else cx - 44
            pygame.draw.rect(surf, self.color, (kx, bot - 20, 24, 14))

        # Head
        pygame.draw.circle(surf, PINK, (cx, r.top + 22), 22)
        # Eyes (determined expression)
        eye_x = 6 if self.facing > 0 else -6
        pygame.draw.circle(surf, DARK, (cx + eye_x, r.top + 18), 5)
        pygame.draw.circle(surf, DARK, (cx + eye_x + self.facing * 12, r.top + 18), 5)
        if self.hp < self.max_hp // 3:
            pygame.draw.arc(surf, RED, (cx - 8, r.top + 26, 16, 10), 0, math.pi, 2)

        # Hit effect
        if self.hit_box and self.state in ("punch", "kick"):
            pygame.draw.rect(surf, (255, 255, 100, 120), self.hit_box, 2)

def draw_hpbar(surf, fighter, x, y, w=400):
    font = pygame.font.SysFont("consolas", 18, bold=True)
    pct = fighter.hp / fighter.max_hp
    col = GREEN if pct > 0.5 else (YELLOW if pct > 0.25 else RED)
    pygame.draw.rect(surf, GRAY, (x, y, w, 24))
    pygame.draw.rect(surf, col, (x, y, int(w * pct), 24))
    pygame.draw.rect(surf, WHITE, (x, y, w, 24), 2)
    name = font.render(fighter.name[:12], True, WHITE)
    surf.blit(name, (x, y - 22))

def draw_bg(surf, t):
    # Sky gradient
    for i in range(H):
        alpha = i / H
        r = int(20 + 30 * alpha)
        g = int(5 + 10 * alpha)
        b = int(40 + 20 * alpha)
        pygame.draw.line(surf, (r, g, b), (0, i), (W, i))

    # Crowd (silhouettes)
    for i in range(30):
        cx = 30 + i * 42
        cy = 490 + int(5 * math.sin(t * 2 + i))
        pygame.draw.ellipse(surf, (40, 20, 60), (cx - 15, cy - 30, 30, 40))
        pygame.draw.circle(surf, (60, 30, 80), (cx, cy - 35), 14)

    # Floor
    pygame.draw.rect(surf, (60, 40, 20), (0, FLOOR_Y, W, H - FLOOR_Y))
    pygame.draw.rect(surf, (100, 70, 30), (0, FLOOR_Y, W, 8))

    # Neon signs
    signs = [("KO!", CYAN, 60, 30), ("FIGHT!", ORANGE, 500, 20), ("WIN!", YELLOW, 1100, 30)]
    fnt = pygame.font.SysFont("consolas", 28, bold=True)
    for txt, col, sx, sy in signs:
        s = fnt.render(txt, True, col)
        flicker = 0.7 + 0.3 * math.sin(t * 7 + sx)
        s.set_alpha(int(255 * flicker))
        surf.blit(s, (sx, sy))

def run_street_fighter(screen, clock, player_name):
    pygame.display.set_caption("Street Fighter II")
    font = pygame.font.SysFont("consolas", 22, bold=True)
    font_big = pygame.font.SysFont("consolas", 54, bold=True)
    font_med = pygame.font.SysFont("consolas", 32, bold=True)

    def new_round(wins_p1, wins_p2):
        p1 = Fighter(200, 1, BLUE, player_name[:12], is_cpu=False)
        p2 = Fighter(W - 250, -1, RED, "CPU", is_cpu=True)
        return p1, p2

    wins_p1 = wins_p2 = 0
    p1, p2 = new_round(wins_p1, wins_p2)
    score = 0
    t = 0.0
    round_num = 1
    ROUNDS_TO_WIN = 2

    round_msg = "FIGHT!"
    round_timer = 1.5
    ko = False
    ko_timer = 0.0
    game_over = False

    def show_overlay(text, color, sub="", wait=2000):
        draw_bg(screen, t)
        draw_hpbar(screen, p1, 50, 50)
        draw_hpbar(screen, p2, W - 450, 50)
        p1.draw(screen)
        p2.draw(screen)
        s = font_big.render(text, True, color)
        screen.blit(s, (W//2 - s.get_width()//2, H//2 - 60))
        if sub:
            s2 = font_med.render(sub, True, WHITE)
            screen.blit(s2, (W//2 - s2.get_width()//2, H//2 + 30))
        pygame.display.flip()
        pygame.time.wait(wait)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt
        round_timer = max(0, round_timer - dt)
        if ko_timer > 0:
            ko_timer -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score
                # P1 controls: A/D=move, W=jump, J=punch, K=kick, L=block
                if event.key == pygame.K_w:
                    p1.do_jump()
                if event.key == pygame.K_j:
                    if p1.do_punch():
                        if p1.hit_box and p1.hit_box.colliderect(p2.rect()):
                            dmg = p2.take_hit(12 + random.randint(0, 6))
                            score += dmg * 5
                if event.key == pygame.K_k:
                    if p1.do_kick():
                        if p1.hit_box and p1.hit_box.colliderect(p2.rect()):
                            dmg = p2.take_hit(18 + random.randint(0, 8), True)
                            score += dmg * 7
                if event.key == pygame.K_l:
                    p1.block = not p1.block

        if game_over:
            if wins_p1 >= ROUNDS_TO_WIN:
                show_overlay("YOU WIN!", YELLOW, f"Score: {score}", 3000)
            else:
                show_overlay("YOU LOSE!", RED, f"Score: {score}", 3000)
            return score

        # P1 movement
        if round_timer == 0 and not ko:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                p1.vx = -180
                p1.state = "walk"
                p1.facing = -1
            elif keys[pygame.K_d]:
                p1.vx = 180
                p1.state = "walk"
                p1.facing = 1
            else:
                if p1.state == "walk":
                    p1.state = "idle"
                p1.vx = 0

            # Check punch/kick hits (continuous)
            if p1.hit_box:
                if p1.hit_box.colliderect(p2.rect()):
                    dmg = p2.take_hit(2)
                    score += dmg * 3

            p1.update(dt, p2)
            p2.update(dt, p1)

            # P2 hit by p2 own hitbox
            if p2.hit_box and p2.hit_box.colliderect(p1.rect()):
                p1.take_hit(8 + random.randint(0, 5))

            # Face each other
            if p1.x < p2.x:
                p1.facing = 1
            else:
                p1.facing = -1

        # KO check
        if not ko and (p1.hp == 0 or p2.hp == 0):
            ko = True
            ko_timer = 2.5
            if p2.hp == 0:
                wins_p1 += 1
                score += 1000 * round_num
                show_overlay("K.O.!", YELLOW, f"Round {round_num} - YOU WIN!", 2500)
            else:
                wins_p2 += 1
                show_overlay("K.O.!", RED, f"Round {round_num} - CPU WINS!", 2500)
            round_num += 1
            if wins_p1 >= ROUNDS_TO_WIN or wins_p2 >= ROUNDS_TO_WIN:
                game_over = True
            else:
                p1, p2 = new_round(wins_p1, wins_p2)
                round_timer = 1.5
                round_msg = f"ROUND {round_num}"
                ko = False

        # Draw
        draw_bg(screen, t)
        draw_hpbar(screen, p1, 50, 55)
        draw_hpbar(screen, p2, W - 450, 55)

        # Win pips
        for i in range(wins_p1):
            pygame.draw.circle(screen, YELLOW, (80 + i * 22, 88), 8)
        for i in range(wins_p2):
            pygame.draw.circle(screen, ORANGE, (W - 80 - i * 22, 88), 8)

        p1.draw(screen)
        p2.draw(screen)

        # Round message
        if round_timer > 0:
            s = font_big.render(round_msg, True, YELLOW)
            s.set_alpha(int(255 * min(1, round_timer)))
            screen.blit(s, (W//2 - s.get_width()//2, H//2 - 40))

        # Controls hint
        hint = font.render("A/D:Move  W:Jump  J:Punch  K:Kick  L:Block  ESC:Exit", True, (80, 80, 80))
        screen.blit(hint, (W//2 - hint.get_width()//2, H - 35))

        pygame.display.flip()

    return score
