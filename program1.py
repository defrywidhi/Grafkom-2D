import pygame
import sys
import time
import math

pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Program Pembuatan Garis dan Lingkaran")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

font = pygame.font.SysFont(None, 24)

points = []
shapes = []
current_algorithm = "brute_force"

def draw_line_brute_force(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        for y in range(y1, y2 + 1):
            screen.set_at((x1, y), RED)
    else:
        m = dy / dx
        for x in range(x1, x2 + 1):
            y = y1 + int(m * (x - x1))
            screen.set_at((x, y), RED)

def draw_line_dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        screen.set_at((int(x), int(y)), BLUE)
        x += x_increment
        y += y_increment

def draw_line_bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        screen.set_at((x1, y1), GREEN)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_circle_bresenham(x_center, y_center, radius):
    x = 0
    y = radius
    d = 3 - (2 * radius)
    draw_circle_points(x_center, y_center, x, y)
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
        draw_circle_points(x_center, y_center, x, y)


def draw_circle_points(x_center, y_center, x, y):
    screen.set_at((x_center + x, y_center + y), GREEN)
    screen.set_at((x_center - x, y_center + y), GREEN)
    screen.set_at((x_center + x, y_center - y), GREEN)
    screen.set_at((x_center - x, y_center - y), GREEN)
    screen.set_at((x_center + y, y_center + x), GREEN)
    screen.set_at((x_center - y, y_center + x), GREEN)
    screen.set_at((x_center + y, y_center - x), GREEN)
    screen.set_at((x_center - y, y_center - x), GREEN)


def draw_shape(x1, y1, x2, y2, algorithm):
    start_time = time.perf_counter()
    if algorithm == "brute_force":
        draw_line_brute_force(x1, y1, x2, y2)
    elif algorithm == "dda":
        draw_line_dda(x1, y1, x2, y2)
    elif algorithm == "bresenham":
        draw_line_bresenham(x1, y1, x2, y2)
    elif algorithm == "circle":
        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        draw_circle_bresenham(x1, y1, radius)
    return time.perf_counter() - start_time


def draw_text(text, pos):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, pos)


running = True
while running:
    screen.fill(WHITE)
    

    for shape in shapes:
        x1, y1, x2, y2, algorithm, draw_time = shape
        draw_shape(x1, y1, x2, y2, algorithm)
        draw_text(f"{algorithm} - ({x1}, {y1}) to ({x2}, {y2})", (x1, y1 - 20))
        draw_text(f"Time: {draw_time:.8f} sec", (x1, y1 - 40))


    for point in points:
        pygame.draw.circle(screen, BLUE, point, 5)


    if current_algorithm:
        draw_text(f"Algoritma Yang digunakan : {current_algorithm}", (10, 10))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_algorithm = "brute_force"
            elif event.key == pygame.K_2:
                current_algorithm = "dda"
            elif event.key == pygame.K_3:
                current_algorithm = "bresenham"
            elif event.key == pygame.K_4:
                current_algorithm = "circle"
            elif event.key == pygame.K_r:
                points = []
                shapes = []

        elif event.type == pygame.MOUSEBUTTONDOWN and current_algorithm:
            points.append(event.pos)
            if len(points) == 2:
                x1, y1 = points[0]
                x2, y2 = points[1]
                draw_time = draw_shape(x1, y1, x2, y2, current_algorithm)
                shapes.append((x1, y1, x2, y2, current_algorithm, draw_time))
                points = [] 
pygame.quit()
