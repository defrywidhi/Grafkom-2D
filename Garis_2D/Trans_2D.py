import pygame
import pandas as pd
import math

pygame.init()

# Setup layar pygame
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menggambar Garis dengan Transformasi")

# Warna
BLUE = (0, 0, 255)

# Fungsi menggambar garis menggunakan algoritma DDA
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

# Fungsi untuk membaca data titik dan garis dari file CSV
def load_data(titik_file, garis_file):
    titik_df = pd.read_csv(titik_file, header=None, names=['x', 'y', 'z'])
    garis_df = pd.read_csv(garis_file, header=None, names=['start', 'end'])
    return titik_df, garis_df

# Fungsi untuk menerapkan skala menggunakan matriks
def apply_scaling(titik_df, sx, sy):
    scaling_matrix = [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]
    for index, row in titik_df.iterrows():
        point = [row['x'], row['y'], 1]
        scaled_point = [
            point[0] * scaling_matrix[0][0] + point[1] * scaling_matrix[0][1] + point[2] * scaling_matrix[0][2],
            point[0] * scaling_matrix[1][0] + point[1] * scaling_matrix[1][1] + point[2] * scaling_matrix[1][2],
            point[0] * scaling_matrix[2][0] + point[1] * scaling_matrix[2][1] + point[2] * scaling_matrix[2][2],
        ]
        titik_df.at[index, 'x'] = scaled_point[0]
        titik_df.at[index, 'y'] = scaled_point[1]
    return titik_df

# Fungsi translasi menggunakan matriks
def apply_translation(titik_df, tx, ty):
    translation_matrix = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]
    for index, row in titik_df.iterrows():
        point = [row['x'], row['y'], 1]
        translated_point = [
            point[0] * translation_matrix[0][0] + point[1] * translation_matrix[0][1] + point[2] * translation_matrix[0][2],
            point[0] * translation_matrix[1][0] + point[1] * translation_matrix[1][1] + point[2] * translation_matrix[1][2],
            point[0] * translation_matrix[2][0] + point[1] * translation_matrix[2][1] + point[2] * translation_matrix[2][2],
        ]
        titik_df.at[index, 'x'] = translated_point[0]
        titik_df.at[index, 'y'] = translated_point[1]
    return titik_df

# Fungsi rotasi menggunakan matriks
def apply_rotation(titik_df, angle):
    angle_rad = math.radians(angle)
    # Matriks rotasi
    rotation_matrix = [
        [math.cos(angle_rad), -math.sin(angle_rad), 0],
        [math.sin(angle_rad), math.cos(angle_rad), 0],
        [0, 0, 1]
    ]
    
    # Hitung centroid (pusat massa)
    x_centroid = titik_df['x'].mean()
    y_centroid = titik_df['y'].mean()
    
    # Translasi ke pusat (centroid)
    for index, row in titik_df.iterrows():
        titik_df.at[index, 'x'] -= x_centroid
        titik_df.at[index, 'y'] -= y_centroid

    # Rotasi di sekitar titik asal (0, 0)
    for index, row in titik_df.iterrows():
        point = [row['x'], row['y'], 1]
        rotated_point = [
            point[0] * rotation_matrix[0][0] + point[1] * rotation_matrix[0][1] + point[2] * rotation_matrix[0][2],
            point[0] * rotation_matrix[1][0] + point[1] * rotation_matrix[1][1] + point[2] * rotation_matrix[1][2],
            point[0] * rotation_matrix[2][0] + point[1] * rotation_matrix[2][1] + point[2] * rotation_matrix[2][2],
        ]
        titik_df.at[index, 'x'] = rotated_point[0]
        titik_df.at[index, 'y'] = rotated_point[1]

    # Kembalikan translasi ke posisi asal
    for index, row in titik_df.iterrows():
        titik_df.at[index, 'x'] += x_centroid
        titik_df.at[index, 'y'] += y_centroid

    return titik_df

# Load data dari file CSV
try:
    titik_df, garis_df = load_data('Garis2d/titik.csv', 'Garis2d/garis.csv')
except FileNotFoundError:
    print("File CSV tidak ditemukan. Pastikan 'titik.csv' dan 'garis.csv' ada.")
    pygame.quit()
    exit()

# Terapkan transformasi
scale_x, scale_y = 50, 50  # Faktor skala
translate_x, translate_y = 250, 50  # Nilai translasi
rotation_speed = 1
current_angle = 0

titik_df = apply_scaling(titik_df, scale_x, scale_y)
titik_df = apply_translation(titik_df, translate_x, translate_y)

# Loop utama aplikasi
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Membersihkan layar
    screen.fill((255, 255, 255))

    current_angle += rotation_speed
    current_angle %= 360

    titik_df = apply_rotation(titik_df, rotation_speed)


    # Gambar semua titik
    for _, titik in titik_df.iterrows():
        pygame.draw.circle(screen, (255, 0, 0), (int(titik['x']), int(titik['y'])), 3)

    # Gambar semua garis
    for _, garis in garis_df.iterrows():
        start_point = titik_df.iloc[garis['start']]
        end_point = titik_df.iloc[garis['end']]
        x1, y1 = int(start_point['x']), int(start_point['y'])
        x2, y2 = int(end_point['x']), int(end_point['y'])
        draw_line_dda(x1, y1, x2, y2)

    # Update tampilan layar
    pygame.display.flip()
    clock.tick(60)

pygame.quit()