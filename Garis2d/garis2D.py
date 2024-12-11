import pygame
import pandas as pd


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menggambar Garis")


BLUE = (0,0,255)

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
        pygame.draw.circle(screen, (255, 0, 0), (int(titik['x']), int(titik['y'])), 3)


    for _, garis in garis_df.iterrows():

        start_point = titik_df.iloc[garis['start']]
        end_point = titik_df.iloc[garis['end']]
        
        x1, y1 = int(start_point['x']), int(start_point['y'])
        x2, y2 = int(end_point['x']), int(end_point['y'])
        
        draw_line_dda(x1, y1, x2, y2)


    pygame.display.flip()


pygame.quit()