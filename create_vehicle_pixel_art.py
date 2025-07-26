from PIL import Image

# Vehicle pixel art definitions (simple 32x16 images)
def create_used_car():
    img = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
    pixels = img.load()
    # Body (gray)
    for x in range(2, 30):
        for y in range(7, 13):
            pixels[x, y] = (120, 120, 120, 255)
    # Windows (light blue)
    for x in range(8, 24):
        for y in range(8, 11):
            pixels[x, y] = (180, 220, 255, 255)
    # Wheels (black)
    for x in [6, 25]:
        for y in range(13, 16):
            pixels[x, y] = (30, 30, 30, 255)
    return img

def create_sedan():
    img = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
    pixels = img.load()
    # Body (blue)
    for x in range(2, 30):
        for y in range(7, 13):
            pixels[x, y] = (40, 80, 200, 255)
    # Windows (white)
    for x in range(10, 22):
        for y in range(8, 11):
            pixels[x, y] = (240, 240, 255, 255)
    # Wheels (black)
    for x in [7, 24]:
        for y in range(13, 16):
            pixels[x, y] = (30, 30, 30, 255)
    return img

def create_suv():
    img = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
    pixels = img.load()
    # Body (green)
    for x in range(2, 30):
        for y in range(6, 13):
            pixels[x, y] = (40, 160, 80, 255)
    # Windows (gray)
    for x in range(12, 20):
        for y in range(8, 11):
            pixels[x, y] = (180, 180, 180, 255)
    # Wheels (black)
    for x in [8, 22]:
        for y in range(13, 16):
            pixels[x, y] = (30, 30, 30, 255)
    return img

def save_vehicles():
    create_used_car().save('assets/vehicle_used_car.png')
    create_sedan().save('assets/vehicle_sedan.png')
    create_suv().save('assets/vehicle_suv.png')

if __name__ == '__main__':
    save_vehicles()

