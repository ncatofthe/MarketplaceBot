# MarketplaceBot 🛒🤖 - Полное руководство

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-PASS-brightgreen.svg)](test_all.py)

**Автоматический бот для ответов на отзывы Ozon & Wildberries.**  
GUI, templates по звездам (1⭐ извините → 5⭐ спасибо), детальные логи, EXE.

## 📋 Содержание
- [Что делает](#-что-делает)
- [Требования](#-требования)
- [Запуск по ОС](#-запуск-по-ос)
- [Настройка API](#-настройка-api)
- [GUI](#-gui)
- [Файлы проекта](#-файлы-проекта)
- [Кастомизация](#-кастомизация)
- [Тесты](#-тесты)
- [Ошибки](#-ошибки)
- [Build EXE](#-build-exe)

## 🎯 Что делает бот (шаг за шагом)

1. **Каждые 60мин** (настройка) → API check **неотвеченных** (UNPROCESSED)
2. **Fetch**: ID, rating (1-5), text (Ozon pagination 100+/page)
3. **Parse**: raw rating from API → bot rating
4. **Generate**: random from templates `"1": ["Извините...", "Нам жаль..."]`
5. **Log**: `"Raw=1 type=int → extracted=1 → 'Извините...' sent ID=abc"`
6. **Send** + mark PROCESSED

**Пример лога:**
```
Ozon ID=abc: Raw rating=1 (int), extracted=1, keys=['rating','text']
OzonBot: Отзыв abc (1⭐, comment=True): 'Нам жаль за 1⭐. Извините. Свяжитесь...'
Sent OK
```

## 📥 Требования

| OS | Python | Другое |
|-----|--------|--------|
| **Windows** | 3.8+ | - |
| **Linux/Mac** | 3.8+ | tkinter (`sudo apt install python3-tk`) |

**Зависимости** (`pip install -r requirements.txt`):
- `requests` - API calls
- `pycryptodome` - WB auth
- `tkinter` - GUI (built-in)

## 🚀 Запуск по ОС (подробно)

### **Windows (EXE - проще)**

1. Скачайте `dist/MarketplaceBot.exe` (Releases)
2. **Двойной клик** → GUI открывается
3. Если не запускается → антивирус whitelist or `python main.py`

### **Windows (Python)**

1. **Скачать Python**: [python.org/downloads/windows](https://www.python.org/downloads/windows) → "Add to PATH" → Install
2. **Открыть CMD**: Win+R → `cmd`
3. **Clone**:
```cmd
git clone https://github.com/gzhiharev/MarketplaceBot.git
cd MarketplaceBot
```
4. **Deps**:
```cmd
pip install -r requirements.txt
```
5. **Запуск**:
```cmd
python main.py
```

### **Linux (Ubuntu/Debian)**

1. **Python + tkinter**:
```bash
sudo apt update
sudo apt install python3.8 python3-pip python3-tk git
```
2. **Clone/deps/run**:
```bash
git clone https://github.com/gzhiharev/MarketplaceBot.git
cd MarketplaceBot
pip3 install -r requirements.txt
python3 main.py
```

### **macOS**

1. **Homebrew + Python**:
```bash
brew install python git
```
2. **Clone/deps/run** (same as Linux):
```bash
git clone https://github.com/gzhiharev/MarketplaceBot.git
cd MarketplaceBot
pip3 install -r requirements.txt
python3 main.py
```

## 🔑 Настройка API (5 мин)

### **Ozon API**
1. [seller.ozon.ru](https://seller.ozon.ru) → **Settings → API Keys → Create**
2. Permissions: **Reviews** (read/write)
3. Copy **API Key** (UUID), **Client ID** → GUI Settings/Ozon

### **Wildberries API**
1. [seller.wb.ru](https://seller.wb.ru) → **Settings → Access to API → Create**
2. Copy **Token** → GUI Settings/WB

**Test**: GUI Start → Logs "Connect OK"

## 📱 GUI Полное руководство

```
[Settings] ← API keys, min_stars=1 (answer 1*), interval=60min → Save → Start bots
[Templates] ← JSON edit "1": ["Извините..."] → Save
[Logs] ← Live "Raw rating=3 → answer sent"
[Status] ← Bots running?
```

## 📁 Файлы проекта (подробно)

### **Запуск**
| Файл | Что делает | Изменять? |
|------|------------|-----------|
| `main.py` | `run_gui()` | No |
| `gui/main_window.py` | 4 tabs | GUI custom |

### **Конфиг**
| Файл | Что | Edit |
|------|----|------|
| `config.py` | Load/save config.json | No |
| `settings/config.json` | Keys/interval (gitignore) | **Yes** notepad++/VSCode |

### **API & Bots**
| Файл | API/Bot | Custom |
|------|---------|--------|
| `api/ozon_api.py` | Ozon v1/review pagination/info | Advanced |
| `api/wb_api.py` | WB feedbacks | Advanced |
| `bots/base_bot.py` | Loop + **logs rating→answer** | Logs custom |
| `bots/ozon_bot.py` | Ozon connect | No |
| `bots/wildberries_bot.py` | WB | No |

### **Utils**
| Файл | Что | Custom |
|------|----|--------|
| `utils/logger.py` | Logs console/GUI/files | Level |
| `utils/answers.py` | **Templates 1-5*** | **JSON** |

### **Тесты (подробно)**
| Команда | Что проверяет | Output |
|---------|--------------|--------|
| `python test_all.py` | Imports/config/templates/bots | **[SUCCESS]** |
| `python test_ozon_full.py` | Ozon full cycle | Logs 163 sent |
| `python test_ozon.py` | Fetch | "Found N reviews" |
| `test_check.py` | Quick imports | OK 1-7 |

**Как смотреть:** CMD/PowerShell → copy logs/*.log → Notepad++/VSCode.

### **Build/Docs**
| Файл | Что | Run |
|------|----|-----|
| `build.bat` | EXE | `build.bat` |
| `.spec` | PyInstaller config | pyinstaller .spec |
| CHANGELOG/ИНСТРУКЦИЯ etc | History/RU guide | Read |

## 🎛️ Кастомизация (пошагово)

### **1. Шаблоны (тексты ответов)**
```
GUI → Templates → Edit:
{
  "1": ["Нам жаль 1⭐. Извините!", "Спасибо за отзыв. Разберёмся."],
  "5": ["Спасибо 5⭐!", "Рады!"]
}
→ Save → Restart bots
```
**Файл**: `settings/answers.json` (VSCode/Notepad)

### **2. Настройки**
`settings/config.json` (VSCode):
```json
{
  "ozon": {"enabled":true, "api_key":"uuid", "company_id":"123"},
  "general": {"min_stars":1, "interval":30}
}
```
Reload GUI.

### **3. Логи уровень**
`config.json "log_level":"DEBUG"` → more info.

## 🚨 Работа с ошибками (пошагово)

### **1. GUI Logs** (live)
- Open Logs tab → see "Raw rating error" or "API 403"

### **2. Files**
```
notepad logs/2026-03-16-14-06-49.log
# or VSCode logs/*.log
```
Search "ERROR" "WARNING".

### **3. Common**
| Log | Fix |
|----|-----|
| "API key invalid" | New keys seller.ozon.ru |
| "No reviews" | min_stars too high or all PROCESSED |
| "403 antibot" | Sleeps/retry OK |
| "ImportError" | `pip install -r requirements.txt` |

**Full**: ИНСТРУКЦИЯ_ПО_ОШИБКАМ.md

## 🧪 Тесты (почему/как)

**Зачем**: Verify before/after custom.
```
cd MarketplaceBot
python test_all.py  # [SUCCESS] = OK
```
**test_ozon_full.py**: Real API call → logs ratings/answers → **Sent!**

## 🔨 EXE (Windows)
```
build.bat  # 30s → dist/MarketplaceBot.exe ready
```
Distribute EXE - no Python needed!

## 📄 Лицензия & Support
MIT - use/fork.

**Issues** on GitHub 🚀
