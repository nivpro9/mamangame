import pygame, random, math, sys

W, H = 1280, 720
DARK = (5, 5, 20)
WHITE = (255, 255, 255)
CYAN = (0, 200, 255)
RED = (255, 60, 60)
GREEN = (60, 255, 100)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)

def run_galaga(screen, clock, player_name):
    pygame.display.set_caption("Galaga")
    font = pygame.font.SysFont("consolas", 24, bold=True)
    font_big = pygame.font.SysFont("consolas", 48, bold=True)

    player = pygame.Rect(W // 2 - 20, H - 90, 40, 40)
    bullets, enemy_bullets = [], []
    bullet_cd = 0
    score, lives, wave = 0, 3, 1
    t = 0.0
    game_over = False

    STARS = [(random.randint(0, W), random.randint(0, H), random.randint(1, 3)) for _ in range(120)]

    def make_wave(w):
        rows = min(4 + w // 3, 7)
        cols = min(8 + w, 14)
        pad_x = max(40, (W - cols * 80) // 2)
        es = []
        for r in range(rows):
            for c in range(cols):
                color = [RED, ORANGE, YELLOW, CYAN, GREEN, WHITE, (200, 100, 255)][r % 7]
                pts = (rows - r) * 50 * w
                es.append({
                    'rect': pygame.Rect(pad_x + c * 80, 60 + r * 65, 36, 36),
                    'bx': pad_x + c * 80, 'by': 60 + r * 65,
                    'color': color, 'alive': True,
                    'dive': False, 'da': 0.0, 'pts': pts,
                })
        return es

    enemies = make_wave(wave)

    def draw_ship(surf, r, col):
        cx = r.centerx
        pts = [(cx, r.top), (r.left + 4, r.bottom), (cx, r.bottom - 10), (r.right - 4, r.bottom)]
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.circle(surf, WHITE, (cx, r.centery - 4), 5)

    def draw_enemy(surf, e):
        r, c = e['rect'], e['color']
        pygame.draw.rect(surf, c, r, border_radius=5)
        pygame.draw.circle(surf, WHITE, r.center, 7)
        pygame.draw.circle(surf, DARK, r.center, 4)

    def show_banner(text, color, sub=""):
        screen.fill(DARK)
        for sx, sy, sb in STARS:
            pygame.draw.circle(screen, WHITE, (sx, sy), sb)
        s = font_big.render(text, True, color)
        screen.blit(s, (W // 2 - s.get_width() // 2, H // 2 - 60))
        if sub:
            s2 = font.render(sub, True, WHITE)
            screen.blit(s2, (W // 2 - s2.get_width() // 2, H // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(2500)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt
        bullet_cd = max(0, bullet_cd - dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return score

        if game_over:
            show_banner("GAME OVER", RED, f"SCORE: {score}")
            return score

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 6
        if keys[pygame.K_RIGHT] and player.right < W:
            player.x += 6
        if keys[pygame.K_SPACE] and bullet_cd == 0:
            bullets.append(pygame.Rect(player.centerx - 3, player.top, 6, 18))
            bullet_cd = 0.22

        # Move player bullets
        bullets = [b for b in bullets if b.bottom > 0]
        for b in bullets:
            b.y -= 11

        # Move enemies
        alive = [e for e in enemies if e['alive']]
        for e in enemies:
            if not e['alive']:
                continue
            if not e['dive']:
                e['rect'].x = int(e['bx'] + 35 * math.sin(t * 1.4 + e['bx'] * 0.01))
                if random.random() < 0.0008 + wave * 0.0001:
                    e['dive'] = True
                    e['da'] = random.uniform(-0.4, 0.4)
            else:
                e['rect'].y += 5 + wave * 0.3
                e['rect'].x += int(e['da'] * 28)
                if e['rect'].top > H:
                    e['rect'].x, e['rect'].y = e['bx'], e['by']
                    e['dive'] = False

        # Enemy shooting
        if alive and random.random() < 0.018 + wave * 0.003:
            s = random.choice(alive)
            enemy_bullets.append(pygame.Rect(s['rect'].centerx - 3, s['rect'].bottom, 6, 16))
        enemy_bullets = [b for b in enemy_bullets if b.top < H]
        for b in enemy_bullets:
            b.y += 7 + wave * 0.3

        # Collisions: bullets -> enemies
        for b in bullets[:]:
            for e in enemies:
                if e['alive'] and b.colliderect(e['rect']):
                    e['alive'] = False
                    score += e['pts']
                    if b in bullets:
                        bullets.remove(b)
                    break

        # Enemy bullets -> player
        for b in enemy_bullets[:]:
            if b.colliderect(player):
                enemy_bullets.remove(b)
                lives -= 1
                if lives <= 0:
                    game_over = True

        # Diving enemy -> player
        for e in enemies:
            if e['alive'] and e['dive'] and e['rect'].colliderect(player):
                e['alive'] = False
                lives -= 1
                if lives <= 0:
                    game_over = True

        # New wave
        if not [e for e in enemies if e['alive']]:
            wave += 1
            enemies = make_wave(wave)
            show_banner(f"WAVE {wave}", CYAN, "GET READY!")

        # Draw
        screen.fill(DARK)
        for sx, sy, sb in STARS:
            pygame.draw.circle(screen, WHITE, (sx, sy), sb)
        for e in enemies:
            if e['alive']:
                draw_enemy(screen, e)
        for b in bullets:
            pygame.draw.rect(screen, CYAN, b, border_radius=3)
        for b in enemy_bullets:
            pygame.draw.rect(screen, RED, b, border_radius=3)
        draw_ship(screen, player, GREEN)

        # HUD
        hud = font.render(f"SCORE: {score:>7}   {'♥ ' * lives}  WAVE: {wave}", True, WHITE)
        screen.blit(hud, (10, 10))
        esc = font.render("ESC: Exit", True, (80, 80, 80))
        screen.blit(esc, (W - esc.get_width() - 10, 10))

        pygame.display.flip()

    return score
