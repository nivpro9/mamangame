import pygame
import sys
import math
import random
from scores import save_score, get_all_scores

W, H = 1280, 720
FPS = 60

# Colors
DARK_BG   = (8, 3, 18)
BLACK     = (0, 0, 0)
WHITE     = (255, 255, 255)
PURPLE    = (140, 40, 230)
BLUE      = (30, 90, 255)
CYAN      = (0, 200, 255)
NEON_PINK = (255, 0, 160)
YELLOW    = (255, 220, 0)
ORANGE    = (255, 140, 0)
GRAY      = (70, 70, 90)

GAME_COLORS = [YELLOW, NEON_PINK, CYAN, ORANGE]
GAME_KEYS   = ["↑/↓/←/→: Move  SPACE: Eat dots",
               "←/→: Move  SPACE: Shoot",
               "←/→/↑/↓: Move  SPACE: Jump",
               "A/D: Move  W: Jump  J: Punch  K: Kick  L: Block"]
GAME_ICONS  = ["PAC", "GAL", "D.K", "S.F"]

# Particle
class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(40, 140)
        self.x, self.y = float(x), float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 1.0
        self.r = random.randint(2, 5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt * 1.2
        return self.life > 0

    def draw(self, surf):
        alpha = max(0, int(255 * self.life))
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.r, self.r), self.r)
        surf.blit(s, (int(self.x) - self.r, int(self.y) - self.r))


def glow_text(surf, text, font, color, cx, cy, glow_size=12):
    for i in range(glow_size, 0, -3):
        alpha = 18 - i
        s = font.render(text, True, color)
        s.set_alpha(alpha * 6)
        sx = cx - s.get_width() // 2
        sy = cy - s.get_height() // 2
        surf.blit(s, (sx - i // 2, sy - i // 2))
    main = font.render(text, True, color)
    surf.blit(main, (cx - main.get_width() // 2, cy - main.get_height() // 2))


def neon_rect(surf, color, rect, width=2, glow=8):
    for i in range(glow, 0, -2):
        s = pygame.Surface((rect.w + i * 2, rect.h + i * 2), pygame.SRCALPHA)
        alpha = max(0, 60 - i * 7)
        pygame.draw.rect(s, (*color, alpha), s.get_rect(), width + 1, border_radius=6)
        surf.blit(s, (rect.x - i, rect.y - i))
    pygame.draw.rect(surf, color, rect, width, border_radius=6)


class ArcadeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("RETRO ARCADE MACHINE")
        self.clock = pygame.time.Clock()

        self.font_xl   = pygame.font.SysFont("consolas", 56, bold=True)
        self.font_lg   = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_md   = pygame.font.SysFont("consolas", 28, bold=True)
        self.font_sm   = pygame.font.SysFont("consolas", 20)

        self.state = "name_entry"
        self.name  = ""
        self.selected = 0
        self.games = ["Pac-Man", "Galaga", "Donkey Kong", "Street Fighter II"]
        self.t = 0.0
        self.particles = []
        self.stars = [(random.randint(0, W), random.randint(0, H),
                       random.uniform(0.3, 1.5), random.uniform(0, math.tau)) for _ in range(200)]

        self.scanline_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        for y in range(0, H, 3):
            pygame.draw.line(self.scanline_surf, (0, 0, 0, 35), (0, y), (W, y))

    # ─── helpers ─────────────────────────────────────────────────────────────
    def spawn_particles(self, x, y, color, n=12):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def draw_bg(self):
        self.screen.fill(DARK_BG)
        # Animated stars
        for i, (sx, sy, sp, phase) in enumerate(self.stars):
            brightness = int(80 + 60 * math.sin(self.t * sp + phase))
            pygame.draw.circle(self.screen, (brightness, brightness, brightness + 20), (sx, sy), 1)
        # LED strip top + bottom
        for bar_y in (0, H - 8):
            for bx in range(0, W, 16):
                hue = (bx / W + self.t * 0.3) % 1.0
                col = pygame.Color(0)
                col.hsva = (hue * 360, 100, 90, 100)
                pygame.draw.rect(self.screen, col, (bx, bar_y, 12, 8))
        self.screen.blit(self.scanline_surf, (0, 0))

    # ─── name entry ──────────────────────────────────────────────────────────
    def draw_name_entry(self):
        self.draw_bg()

        # Outer arcade frame
        frame = pygame.Rect(W // 2 - 340, 80, 680, 520)
        neon_rect(self.screen, PURPLE, frame, 3, 18)

        glow_text(self.screen, "RETRO ARCADE", self.font_xl, CYAN, W // 2, 170, 16)
        glow_text(self.screen, "MACHINE", self.font_lg, PURPLE, W // 2, 228, 12)

        # Decorative icons
        icons = ["★  PAC-MAN  ★", "★  GALAGA   ★", "★ DONKEY KONG ★", "★ STREET FIGHTER ★"]
        for i, ico in enumerate(icons):
            col = GAME_COLORS[i]
            s = self.font_sm.render(ico, True, col)
            s.set_alpha(int(150 + 80 * math.sin(self.t * 2 + i)))
            self.screen.blit(s, (W // 2 - s.get_width() // 2, 290 + i * 28))

        glow_text(self.screen, "ENTER YOUR NAME", self.font_md, YELLOW, W // 2, 430, 8)

        # Name box
        box = pygame.Rect(W // 2 - 220, 456, 440, 54)
        neon_rect(self.screen, CYAN, box, 2, 10)
        cursor = "_" if int(self.t * 2) % 2 else " "
        name_s = self.font_lg.render(self.name + cursor, True, WHITE)
        self.screen.blit(name_s, (box.x + 12, box.y + 9))

        hint = self.font_sm.render("Press ENTER to start", True, GRAY)
        self.screen.blit(hint, (W // 2 - hint.get_width() // 2, 530))

    def handle_name_entry(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name.strip():
                self.state = "menu"
                self.spawn_particles(W // 2, 456 + 27, CYAN, 30)
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif len(self.name) < 14 and (event.unicode.isalnum() or event.unicode in (" ", "_", "-")):
                self.name += event.unicode

    # ─── game menu ───────────────────────────────────────────────────────────
    def draw_menu(self):
        self.draw_bg()

        glow_text(self.screen, "SELECT GAME", self.font_xl, NEON_PINK, W // 2, 52, 16)

        pname = self.font_md.render(f"PLAYER: {self.name.upper()}", True, CYAN)
        self.screen.blit(pname, (18, 15))
        hint_s = self.font_sm.render("S = High Scores", True, GRAY)
        self.screen.blit(hint_s, (W - hint_s.get_width() - 18, 18))

        pw, ph = 560, 240
        positions = [
            (W // 2 - pw - 16, 100),
            (W // 2 + 16,       100),
            (W // 2 - pw - 16, 358),
            (W // 2 + 16,       358),
        ]

        for i, (game, pos) in enumerate(zip(self.games, positions)):
            col = GAME_COLORS[i]
            rect = pygame.Rect(pos[0], pos[1], pw, ph)
            selected = (i == self.selected)

            # Background fill
            bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
            alpha = 55 if selected else 18
            bg.fill((*col, alpha))
            self.screen.blit(bg, pos)

            # Border
            neon_rect(self.screen, col if selected else tuple(c // 3 for c in col),
                      rect, 3 if selected else 1, 12 if selected else 3)

            # Icon badge
            badge = pygame.Rect(pos[0] + 14, pos[1] + 14, 80, 56)
            badge_bg = pygame.Surface((80, 56), pygame.SRCALPHA)
            badge_bg.fill((*col, 80))
            self.screen.blit(badge_bg, (badge.x, badge.y))
            pygame.draw.rect(self.screen, col, badge, 2, border_radius=6)
            icon_s = self.font_md.render(GAME_ICONS[i], True, WHITE)
            self.screen.blit(icon_s, (badge.x + 40 - icon_s.get_width() // 2,
                                       badge.y + 28 - icon_s.get_height() // 2))

            # Game title
            title_c = col if selected else tuple(c // 2 for c in col)
            title_s = self.font_lg.render(game, True, title_c)
            self.screen.blit(title_s, (pos[0] + 108, pos[1] + 24))

            # Controls
            ctrl = self.font_sm.render(GAME_KEYS[i], True, GRAY if not selected else WHITE)
            self.screen.blit(ctrl, (pos[0] + 14, pos[1] + 84))

            # Selected indicator
            if selected:
                pulse = 0.6 + 0.4 * math.sin(self.t * 5)
                press_s = self.font_md.render("▶  PRESS ENTER", True, WHITE)
                press_s.set_alpha(int(255 * pulse))
                self.screen.blit(press_s, (pos[0] + 14, pos[1] + ph - 46))

                # Particles from corners
                if random.random() < 0.15:
                    self.spawn_particles(rect.right, rect.centery, col, 3)

        nav = self.font_sm.render("ARROWS: Navigate   ENTER: Play   S: Scores   ESC: Back", True, GRAY)
        self.screen.blit(nav, (W // 2 - nav.get_width() // 2, H - 32))

    def handle_menu(self, event):
        if event.type == pygame.KEYDOWN:
            prev = self.selected
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 2) % 4
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 2) % 4
            elif event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % 4
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.launch_game(self.selected)
            elif event.key == pygame.K_s:
                self.state = "scores"
            elif event.key == pygame.K_ESCAPE:
                self.state = "name_entry"
            if self.selected != prev:
                pw, ph = 560, 240
                positions = [(W//2-pw-16,100),(W//2+16,100),(W//2-pw-16,358),(W//2+16,358)]
                pos = positions[self.selected]
                self.spawn_particles(pos[0]+pw//2, pos[1]+ph//2, GAME_COLORS[self.selected], 15)

    def launch_game(self, idx):
        game = self.games[idx]
        score = 0
        try:
            if game == "Pac-Man":
                from pacman import run_pacman
                score = run_pacman(self.screen, self.clock, self.name)
            elif game == "Galaga":
                from galaga import run_galaga
                score = run_galaga(self.screen, self.clock, self.name)
            elif game == "Donkey Kong":
                from donkey_kong import run_donkey_kong
                score = run_donkey_kong(self.screen, self.clock, self.name)
            elif game == "Street Fighter II":
                from street_fighter import run_street_fighter
                score = run_street_fighter(self.screen, self.clock, self.name)
        except Exception as e:
            print(f"Game error: {e}")

        pygame.display.set_caption("RETRO ARCADE MACHINE")
        if score > 0:
            save_score(game, self.name or "AAA", score)
        self.state = "scores"
        self.last_game = game
        self.last_score = score

    # ─── scores ──────────────────────────────────────────────────────────────
    def draw_scores(self):
        self.draw_bg()
        glow_text(self.screen, "HIGH SCORES", self.font_xl, YELLOW, W // 2, 52, 14)

        all_sc = get_all_scores()
        col_w = W // 4

        for idx, game in enumerate(self.games):
            col = GAME_COLORS[idx]
            x = idx * col_w + 14
            y = 110

            # Column header
            neon_rect(self.screen, col, pygame.Rect(x, y, col_w - 20, 36), 2, 6)
            hdr = self.font_sm.render(game, True, col)
            self.screen.blit(hdr, (x + 8, y + 8))

            entries = all_sc.get(game, [])
            for rank, e in enumerate(entries[:8], 1):
                ey = y + 50 + (rank - 1) * 36
                rank_col = YELLOW if rank == 1 else (GRAY if rank > 3 else WHITE)
                line = f"{rank}.{e['name'][:8]:<8}{e['score']:>7}"
                s = self.font_sm.render(line, True, rank_col)
                self.screen.blit(s, (x + 4, ey))
                if rank <= 3:
                    pygame.draw.rect(self.screen, (*rank_col, 30),
                                     (x, ey - 2, col_w - 20, 26))

            if not entries:
                empty = self.font_sm.render("No scores yet", True, GRAY)
                self.screen.blit(empty, (x + 8, y + 60))

        # Last score
        if hasattr(self, "last_score") and self.last_score > 0:
            msg = self.font_md.render(
                f"Last game: {getattr(self,'last_game','')} — {self.name}: {self.last_score}",
                True, CYAN)
            self.screen.blit(msg, (W // 2 - msg.get_width() // 2, H - 70))

        back = self.font_sm.render("Press any key to return to menu", True, GRAY)
        self.screen.blit(back, (W // 2 - back.get_width() // 2, H - 38))

    # ─── main loop ───────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.t += dt
            self.particles = [p for p in self.particles if p.update(dt)]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if self.state == "name_entry":
                    self.handle_name_entry(event)
                elif self.state == "menu":
                    self.handle_menu(event)
                elif self.state == "scores":
                    if event.type == pygame.KEYDOWN:
                        self.state = "menu"

            if self.state == "name_entry":
                self.draw_name_entry()
            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "scores":
                self.draw_scores()

            # Particles on top
            for p in self.particles:
                p.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    ArcadeApp().run()
