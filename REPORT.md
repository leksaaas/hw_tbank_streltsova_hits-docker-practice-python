# Отчёт по заданию: полный цикл доработки проекта с AI

Проект: Tornado + Redis веб-приложение (учебная лабораторная по БД).  
Цель: улучшить проект с помощью AI на всех этапах (тесты, нагрузка, документация, рефакторинг, CI/CD).

---

## 1) Использованные инструменты / модели

- ChatGPT (LLM): генерация unit-тестов, помощь с запуском, рефакторинг `main.py`, подготовка структуры файлов.
- IDE/инструменты:  terminal, pip, pytest.

---

## 2) Основные использованные промпты

1. Анализ проекта  
«Проанализируй Tornado + Redis проект, опиши архитектуру,
основные сущности и возможные улучшения».

2. Юнит-тесты  
«Сгенерируй pytest-тесты для Tornado-приложения
с использованием AsyncHTTPTestCase и fakeredis.
Проверь healthcheck, валидацию данных и обработку ошибок».

3. Отладка тестов  
«Почему pytest не видит main.py и как исправить ошибки
AsyncHTTPTestCase и импорта приложения?»

4. Нагрузочное тестирование  
«Сгенерируй Locust-сценарий для Tornado-приложения
и объясни, какие метрики (RPS, latency, error rate) нужно собрать».

5. Интерпретация результатов  
«Откуда брать RPS и latency в Locust
и как корректно описать результаты в отчёте?»

6. Документация  
«Сгенерируй README.md с описанием архитектуры,
запуска, эндпоинтов и тестирования проекта».

7. Рефакторинг  
«Предложи минимальный рефакторинг Tornado-приложения
без изменения бизнес-логики для повышения тестируемости».

8. Docker  
«Сгенерируй Dockerfile и docker-compose.yml
для запуска Tornado-приложения с Redis».

9. CI/CD  
«Сгенерируй GitHub Actions workflow
для запуска pytest и сборки Docker-образа».

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
## Docker и контейнеризация

### Что сделано
- Добавлен `Dockerfile` для сборки образа приложения.
- Добавлен `.dockerignore` для исключения лишних файлов из build context.
- Добавлен `docker-compose.yml` для запуска связки `app + redis`.

### Как запускалось
```bash
docker compose up --build
```
Все собралось локально через терминал:
```bash
(base) a.v.streltsova@macbook-GJTXH6TK7C hw_tbank_streltsova_hits-docker-practice-python % docker compose pull
docker compose up --build
[+] Pulling 7/12
 ✔ app Skipped - No image to be pulled                                     0.0s 
 ⠇ redis [⣿⠀⠀⠀⣿⣿⠀⣿⣿⣿] Pulling                                              4.8s 
   ✔ e43997775f51 Download complete                                        0.7s 
   ⠙ c2fe130f4aab Pulling fs layer                                         1.1s 
   ⠙ a4cd490265be Pulling fs layer                                         1.1s 
   ⠙ b3c1bc2ae482 Downloading      1.049MB/12.5...                         1.1s 
   ✔ f644b71be12e Download complete                                        0.8s 
   ✔ cda2dfd82503 Download complete                                        0.9s 
   ⠙ ea7069ec8986 Pulling fs layer                                         1.1s 
   ✔ 4f4fb700ef54 Download complete                                        0.8s 
   ✔ dcb2e590091c Download complete                                        0.0s 
   ✔ 2f459f3b393e Download complete                                        0.0s 
unknown: failed to copy: httpReadSeeker: failed open: unexpected status from GET request to https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com/registry-v2/docker/registry/v2/blobs/sha256/a4/a4cd490265becb809d7ebc53c74d921d04612e0dc6f62c49349f8e602ce8a121/data?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=f1baa2dd9b876aeb89efebbfc9e5d5f4%2F20251214%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20251214T202916Z&X-Amz-Expires=1200&X-Amz-SignedHeaders=host&X-Amz-Signature=de46c090b541c2d3a2051fd9ce88421daaf2cb45a26f16f140b322c1124ffe9b: 503 Service Unavailable
[+] Running 11/11
 ✔ redis Pulled                                                            7.7s 
   ✔ e43997775f51 Pull complete                                            0.8s 
   ✔ a4cd490265be Pull complete                                            2.4s 
   ✔ b3c1bc2ae482 Pull complete                                            4.4s 
   ✔ f644b71be12e Pull complete                                            0.7s 
   ✔ cda2dfd82503 Pull complete                                            0.6s 
   ✔ ea7069ec8986 Pull complete                                            1.3s 
   ✔ 4f4fb700ef54 Pull complete                                            0.8s 
   ✔ c2fe130f4aab Pull complete                                            2.0s 
   ✔ 2f459f3b393e Download complete                                        0.0s 
   ✔ dcb2e590091c Download complete                                        0.0s 
[+] Building 25.5s (14/14) FINISHED                                             
 => [internal] load local bake definitions                                 0.0s
 => => reading from stdin 697B                                             0.0s
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 783B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim        2.2s
 => [auth] library/python:pull token for registry-1.docker.io              0.0s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 160B                                          0.0s
 => [1/6] FROM docker.io/library/python:3.13-slim@sha256:baf66684c5fcafbd  0.0s
 => => resolve docker.io/library/python:3.13-slim@sha256:baf66684c5fcafbd  0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 138.06kB                                      0.0s
 => [2/6] WORKDIR /app                                                     0.1s
 => [3/6] RUN apt-get update && apt-get install -y --no-install-recommend  4.6s
 => [4/6] COPY requirements.txt .                                          0.0s
 => [5/6] RUN python -m pip install --upgrade pip &&     pip install --n  17.7s
 => [6/6] COPY . .                                                         0.0s 
 => exporting to image                                                     0.5s 
 => => exporting layers                                                    0.4s 
 => => exporting manifest sha256:a2cc2f0f79b400f37afed26a75de2ad940481ce8  0.0s 
 => => exporting config sha256:4665ddf4578401e236bf26498b43c8fccfe244f73f  0.0s 
 => => exporting attestation manifest sha256:7033f2a10af849affec0ce91e11d  0.0s 
 => => exporting manifest list sha256:2e084c37a31d86ddd81801768ca2d87ba86  0.0s
 => => naming to docker.io/library/hw_tbank_streltsova_hits-docker-practi  0.0s
 => => unpacking to docker.io/library/hw_tbank_streltsova_hits-docker-pra  0.1s
 => resolving provenance for metadata file                                 0.0s
[+] Running 2/3
 ✔ hw_tbank_streltsova_hits-docker-practice-python-app                Built0.0s 
[+] Running 4/4bank_streltsova_hits-docker-practice-python_default    Created0.0 ✔ hw_tbank_streltsova_hits-docker-practice-python-app                Built0.0s 
 ✔ Network hw_tbank_streltsova_hits-docker-practice-python_default    Created0.0s  
 ✔ Container hw_tbank_streltsova_hits-docker-practice-python-redis-1  Created0.0s 
 ✔ Container hw_tbank_streltsova_hits-docker-practice-python-app-1    Created0.0s 
Attaching to app-1, redis-1
redis-1  | 1:C 14 Dec 2025 20:29:51.033 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-1  | 1:C 14 Dec 2025 20:29:51.033 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-1  | 1:C 14 Dec 2025 20:29:51.033 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis-1  | 1:M 14 Dec 2025 20:29:51.034 * monotonic clock: POSIX clock_gettime
redis-1  | 1:M 14 Dec 2025 20:29:51.034 * Running mode=standalone, port=6379.
redis-1  | 1:M 14 Dec 2025 20:29:51.034 * Server initialized
redis-1  | 1:M 14 Dec 2025 20:29:51.034 * Ready to accept connections tcp
app-1    | INFO:root:Listening on 8888
app-1    | INFO:tornado.access:200 GET /health (151.101.64.223) 4.37ms
app-1    | INFO:tornado.access:304 GET /health (151.101.64.223) 0.47ms


v View in Docker Desktop   o View Config   w Enable Watch
```
## После сборки докера
Можно запустить сайт и потыкать кнопочки
![Locust results](screen_app.png)
