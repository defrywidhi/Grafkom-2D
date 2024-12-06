import pygame
import pandas as pd

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gambar Garis dengan Algoritma Bresenham")

# Fungsi untuk menggambar garis menggunakan algoritma Bresenham
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

# Fungsi untuk membaca titik dan garis dari CSV
def load_data(titik_file, garis_file):
    # Baca file titik
    titik_df = pd.read_csv(titik_file, header=None, names=['x', 'y', 'z'])
    
    # Baca file garis
    garis_df = pd.read_csv(garis_file, header=None, names=['start', 'end'])
    
    return titik_df, garis_df

# Muat data dari file CSV
try:
    titik_df, garis_df = load_data('Garis2d/titik.csv', 'Garis2d/garis.csv')
except FileNotFoundError:
    print("File CSV tidak ditemukan. Pastikan 'titik.csv' dan 'garis.csv' ada.")
    pygame.quit()
    exit()

# Loop utama Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mengisi latar belakang
    screen.fill((255, 255, 255))

    # Menggambar titik-titik
    for _, titik in titik_df.iterrows():
        pygame.draw.circle(screen, (255, 0, 0), (int(titik['x']), int(titik['y'])), 3)

    # Menggambar garis
    for _, garis in garis_df.iterrows():
        # Ambil koordinat titik dari DataFrame titik
        start_point = titik_df.iloc[garis['start']]
        end_point = titik_df.iloc[garis['end']]
        
        x1, y1 = int(start_point['x']), int(start_point['y'])
        x2, y2 = int(end_point['x']), int(end_point['y'])
        
        # Gunakan algoritma Bresenham untuk menggambar garis
        points = bresenham(x1, y1, x2, y2)
        
        # Gambar titik-titik garis
        for point in points:
            pygame.draw.circle(screen, (0, 0, 0), point, 1)

    # Memperbarui tampilan
    pygame.display.flip()

# Menutup Pygame
pygame.quit()