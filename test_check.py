#!/usr/bin/env python3
"""Test script to verify all imports work"""
import sys
sys.path.insert(0, '.')

print("Testing imports...")

try:
    import main
    print("1. main.py - OK")
except Exception as e:
    print(f"1. main.py - ERROR: {e}")

try:
    import config
    print("2. config.py - OK")
except Exception as e:
    print(f"2. config.py - ERROR: {e}")

try:
    from bots import OzonBot, WildberriesBot
    print("3. bots - OK")
except Exception as e:
    print(f"3. bots - ERROR: {e}")

try:
    from api import OzonAPI, WBAPI
    print("4. api - OK")
except Exception as e:
    print(f"4. api - ERROR: {e}")

try:
    from gui import run_gui
    print("5. gui - OK")
except Exception as e:
    print(f"5. gui - ERROR: {e}")

try:
    from utils import logger, answer_generator
    print("6. utils - OK")
except Exception as e:
    print(f"6. utils - ERROR: {e}")

try:
    from config import config
    print(f"7. config values - min_stars: {config.get('general', 'min_stars')}, ozon.enabled: {config.get('ozon', 'enabled')}")
except Exception as e:
    print(f"7. config values - ERROR: {e}")

print("\nAll tests completed!")
