# hw_tbank_streltsova_hits-docker-practice-python
Репозиторий с доработанным проектом hits-docker-practice (python) для ДЗ по использованию ИИ в разработке ПО
# Hospital Web App (Tornado + Redis)

Учебное веб-приложение на Python (Tornado), использующее Redis в качестве хранилища.
Проект разработан в рамках дисциплины «Базы данных» и демонстрирует
использование AI-ассистента для полного цикла доработки проекта:
юнит-тестирование, нагрузочное тестирование, документация, рефакторинг и CI/CD.

---

## Архитектура проекта

- **Tornado** — веб-сервер и HTTP-роутинг  
- **Redis** — key-value хранилище данных  
- **HTML templates** — пользовательский интерфейс  
- **Static files** — CSS и JavaScript  
- **/health endpoint** — проверка состояния сервиса (используется в тестах и нагрузке)

### Структура данных в Redis
- `hospital:{id}` — данные больницы  
- `doctor:{id}` — данные врача  
- `patient:{id}` — данные пациента  
- `diagnosis:{id}` — данные диагноза  
- `doctor-patient:{doctor_id}` — связь врач–пациент (set)

---

## Переменные окружения

- `REDIS_HOST` — адрес Redis (по умолчанию `localhost`)  
- `REDIS_PORT` — порт Redis (по умолчанию `6379`)  
- `PORT` — порт приложения (по умолчанию `8888`)  
- `DEBUG` — режим Tornado (`1` — debug, `0` — production)

---

## Локальный запуск

### 1) Установка и запуск Redis (macOS)
```bash
brew install redis
brew services start redis
redis-cli ping
```
Ожидается ответ PONG
# Hospital Web App (Tornado + Redis)

Учебное веб-приложение на Python (Tornado), использующее Redis в качестве хранилища.
Проект разработан в рамках дисциплины «Базы данных» и демонстрирует
использование AI-ассистента для полного цикла доработки проекта:
юнит-тестирование, нагрузочное тестирование, документация, рефакторинг и CI/CD.

---

## Архитектура проекта

- **Tornado** — веб-сервер и HTTP-роутинг  
- **Redis** — key-value хранилище данных  
- **HTML templates** — пользовательский интерфейс  
- **Static files** — CSS и JavaScript  
- **/health endpoint** — проверка состояния сервиса (используется в тестах и нагрузке)

### Структура данных в Redis
- `hospital:{id}` — данные больницы  
- `doctor:{id}` — данные врача  
- `patient:{id}` — данные пациента  
- `diagnosis:{id}` — данные диагноза  
- `doctor-patient:{doctor_id}` — связь врач–пациент (set)

---

## Переменные окружения

- `REDIS_HOST` — адрес Redis (по умолчанию `localhost`)  
- `REDIS_PORT` — порт Redis (по умолчанию `6379`)  
- `PORT` — порт приложения (по умолчанию `8888`)  
- `DEBUG` — режим Tornado (`1` — debug, `0` — production)

---

## Локальный запуск

### 1) Установка и запуск Redis (macOS)
```bash
brew install redis
brew services start redis
redis-cli ping
```
## Приложение будет доступно по адресам:
http://localhost:8888
http://localhost:8888/health

## HTTP эндпоинты
GET / — главная страница
GET /health — проверка состояния сервиса
GET/POST /hospital — просмотр и добавление больниц
GET/POST /doctor — просмотр и добавление врачей
GET/POST /patient — просмотр и добавление пациентов
GET/POST /diagnosis — просмотр и добавление диагнозов
GET/POST /doctor-patient — связь врач–пациент

## Юнит-тесты
Установка dev-зависимостей
```bash
pip3 install -r requirements.txt -r requirements-dev.txt
```
Запуск тестов
```bash
pytest
```
Запуск с покрытием
```bash
pytest --cov=
```
Для юнит-тестирования используется fakeredis, что позволяет запускать тесты
без необходимости поднимать реальный Redis.
## Нагрузочное тестирование
Инструмент
**Locust**
### Установка
```bash
pip3 install locust
```
### Запуск
Запустить приложение:
```bash
python3 main.py
```
Запустить Locust:
```bash
locust -f loadtest/locustfile.py --host http://localhost:8888
```
### Открыть веб-интерфейс:
http://localhost:8089
### Метрики нагрузочного тестирования берутся из вкладки Statistics
(строка Aggregated):
- Requests per second (RPS)
- 95th percentile latency (p95)
- Error rate
