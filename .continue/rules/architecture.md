# Project Architecture
This is a Python FastAPI backend application with the following key directories and files:

## Top level directories
- Application entrypoint and middleware in `itjob/app/main.py`
- Core configuration, database clients (Beanie/Motor), and utilities in `itjob/app/core/`
- MongoDB ODM models defined using Beanie in `itjob/app/models/`
- Data validation schemas defined using Pydantic in `itjob/app/schemas/`
- API endpoint handlers (business logic) grouped by feature in `itjob/app/api/endpoints/`
- Route definitions mapping paths to endpoints in `itjob/app/api/routers/`
- Reusable components and helpers in `itjob/app/utils/`




## Entrypoint
- `itjob/app/main.py`: The `FastAPI` instance creation, mounting routers, and startup logic.

## Core Setup (`itjob/app/core/`)
- `database.py`: Handles MongoDB connection using Motor and initializing Beanie ODM.
- `settings.py`: Manages environment variables and configurations using Pydantic `BaseSettings`.
- `dependencies.py`: Contains reusable FastAPI dependencies like current payload retrieval.
- `rolechecker.py`: Defines the `RoleChecker` dependency to enforce role-based access control on routes.
- `modules.py`: Helpers for setting up middleware and aggregating app routers.

## Data Models (`itjob/app/models/`)
- `user_model.py`: Beanie ODM document schema for `User`.
- `category_model.py`: Beanie ODM document schemas for `Category`, `SubCategory`, and `Topic`.
- `question_model.py`: Beanie ODM document schema for `Question`.

## Validation Schemas (`itjob/app/schemas/`)
- `common.py`: Shared Pydantic schemas (e.g., for standard responses and pagination).
- `user_schema.py`: Schemas for user creation, login, and responses.
- `category_schema.py`: Schemas for category, subcategory, and topic CRUD operations.
- `question_schema.py`: Schemas for question CRUD operations.

## APIs (`itjob/app/api/`)
- `endpoints/`: Grouped vertically by domain (e.g., `user/`, `category/`, `question/`). Each contains business logic implementations for endpoints (like `user_api.py` and `auth.py`).
- `routers/`: Aggregates the endpoints into routers (like `user_router.py`, `main_router.py`) and maps paths and tags.

## Shared Utilities (`itjob/app/utils/`)
- `env.py`: Helper script to load `.env` fallback.
- Helpers for hashing, token generation, etc., if applicable.
