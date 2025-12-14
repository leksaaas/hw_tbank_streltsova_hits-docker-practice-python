import sys
from pathlib import Path

# Добавляем корень проекта (папку на уровень выше tests/) в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
