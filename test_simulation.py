#!/usr/bin/env python3
"""
Симуляция работы бота для выявления ошибок
"""
import sys
import os
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("СИМУЛЯЦИЯ РАБОТЫ БОТА")
print("=" * 60)
print()

errors_found = []
warnings = []

# Тест 1: Импорт основных модулей
print("[1] Тест импорта основных модулей...")
try:
    from config import config
    print("    OK: config импортирован")
except Exception as e:
    errors_found.append(f"Ошибка импорта config: {e}")
    print(f"    ERROR: {e}")

try:
    from utils import logger, answer_generator
    print("    OK: utils импортирован")
except Exception as e:
    errors_found.append(f"Ошибка импорта utils: {e}")
    print(f"    ERROR: {e}")

try:
    from bots import OzonBot, WildberriesBot
    print("    OK: bots импортирован")
except Exception as e:
    errors_found.append(f"Ошибка импорта bots: {e}")
    print(f"    ERROR: {e}")

try:
    from api import OzonAPI, WBAPI
    print("    OK: api импортирован")
except Exception as e:
    errors_found.append(f"Ошибка импорта api: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 2: Проверка конфигурации
print("[2] Тест конфигурации...")
try:
    ozon_config = config.get("ozon")
    print(f"    Ozon enabled: {ozon_config.get('enabled')}")
    print(f"    Ozon api_key: {'*' * len(ozon_config.get('api_key', '')) if ozon_config.get('api_key') else 'EMPTY'}")
    print(f"    Ozon company_id: {'*' * len(ozon_config.get('company_id', '')) if ozon_config.get('company_id') else 'EMPTY'}")
except Exception as e:
    errors_found.append(f"Ошибка чтения конфигурации Ozon: {e}")
    print(f"    ERROR: {e}")

try:
    wb_config = config.get("wildberries")
    print(f"    WB enabled: {wb_config.get('enabled')}")
    print(f"    WB api_key: {'*' * len(wb_config.get('api_key', '')) if wb_config.get('api_key') else 'EMPTY'}")
except Exception as e:
    errors_found.append(f"Ошибка чтения конфигурации WB: {e}")
    print(f"    ERROR: {e}")

try:
    general = config.get("general")
    print(f"    check_interval: {general.get('check_interval')} мин")
    print(f"    min_stars: {general.get('min_stars')}")
    print(f"    max_answers_per_run: {general.get('max_answers_per_run')}")
    print(f"    short_sleep: {general.get('short_sleep')} сек")
except Exception as e:
    errors_found.append(f"Ошибка чтения общих настроек: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 3: Проверка генератора ответов
print("[3] Тест генератора ответов...")
try:
    templates = config.get_answer_templates()
    
    required_keys = ['greetings', 'gratitude', 'goodbye']
    for key in required_keys:
        if key not in templates:
            warnings.append(f"Отсутствует ключевой шаблон: {key}")
            print(f"    WARNING: Отсутствует шаблон '{key}'")
        else:
            print(f"    OK: Шаблон '{key}' найден, {len(templates[key])} вариантов")
    
    test_ratings = [5, 4, 3, 2, 1, 0]
    for rating in test_ratings:
        try:
            answer = answer_generator.generate(rating, has_comment=True)
            answer_no_comment = answer_generator.generate(rating, has_comment=False)
            if answer:
                print(f"    OK: Сгенерирован ответ для {rating} звезд (с комментарием)")
            else:
                errors_found.append(f"Пустой ответ для {rating} звезд")
                print(f"    ERROR: Пустой ответ для {rating} звезд")
        except Exception as e:
            errors_found.append(f"Ошибка генерации ответа для {rating} звезд: {e}")
            print(f"    ERROR при генерации {rating} зв.: {e}")
            
except Exception as e:
    errors_found.append(f"Ошибка генератора ответов: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 4: Проверка создания ботов
print("[4] Тест создания ботов...")
try:
    ozon_bot = OzonBot()
    print("    OK: OzonBot создан")
    print(f"    - is_running: {ozon_bot.is_running}")
except Exception as e:
    errors_found.append(f"Ошибка создания OzonBot: {e}")
    print(f"    ERROR: {e}")

try:
    wb_bot = WildberriesBot()
    print("    OK: WildberriesBot создан")
    print(f"    - is_running: {wb_bot.is_running}")
except Exception as e:
    errors_found.append(f"Ошибка создания WildberriesBot: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 5: Проверка статуса ботов
print("[5] Тест получения статуса ботов...")
try:
    status = ozon_bot.get_status()
    print(f"    OzonBot status: {status}")
except Exception as e:
    errors_found.append(f"Ошибка получения статуса OzonBot: {e}")
    print(f"    ERROR: {e}")

try:
    status = wb_bot.get_status()
    print(f"    WildberriesBot status: {status}")
except Exception as e:
    errors_found.append(f"Ошибка получения статуса WildberriesBot: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 6: Проверка API классов
print("[6] Тест API классов...")
try:
    print("    OK: Классы API импортированы корректно")
except Exception as e:
    errors_found.append(f"Ошибка теста API: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 7: Проверка логирования
print("[7] Тест логирования...")
try:
    test_message = f"Тестовое сообщение {datetime.now()}"
    logger.info(test_message)
    recent = logger.get_recent_messages()
    if recent and test_message in recent[-1]:
        print("    OK: Логирование работает")
    else:
        warnings.append("Логирование может работать неправильно")
        print("    WARNING: Не удалось проверить логи")
except Exception as e:
    errors_found.append(f"Ошибка логирования: {e}")
    print(f"    ERROR: {e}")

print()

# Тест 8: Проверка настроек
print("[8] Проверка настроек...")
try:
    general = config.get("general")
    
    interval = general.get("check_interval", 0)
    if interval < 1:
        warnings.append("Интервал проверки меньше 1 минуты")
        print(f"    WARNING: Интервал слишком маленький: {interval} мин")
    else:
        print(f"    OK: Интервал проверки: {interval} мин")
    
    min_stars = general.get("min_stars", 0)
    if min_stars < 1:
        warnings.append("min_stars меньше 1 - будут обрабатываться отзывы с 0 звезд")
        print(f"    WARNING: min_stars = {min_stars} (может быть слишком низким)")
    else:
        print(f"    OK: min_stars = {min_stars}")
        
    short_sleep = general.get("short_sleep", 0)
    if short_sleep < 0.1:
        warnings.append("short_sleep слишком маленький - возможны ошибки API")
        print(f"    WARNING: short_sleep = {short_sleep} сек (может быть слишком низким)")
    else:
        print(f"    OK: short_sleep = {short_sleep} сек")
        
except Exception as e:
    errors_found.append(f"Ошибка проверки настроек: {e}")
    print(f"    ERROR: {e}")

print()
print("=" * 60)
print("РЕЗУЛЬТАТЫ СИМУЛЯЦИИ")
print("=" * 60)
print()

if errors_found:
    print(f"НАЙДЕНО ОШИБОК: {len(errors_found)}")
    for i, err in enumerate(errors_found, 1):
        print(f"  {i}. {err}")
    print()

if warnings:
    print(f"ПРЕДУПРЕЖДЕНИЙ: {len(warnings)}")
    for i, warn in enumerate(warnings, 1):
        print(f"  {i}. {warn}")
    print()

if not errors_found and not warnings:
    print("Все тесты пройдены успешно! Ошибок не найдено.")
elif not errors_found:
    print("Критических ошибок нет. Есть только предупреждения.")
else:
    print("НАЙДЕНЫ КРИТИЧЕСКИЕ ОШИБКИ - требуется исправление!")

print()
print("=" * 60)

result_file = os.path.join("logs", f"simulation_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt")
try:
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ СИМУЛЯЦИИ РАБОТЫ БОТА\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Время: {datetime.now()}\n\n")
        
        f.write(f"ОШИБКИ: {len(errors_found)}\n")
        for i, err in enumerate(errors_found, 1):
            f.write(f"  {i}. {err}\n")
        
        f.write(f"\nПРЕДУПРЕЖДЕНИЯ: {len(warnings)}\n")
        for i, warn in enumerate(warnings, 1):
            f.write(f"  {i}. {warn}\n")
    
    print(f"Результаты сохранены в: {result_file}")
except Exception as e:
    print(f"Не удалось сохранить результаты: {e}")

