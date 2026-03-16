#!/usr/bin/env python3
"""
Тест для проверки работоспособности всех модулей проекта
"""
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Тест всех импортов"""
    print("=" * 50)
    print("ТЕСТ ИМПОРТОВ")
    print("=" * 50)
    
    errors = []
    
    # Тест импорта config
    try:
        from config import config
        print("[OK] config")
    except Exception as e:
        errors.append(f"config: {e}")
        print(f"[ERROR] config: {e}")
    
    # Тест импорта utils
    try:
        from utils.logger import logger
        from utils.answers import answer_generator
        print("[OK] utils (logger, answer_generator)")
    except Exception as e:
        errors.append(f"utils: {e}")
        print(f"[ERROR] utils: {e}")
    
    # Тест импорта bots
    try:
        from bots import OzonBot, WildberriesBot
        print("[OK] bots (OzonBot, WildberriesBot)")
    except Exception as e:
        errors.append(f"bots: {e}")
        print(f"[ERROR] bots: {e}")
    
    # Тест импорта api
    try:
        from api import OzonAPI, WBAPI
        print("[OK] api (OzonAPI, WBAPI)")
    except Exception as e:
        errors.append(f"api: {e}")
        print(f"[ERROR] api: {e}")
    
    # Тест импорта gui
    try:
        from gui import run_gui
        print("[OK] gui (run_gui)")
    except Exception as e:
        errors.append(f"gui: {e}")
        print(f"[ERROR] gui: {e}")
    
    return errors


def test_config():
    """Тест конфигурации"""
    print("\n" + "=" * 50)
    print("ТЕСТ КОНФИГУРАЦИИ")
    print("=" * 50)
    
    from config import config
    errors = []
    
    try:
        ozon = config.get("ozon")
        print(f"[OK] Ozon enabled: {ozon.get('enabled')}")
        
        wb = config.get("wildberries")
        print(f"[OK] WB enabled: {wb.get('enabled')}")
        
        general = config.get("general")
        print(f"[OK] check_interval: {general.get('check_interval')} мин")
        print(f"[OK] min_stars: {general.get('min_stars')}")
        
    except Exception as e:
        errors.append(f"config: {e}")
        print(f"[ERROR] {e}")
    
    return errors


def test_answer_generator():
    """Тест генератора ответов"""
    print("\n" + "=" * 50)
    print("ТЕСТ ГЕНЕРАТОРА ОТВЕТОВ")
    print("=" * 50)
    
    from utils import answer_generator
    errors = []
    
    for rating in [5, 4, 3, 2, 1]:
        try:
            answer = answer_generator.generate(rating, has_comment=True)
            if answer and len(answer) > 0:
                print(f"[OK] {rating} stars: {answer[:50]}...")
            else:
                errors.append(f"Пустой ответ для {rating} звезд")
                print(f"[ERROR] Пустой ответ для {rating} звезд")
        except Exception as e:
            errors.append(f"Ошибка генерации для {rating} зв.: {e}")
            print(f"[ERROR] {rating} stars: {e}")
    
    return errors


def test_bots():
    """Тест создания ботов"""
    print("\n" + "=" * 50)
    print("ТЕСТ СОЗДАНИЯ БОТОВ")
    print("=" * 50)
    
    from bots import OzonBot, WildberriesBot
    errors = []
    
    try:
        ozon = OzonBot()
        print(f"[OK] OzonBot создан, is_running={ozon.is_running}")
    except Exception as e:
        errors.append(f"OzonBot: {e}")
        print(f"[ERROR] OzonBot: {e}")
    
    try:
        wb = WildberriesBot()
        print(f"[OK] WildberriesBot создан, is_running={wb.is_running}")
    except Exception as e:
        errors.append(f"WildberriesBot: {e}")
        print(f"[ERROR] WildberriesBot: {e}")
    
    return errors


def main():
    """Главная функция"""
    print("\n" + "#" * 50)
    print("# ТЕСТ РАБОТОСПОСОБНОСТИ ПРОЕКТА")
    print("#" * 50 + "\n")
    
    all_errors = []
    
    all_errors.extend(test_imports())
    all_errors.extend(test_config())
    all_errors.extend(test_answer_generator())
    all_errors.extend(test_bots())
    
    print("\n" + "=" * 50)
    print("ИТОГИ")
    print("=" * 50)
    
    if all_errors:
        print(f"\nНАЙДЕНО ОШИБОК: {len(all_errors)}")
        for i, err in enumerate(all_errors, 1):
            print(f"  {i}. {err}")
        print("\n[FAILED] Тест не пройден!")
        return 1
    else:
        print("\n[SUCCESS] Все тесты пройдены успешно!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
