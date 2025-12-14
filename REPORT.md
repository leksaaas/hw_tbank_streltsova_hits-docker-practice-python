# Отчёт по заданию: полный цикл доработки проекта с AI

Проект: Tornado + Redis веб-приложение (учебная лабораторная по БД).  
Цель: улучшить проект с помощью AI на всех этапах (тесты, нагрузка, документация, рефакторинг, CI/CD).

---

## 1) Использованные инструменты / модели

- ChatGPT (LLM): генерация unit-тестов, помощь с запуском, рефакторинг `main.py`, подготовка структуры файлов.
- IDE/инструменты:  terminal, pip, pytest.

---

## 2) Промпты, которые использовались

1. «Сгенерируй юнит-тесты на pytest для Tornado-приложения, которое использует Redis и имеет эндпоинты: /, /hospital, /doctor, /patient, /diagnosis, /doctor-patient».
2. «Предложи минимальный рефакторинг, чтобы Redis можно было подменять в тестах (dependency injection), и добавь /health endpoint».
3. «Объясни пошагово, как запускать приложение и тесты, какие файлы создать и куда положить».

---

## 3) Юнит-тесты

### Что было сделано
- Добавлен файл `requirements-dev.txt` с зависимостями для тестирования.
- Изменен исходный файл `requirements.txt` из-за конфликта версий при запуске с консоли.
- Создана папка `tests/` и тестовый файл `tests/test_handlers.py`.
- Для тестов Redis заменён на `fakeredis` (чтобы тесты не требовали реальный Redis).
- В проекте выполнен минимальный рефакторинг:
  - добавлена возможность передавать Redis-клиент в `make_app(...)`,
  - добавлен endpoint `GET /health`,
  - улучшена обработка autoID и ошибок Redis.

### Команды запуска
Установка зависимостей:
```bash
pip3 install -r requirements.txt -r requirements-dev.txt

Запуск тестов:
pytest
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/a.v.streltsova/Documents/Projects/hw_tbank_streltsova_hits-docker-practice-python
plugins: cov-6.0.0, anyio-4.7.0
collected 7 items                                                              

tests/test_handlers.py .......                                           [100%]

=============================== warnings summary ===============================
tests/test_handlers.py::TestHandlers::test_diagnosis_requires_existing_patient
tests/test_handlers.py::TestHandlers::test_doctor_rejects_unknown_hospital_id
tests/test_handlers.py::TestHandlers::test_health_ok
tests/test_handlers.py::TestHandlers::test_hospital_create_ok
tests/test_handlers.py::TestHandlers::test_hospital_validation
tests/test_handlers.py::TestHandlers::test_patient_sex_validation
tests/test_handlers.py::TestHandlers::test_root_ok
  /opt/anaconda3/lib/python3.13/site-packages/fakeredis/_connection.py:144: DeprecationWarning: Call to '__init__' function with deprecated usage of input argument/s 'retry_on_timeout'. (TimeoutError is included by default.) -- Deprecated since version 6.0.0.
    super().__init__(**kwds)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 7 passed, 7 warnings in 1.00s =========================
(base) a.v.streltsova@macbook-GJTXH6TK7C hw_tbank_streltsova_hits-docker-practice-python %
Warning DeprecationWarning от fakeredis не влияет на прохождение тестов (не является ошибкой).
```
## 4) Нагрузочное тестирование

### Инструмент
- Locust

### Сценарий
- GET /health
- GET /hospital, /doctor, /patient, /diagnosis
- POST /hospital
- POST /patient

Сценарий описан в файле `loadtest/locustfile.py`.

### Параметры запуска
- Number of users: 50
- Spawn rate: 5 users/sec
- Duration: ~9 minutes

### Результаты
- Requests per second (RPS): ~32.8
- 95th percentile latency (p95): ~1800 ms
- Error rate: 0%
### Скриншоты
Результаты нагрузочного тестирования представлены на скриншоте:

![Locust results](screen_locust.png)
### Вывод
Приложение стабильно обрабатывает нагрузку,
ошибок не обнаружено, задержки находятся в допустимых пределах
для учебного проекта.
