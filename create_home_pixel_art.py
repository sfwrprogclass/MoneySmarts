from PIL import Image

def create_starter_home():
    img = Image.new('RGBA', (32, 24), (0, 0, 0, 0))
    pixels = img.load()
    # House body (light brown)
    for x in range(6, 26):
        for y in range(12, 22):
            pixels[x, y] = (200, 170, 120, 255)
    # Roof (red)
    for x in range(8, 24):
        for y in range(8, 12):
            pixels[x, y] = (180, 40, 40, 255)
    # Door (dark brown)
    for x in range(15, 19):
        for y in range(16, 22):
            pixels[x, y] = (120, 80, 40, 255)
    return img

def create_family_house():
    img = Image.new('RGBA', (32, 24), (0, 0, 0, 0))
    pixels = img.load()
    # House body (blue)
    for x in range(4, 28):
        for y in range(10, 22):
            pixels[x, y] = (100, 160, 220, 255)
    # Roof (dark gray)
    for x in range(6, 26):
        for y in range(6, 10):
            pixels[x, y] = (80, 80, 80, 255)
    # Door (white)
    for x in range(14, 18):
        for y in range(16, 22):
            pixels[x, y] = (240, 240, 240, 255)
    return img

def create_luxury_villa():
    img = Image.new('RGBA', (32, 24), (0, 0, 0, 0))
    pixels = img.load()
    # House body (cream)
    for x in range(2, 30):
        for y in range(8, 22):
            pixels[x, y] = (255, 240, 200, 255)
    # Roof (gold)
    for x in range(4, 28):
        for y in range(4, 8):
            pixels[x, y] = (220, 180, 60, 255)
    # Door (dark gray)
    for x in range(15, 19):
        for y in range(16, 22):
            pixels[x, y] = (80, 80, 80, 255)
    return img

def save_homes():
    create_starter_home().save('assets/home_starter.png')
    create_family_house().save('assets/home_family.png')
    create_luxury_villa().save('assets/home_luxury.png')

if __name__ == '__main__':
    save_homes()

