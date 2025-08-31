import importlib, traceback
modules = [
    'moneySmarts.constants',
    'moneySmarts.models',
    'moneySmarts.game',
    'moneySmarts.images',
    'moneySmarts.image_manager',
    'moneySmarts.sound_manager',
    'moneySmarts.ui',
    'moneySmarts.world_assets',
    'moneySmarts.screens.overworld_screen'
]
for m in modules:
    try:
        importlib.import_module(m)
        print(f"{m}: OK")
    except Exception as e:
        print(f"{m}: FAIL -> {e}")
        traceback.print_exc()
print('Done')

