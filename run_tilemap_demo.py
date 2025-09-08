import pygame
import os
import sys
import json

# --- CONFIG ---
TILE_SIZE = 48
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- PATHS ---
IMG_ROOT = os.path.join('assets', 'images')
TILESET_PATH = IMG_ROOT  # Use assets/images for tilesets
CHAR_PATH = IMG_ROOT     # Use assets/images for characters
BUILDINGS_JSON = os.path.join('rpgmaker_export', 'buildings.json')
NPCS_JSON = os.path.join('rpgmaker_export', 'npcs.json')

# --- TILESET LOADER ---
def load_tileset(image_path, tile_size):
    tiles = []
    img = pygame.image.load(image_path).convert_alpha()
    img_w, img_h = img.get_size()
    print(f"Loaded tileset: {image_path} ({img_w}x{img_h})")
    for y in range(0, img_h, tile_size):
        for x in range(0, img_w, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            tile = img.subsurface(rect)
            tiles.append(tile)
    print(f"Sliced {len(tiles)} tiles from tileset.")
    return tiles

# --- SPRITE LOADER ---
def load_sprite(image_path):
    img = pygame.image.load(image_path).convert_alpha()
    print(f"Loaded sprite: {image_path} ({img.get_width()}x{img.get_height()})")
    return img

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # --- LOAD TILESET ---
    tiles = []
    tileset_files = [f for f in os.listdir(TILESET_PATH) if f.lower().endswith('.png')]
    if tileset_files:
        tileset_img_path = os.path.join(TILESET_PATH, tileset_files[0])
        tiles = load_tileset(tileset_img_path, TILE_SIZE)
    else:
        print('No tileset images found in', TILESET_PATH)
    if not tiles:
        print('No tiles loaded, using placeholder tiles.')
        # Create colored placeholder tiles
        for i in range(8):
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((32*i, 255-32*i, 128))
            tiles.append(surf)

    # --- SAMPLE TILEMAP (16x12 grid) ---
    tilemap = [[(x + y) % len(tiles) for x in range(16)] for y in range(12)]
    print(f"Tilemap size: {len(tilemap[0])}x{len(tilemap)}")

    # --- LOAD BUILDINGS/NPCS ---
    buildings = []
    if os.path.exists(BUILDINGS_JSON):
        with open(BUILDINGS_JSON) as f:
            buildings = json.load(f)
    print(f"Loaded {len(buildings)} buildings.")
    npcs = []
    if os.path.exists(NPCS_JSON):
        with open(NPCS_JSON) as f:
            npcs = json.load(f)
    print(f"Loaded {len(npcs)} NPCs.")

    # --- LOAD SPRITES ---
    char_files = [f for f in os.listdir(CHAR_PATH) if f.lower().endswith('.png')]
    sprites = {}
    for fname in char_files:
        sprites[fname] = load_sprite(os.path.join(CHAR_PATH, fname))
    print(f"Loaded {len(sprites)} sprites.")

    # --- CAMERA ---
    cam_x, cam_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    cam_x = max(cam_x - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    cam_x = min(cam_x + 1, len(tilemap[0]) - SCREEN_WIDTH // TILE_SIZE)
                elif event.key == pygame.K_UP:
                    cam_y = max(cam_y - 1, 0)
                elif event.key == pygame.K_DOWN:
                    cam_y = min(cam_y + 1, len(tilemap) - SCREEN_HEIGHT // TILE_SIZE)

        screen.fill((0, 0, 0))

        # --- DRAW TILEMAP ---
        for y in range(SCREEN_HEIGHT // TILE_SIZE + 1):
            for x in range(SCREEN_WIDTH // TILE_SIZE + 1):
                map_x = x + cam_x
                map_y = y + cam_y
                if 0 <= map_x < len(tilemap[0]) and 0 <= map_y < len(tilemap):
                    tile_idx = tilemap[map_y][map_x]
                    screen.blit(tiles[tile_idx], (x * TILE_SIZE, y * TILE_SIZE))

        # --- DRAW BUILDINGS ---
        for b in buildings:
            bx, by = b['pos']
            sx = (bx - cam_x) * TILE_SIZE
            sy = (by - cam_y) * TILE_SIZE
            if 0 <= sx < SCREEN_WIDTH and 0 <= sy < SCREEN_HEIGHT:
                if sprites:
                    sprite_img = list(sprites.values())[0]
                    screen.blit(sprite_img, (sx, sy))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (sx, sy, TILE_SIZE, TILE_SIZE))

        # --- DRAW NPCS ---
        for npc in npcs:
            nx, ny = npc['pos']
            sx = (nx - cam_x) * TILE_SIZE
            sy = (ny - cam_y) * TILE_SIZE
            if 0 <= sx < SCREEN_WIDTH and 0 <= sy < SCREEN_HEIGHT:
                if len(sprites) > 1:
                    sprite_img = list(sprites.values())[1]
                    screen.blit(sprite_img, (sx, sy))
                else:
                    pygame.draw.circle(screen, (0, 255, 0), (sx + TILE_SIZE//2, sy + TILE_SIZE//2), TILE_SIZE//2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
