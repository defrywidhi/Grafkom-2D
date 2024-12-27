import pygame
import pandas as pd
import numpy as np

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Transformations")

BLUE = (0, 0, 255)

def draw_line_dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps if steps > 0 else 0
    y_increment = dy / steps if steps > 0 else 0
    x, y = x1, y1
    for _ in range(int(steps)):
        screen.set_at((int(x), int(y)), BLUE)
        x += x_increment
        y += y_increment

def create_scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def create_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def create_rotation_x_matrix(angle):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def create_rotation_y_matrix(angle):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])



def load_data(titik_file, garis_file):
    titik_df = pd.read_csv(titik_file, header=None, names=['x', 'y', 'z'])
    garis_df = pd.read_csv(garis_file, header=None, names=['start', 'end'])
    return titik_df, garis_df

def apply_transformation(points, transformation_matrix):
    homogeneous_points = np.ones((len(points), 4))
    homogeneous_points[:, 0:3] = points[['x', 'y', 'z']].values
    
    transformed_points = np.dot(homogeneous_points, transformation_matrix.T)
    
    result = pd.DataFrame({
        'x': transformed_points[:, 0],
        'y': transformed_points[:, 1],
        'z': transformed_points[:, 2]
    })
    return result

def rotate_around_center(points, rotation_x_angle, rotation_y_angle):
    center = points[['x', 'y', 'z']].mean()
    
    translate_to_origin = create_translation_matrix(-center['x'], -center['y'], -center['z'])
    translate_back = create_translation_matrix(center['x'], center['y'], center['z'])
    
    rotation_x = create_rotation_x_matrix(rotation_x_angle)
    rotation_y = create_rotation_y_matrix(rotation_y_angle)
    
    combined_rotation = np.linalg.multi_dot([
        translate_back,
        rotation_y,
        rotation_x,
        translate_to_origin
    ])
    return apply_transformation(points, combined_rotation)

try:
    titik_df, garis_df = load_data('Garis3d/titik.csv', 'Garis3d/garis.csv')
except FileNotFoundError:
    print("File CSV tidak ditemukan. Pastikan 'titik.csv' dan 'garis.csv' ada.")
    pygame.quit()
    exit()

scale_matrix = create_scale_matrix(100, 100, 100)
titik_df = apply_transformation(titik_df, scale_matrix)

initial_position = create_translation_matrix(100, 200, 0)
titik_df = apply_transformation(titik_df, initial_position)

original_positions = titik_df.copy()



running = True
clock = pygame.time.Clock()
angle_x = 0
angle_y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    transformed_df = rotate_around_center(original_positions, angle_x, angle_y)

    for _, titik in transformed_df.iterrows():
        pygame.draw.circle(screen, (255, 0, 0), (int(titik['x']), int(titik['y'])), 3)

    for _, garis in garis_df.iterrows():
        start_point = transformed_df.iloc[garis['start']]
        end_point = transformed_df.iloc[garis['end']]
        draw_line_dda(int(start_point['x']), int(start_point['y']),
                     int(end_point['x']), int(end_point['y']))

    pygame.display.flip()
    
    angle_x += 1
    angle_y += 1
    clock.tick(60)

pygame.quit()