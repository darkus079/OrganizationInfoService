# OrganizationInfoService

REST API приложения для справочника организаций, зданий и деятельностей.

Стек: `FastAPI + Pydantic + SQLAlchemy + Alembic + PostgreSQL`.

## API-документация

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Все бизнес-методы требуют заголовок:

- `X-API-Key: <ваш_ключ>`

## Переменные окружения

Пример находится в файле `.env.example`:

- `APP_NAME`
- `API_V1_PREFIX`
- `API_KEY`
- `DATABASE_URL`

## Запуск через Docker

1. Создайте `.env` на основе `.env.example`.
2. Запустите:

```bash
docker compose up --build
```

При старте API-контейнера автоматически выполняется:

```bash
alembic upgrade head
```

После запуска приложение доступно на `http://localhost:8000`.

## Локальный запуск (без Docker)

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Создайте `.env` на основе `.env.example` и укажите `DATABASE_URL`.

3. Примените миграции:

```bash
alembic upgrade head
```

4. Запустите API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Реализованные методы API

Базовый префикс: `/api/v1`.

### Buildings

- `GET /buildings`  
  Список зданий.
- `GET /buildings/{building_id}/organizations`  
  Список организаций в конкретном здании.

### Organizations

- `GET /organizations/{organization_id}`  
  Информация об организации по идентификатору.
- `GET /organizations/search/by-name?name=...`  
  Поиск организаций по названию.
- `GET /organizations/search/by-radius?latitude=...&longitude=...&radius_km=...`  
  Поиск организаций в радиусе от точки.
- `GET /organizations/search/by-area?min_latitude=...&max_latitude=...&min_longitude=...&max_longitude=...`  
  Поиск организаций в прямоугольной области.

### Activities

- `GET /activities/{activity_id}/organizations`  
  Список организаций по указанному виду деятельности.
- `GET /activities/{activity_id}/organizations/with-children`  
  Поиск по виду деятельности с включением дочерних узлов дерева (ограничение глубины: 3 уровня).

## Примеры запросов

### Получить список зданий

```bash
curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: change-me"
```

### Поиск организаций по названию

```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search/by-name?name=Рога" \
  -H "X-API-Key: change-me"
```

### Поиск организаций в радиусе

```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search/by-radius?latitude=55.75&longitude=37.61&radius_km=5" \
  -H "X-API-Key: change-me"
```

### Поиск организаций по деятельности с дочерними узлами

```bash
curl -X GET "http://localhost:8000/api/v1/activities/1/organizations/with-children" \
  -H "X-API-Key: change-me"
```