import os
import json
from moneySmarts.screens.overworld_screen import OverworldScreen
from moneySmarts.quest import QuestManager
from moneySmarts.image_manager import image_manager
# --- NEW IMPORTS FOR ASSET CONVERSION ---
from PIL import Image
from pydub import AudioSegment
import shutil

# Dummy game object for extraction (replace with actual game instance if needed)
class DummyGame:
    def __init__(self):
        self.screen = type('Screen', (), {'get_size': lambda self: (1280, 720)})()
        self.player = type('Player', (), {'bank_account': True, 'job': True, 'assets': [], 'cash': 1000, 'compute_net_worth': lambda self: 100000})()
        self.met_mentor = True
        self.quests = QuestManager(self)
        self.quest_notifications = []
        self.gui_manager = type('GUI', (), {'set_screen': lambda self, x: None, 'running': True})()

# Instantiate overworld screen to extract data
GAME = DummyGame()
overworld = OverworldScreen(GAME)

# Export buildings
buildings_data = [
    {
        'key': b.key,
        'display_name': b.display_name,
        'btype': b.btype,
        'pos': b.pos
    }
    for b in overworld.buildings
]

# Export NPCs
npcs_data = [
    {
        'type': npc['type'],
        'pos': npc['pos'],
        'met': npc.get('met', False)
    }
    for npc in overworld.npcs
]

# Export quests
quests_data = [
    {
        'id': q.id,
        'title': q.title,
        'description': q.description,
        'reward_cash': q.reward_cash
    }
    for q in GAME.quests.quests
]

# Export player start position
player_start = overworld.pos

# --- ASSET EXPORT LOGIC ---
EXPORT_ROOT = 'rpgmaker_export'
IMG_CHAR_DIR = os.path.join(EXPORT_ROOT, 'img', 'characters')
IMG_TILE_DIR = os.path.join(EXPORT_ROOT, 'img', 'tilesets')
AUDIO_BGM_DIR = os.path.join(EXPORT_ROOT, 'audio', 'bgm')
AUDIO_SE_DIR = os.path.join(EXPORT_ROOT, 'audio', 'se')

os.makedirs(IMG_CHAR_DIR, exist_ok=True)
os.makedirs(IMG_TILE_DIR, exist_ok=True)
os.makedirs(AUDIO_BGM_DIR, exist_ok=True)
os.makedirs(AUDIO_SE_DIR, exist_ok=True)

# --- IMAGE CONVERSION ---
IMG_SRC_ROOT = os.path.join(os.path.dirname(__file__), 'assets', 'images')
for root, dirs, files in os.walk(IMG_SRC_ROOT):
    for fname in files:
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(root, fname)
            try:
                img = Image.open(src_path)
                img = img.convert('RGBA')
                img_resized = img.resize((48, 48), Image.LANCZOS)
                # Export to both characters and tilesets for flexibility
                img_resized.save(os.path.join(IMG_CHAR_DIR, fname.split('.')[0] + '.png'))
                img_resized.save(os.path.join(IMG_TILE_DIR, fname.split('.')[0] + '.png'))
            except Exception as e:
                print(f'Error processing image {src_path}: {e}')

# --- AUDIO CONVERSION ---
AUDIO_SRC_ROOT = os.path.join(os.path.dirname(__file__), 'assets', 'audio')
for root, dirs, files in os.walk(AUDIO_SRC_ROOT):
    for fname in files:
        if fname.lower().endswith(('.wav', '.mp3', '.m4a')):
            src_path = os.path.join(root, fname)
            try:
                audio = AudioSegment.from_file(src_path)
                out_name = fname.split('.')[0] + '.ogg'
                # Export to both bgm and se for flexibility
                audio.export(os.path.join(AUDIO_BGM_DIR, out_name), format='ogg')
                audio.export(os.path.join(AUDIO_SE_DIR, out_name), format='ogg')
            except Exception as e:
                print(f'Error processing audio {src_path}: {e}')

# --- DATA EXPORT ---
with open(os.path.join(EXPORT_ROOT, 'buildings.json'), 'w') as f:
    json.dump(buildings_data, f, indent=2)
with open(os.path.join(EXPORT_ROOT, 'npcs.json'), 'w') as f:
    json.dump(npcs_data, f, indent=2)
with open(os.path.join(EXPORT_ROOT, 'quests.json'), 'w') as f:
    json.dump(quests_data, f, indent=2)
with open(os.path.join(EXPORT_ROOT, 'player_start.json'), 'w') as f:
    json.dump(player_start, f, indent=2)

print('Export complete! Data and assets saved to rpgmaker_export/')
print('\nIMPORT INSTRUCTIONS:')
print('1. Copy rpgmaker_export/img/characters and img/tilesets to your RPG Maker project.')
print('2. Copy rpgmaker_export/audio/bgm and audio/se to your RPG Maker project.')
print('3. Use the JSON files to manually recreate buildings, NPCs, and quests in RPG Maker.')
print('4. Set player start position using player_start.json.')
