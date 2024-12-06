import pygame
import pandas as pd


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menggambar Garis")


def bresenham(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x1 += sx
        if err2 < dx:
            err += dx
            y1 += sy
    return points


def load_data(titik_file, garis_file):

    titik_df = pd.read_csv(titik_file, header=None, names=['x', 'y', 'z'])
    

    garis_df = pd.read_csv(garis_file, header=None, names=['start', 'end'])
    
    return titik_df, garis_df


try:
    titik_df, garis_df = load_data('Garis2d/titik.csv', 'Garis2d/garis.csv')
except FileNotFoundError:
    print("File CSV tidak ditemukan. Pastikan 'titik.csv' dan 'garis.csv' ada.")
    pygame.quit()
    exit()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))


    for _, titik in titik_df.iterrows():
        pygame.draw.circle(screen, (255, 0, 0), (int(titik['x']), int(titik['y'])), 5)


    for _, garis in garis_df.iterrows():

        start_point = titik_df.iloc[garis['start']]
        end_point = titik_df.iloc[garis['end']]
        
        x1, y1 = int(start_point['x']), int(start_point['y'])
        x2, y2 = int(end_point['x']), int(end_point['y'])
        

        points = bresenham(x1, y1, x2, y2)
        

        for point in points:
            pygame.draw.circle(screen, (0, 0, 0), point, 3)


    pygame.display.flip()


pygame.quit()