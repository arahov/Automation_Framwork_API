# Complete Implementation Guide

## 1. Introduction
This guide details the implementation of the Python API Automation Framework. The framework is built to test the GoRest API but is designed to be easily adaptable for any RESTful service.

## 2. Tech Stack
-   **Language**: Python 3.x
-   **Test Runner**: Pytest 9.x
-   **HTTP Client**: Requests
-   **Reporting**: Pytest-HTML
-   **Config**: Python-Dotenv

## 3. Directory Structure
```text
Automation_Framework_API/
├── core/
│   ├── __init__.py
│   └── api_client.py       # wrapper for requests.Session
├── services/
│   ├── __init__.py
│   └── user_service.py     # Domain logic for /users endpoint
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Fixtures (auth_token, user_service)
│   ├── test_users.py       # Core business logic tests
│   └── test_users_edge.py  # Edge case & negative tests
├── data/
│   ├── __init__.py
│   └── user_payloads.py    # Data generation utilities
├── logs/                   # Log files directory
├── reports/                # HTML reports directory
├── .env                    # Secrets (GOREST_TOKEN)
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
└── README.md               # Quickstart guide
```

## 4. Implementation Details

### Core Layer (`core/`)
The `APIClient` class in `core/api_client.py` is the foundation.
-   **Session Management**: Uses `requests.Session()` to persist headers (Authorization, Content-Type) across requests.
-   **Logging**: Intercepts every request and response to log details (Method, URL, Payload, Status, Body) using the standard `logging` library.

### Service Layer (`services/`)
The `UserService` in `services/user_service.py` extends `APIClient`.
-   **Abstraction**: Exposes methods like `create_user`, `get_user`, rather than raw HTTP calls.
-   **Flexibility**: Accepts data dictionaries to construct payloads dynamically.

### Test Layer (`tests/`)
Tests are split into `test_users.py` (Functional) and `test_users_edge.py` (Edge Cases).
-   **Fixtures**: `conftest.py` provides the `user_service` instance to all tests, handling authentication automatically.
-   **Parametrization**: `@pytest.mark.parametrize` is used to run the same test logic against multiple datasets (e.g., valid users, missing fields).

## 5. Setup & Usage

### Installation
```bash
git clone <repo_url>
cd Automation_Framework_API
python -m venv .venv
.\.venv\Scripts\Activate  # Windows
pip install -r requirements.txt
```

### Configuration
1.  Get a token from [GoRest.co.in](https://gorest.co.in/).
2.  Create `.env` file:
    ```properties
    GOREST_TOKEN=your_token_here
    ```

### Execution
Run all tests and generate a report:
```bash
pytest
```

Artifacts location:
-   **Report**: `reports/report.html`
-   **Logs**: `logs/automation.log`
