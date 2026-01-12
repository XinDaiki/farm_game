#!/usr/bin/env python3
"""
Asset Loading Test Script
Tests if all sprites are loading correctly from the assets folder.
"""

import pygame
import sys

pygame.init()

# Import asset manager
from asset_manager import asset_manager

print("\n" + "=" * 60)
print("ASSET LOADING TEST")
print("=" * 60)

# Test tile sprites
print("\n📦 Testing Tile Sprites:")
tiles = ["G", "S", "W", "P", "T", "F", "R"]
for tile in tiles:
    sprite = asset_manager.get_tile_sprite(tile)
    if sprite:
        print(f"  ✓ {tile} tile: {sprite.get_size()}")
    else:
        print(f"  ✗ {tile} tile: Failed to load")

# Test crop sprites
print("\n🌱 Testing Crop Sprites:")
crops = ["wheat", "carrot", "tomato", "corn"]
for crop in crops:
    sprites = asset_manager.get_crop_sprites(crop)
    if sprites:
        print(f"  ✓ {crop}: {len(sprites)} growth stages loaded")
    else:
        print(f"  ⚠ {crop}: Using fallback graphics")

# Test character sprite
print("\n👤 Testing Character Sprites:")
player = asset_manager.get_character_sprite("player")
if player:
    print(f"  ✓ Player: {player.get_size()}")
else:
    print(f"  ⚠ Player: Using fallback graphics")

# Test animal sprites
print("\n🐓 Testing Animal Sprites:")
animals = ["chicken", "cow"]
for animal in animals:
    sprite = asset_manager.get_animal_sprite(animal)
    if sprite:
        print(f"  ✓ {animal.title()}: {sprite.get_size()}")
    else:
        print(f"  ⚠ {animal.title()}: Using fallback graphics")

# Summary
print("\n" + "=" * 60)
if asset_manager.assets_available:
    print("✅ ASSETS LOADED SUCCESSFULLY!")
    print("   The game will use real pixel art sprites!")
else:
    print("⚠️  NO ASSETS FOUND")
    print("   The game will use procedural graphics.")
print("=" * 60)

print("\n💡 Tip: Run 'python main.py' to start the game!")
print()

pygame.quit()
sys.exit(0)
