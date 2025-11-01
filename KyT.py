import pygame, random, math, time

# Khởi tạo pygame
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Nguyễn Thị Anh Thư ❤️ Từ Ngọc Nguyên Khôi")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)

# Màu
PINK = (255, 105, 180)
RED = (255, 50, 80)
WHITE = (255, 255, 255)
PURPLE = (160, 120, 255)
BLACK = (0, 0, 0)

# Trái tim bay
class Heart:
    def __init__(self):
        self.x = random.randint(0, W)
        self.y = H + 20
        self.size = random.randint(10, 30)
        self.speed = random.uniform(1.5, 4)
        self.angle = random.uniform(-1, 1)
        self.color = random.choice([RED, PINK, PURPLE])

    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.y / 20) * 1.5

    def draw(self, s):
        points = []
        for t in range(0, 360, 10):
            rad = math.radians(t)
            x = 16 * math.sin(rad)**3
            y = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
            points.append((self.x + x * self.size/20, self.y - y * self.size/20))
        pygame.draw.polygon(s, self.color, points)

# Danh sách trái tim
hearts = [Heart() for _ in range(30)]

# Hiệu ứng text
def draw_glowing_text(text, font, x, y, color, pulse=1.0):
    glow = pygame.Surface(font.size(text))
    glow.set_colorkey((0, 0, 0))
    glow.set_alpha(80)
    for i in range(5):
        text_surface = font.render(text, True, (min(255, color[0] + 50),
                                                min(255, color[1] + 50),
                                                min(255, color[2] + 50)))
        glow.blit(text_surface, (i, i))
    screen.blit(glow, (x - i*pulse, y - i*pulse))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Animation vòng sáng
class LightCircle:
    def __init__(self):
        self.x = random.randint(100, W-100)
        self.y = random.randint(100, H-100)
        self.radius = random.randint(20, 80)
        self.alpha = random.randint(40, 100)
        self.color = random.choice([PINK, PURPLE, WHITE])
        self.grow = True

    def update(self):
        if self.grow:
            self.radius += 1
            if self.radius > 100: self.grow = False
        else:
            self.radius -= 1
            if self.radius < 20: self.grow = True

    def draw(self, s):
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, self.alpha), (self.x, self.y), self.radius)
        s.blit(surf, (0, 0))

lights = [LightCircle() for _ in range(10)]

# Main loop
running = True
start_time = time.time()
pulse = 1
while running:
    screen.fill(BLACK)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Cập nhật hiệu ứng
    for h in hearts:
        h.update()
        if h.y < -20:
            hearts.remove(h)
            hearts.append(Heart())
        h.draw(screen)

    for l in lights:
        l.update()
        l.draw(screen)

    # Vòng sáng và chữ
    elapsed = time.time() - start_time
    pulse = 1 + math.sin(elapsed * 2) * 0.1

    draw_glowing_text("Nguyễn Thị Anh Thư", font, 90, 200, PINK, pulse)
    draw_glowing_text("❤️", font, 430, 260, RED, pulse)
    draw_glowing_text("Từ Ngọc Nguyên Khôi", font, 520, 330, PURPLE, pulse)
    text2 = small_font.render("Tình yêu vĩnh cửu ✨", True, WHITE)
    screen.blit(text2, (W/2 - text2.get_width()/2, 500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
