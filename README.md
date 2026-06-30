# DummyJSON API Testing Project

Automated API testing project built in **Python** using **pytest** and **requests**.
This project tests the public [DummyJSON](https://dummyjson.com/) API, covering both positive and negative scenarios across product, authentication, and comments endpoints.

---

## 📋 Project Overview

This project validates the DummyJSON API by checking:
- **Status codes** (200, 201, 400, 404)
- **Response data** (structure, values, business logic)
- **JSON fields** (presence, types, nested objects)
- **Positive scenarios** (valid requests return expected data)
- **Negative scenarios** (invalid requests fail correctly)

---

## 📂 Project Structure

```
api_assigment/
│
├── client/                       # API client (wrapper around requests)
│   ├── __init__.py
│   └── api_client.py             # DummyJSONClient class with all endpoints
│
├── tests/                        # All test cases
│   ├── __init__.py
│   ├── test_products.py          # Products + Authentication tests (1-10)
│   └── test_comments.py          # Comments tests (extra test cases)
│
├── venv/                         # Virtual environment (not committed)
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

---

## 🛠️ Tech Stack

- **Python 3.14**
- **pytest** — Testing framework
- **requests** — HTTP client

---

## 🚀 Setup Instructions

The project was set up on **Windows** using **Git Bash** as the terminal. The following steps describe the full setup from scratch.

### Step 1: Install Python 3.14

1. Download the installer from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. ⚠️ **Important:** On the first screen of the installer, check both boxes:
   - ☑ **Use admin privileges when installing py.exe**
   - ☑ **Add python.exe to PATH**
4. Click **Install Now**.
5. After installation, close and reopen any open terminals.
6. Verify the installation:

   ```bash
   py --version
   ```

   Expected output: `Python 3.14.x`

### Step 2: Create the project folder

```bash
mkdir api_assigment
cd api_assigment
```

### Step 3: Create the virtual environment

A virtual environment isolates the project's dependencies from the rest of the system.

```bash
py -m venv venv
```

This creates a `venv/` folder inside the project.

### Step 4: Activate the virtual environment

**On Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**On Windows (PowerShell/CMD):**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

When the virtual environment is active, the prompt is prefixed with `(venv)`:

```
(venv)
user@machine MINGW64 /c/api_assigment
$
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

This installs `pytest` and `requests` (and their sub-dependencies) inside the virtual environment.

### Step 6: Verify the setup

> ⚠️ **Important:** If the virtual environment is currently active (you see `(venv)` at the start of your prompt), deactivate it first before running `pip list`:
>
> ```bash
> deactivate
> ```

Then run:

```bash
pip list
```

You should see at least:
```
pytest        x.x.x
requests      x.x.x
```

After verifying, re-activate the virtual environment to continue working:

```bash
source venv/Scripts/activate
```

---

## ▶️ Running the Tests

> ⚠️ Make sure the virtual environment is active (`(venv)` should appear at the start of the prompt) before running any of the following commands.

### How to run the tests (full workflow)

Every time you start working on the project, follow these three steps in order:

**Step 1: Navigate to the project folder**
```bash
cd /c/api_assigment
```

**Step 2: Activate the virtual environment**
```bash
source venv/Scripts/activate
```

You should now see `(venv)` at the start of your prompt.

**Step 3: Run the tests**
```bash
pytest -v
```

That's it — three commands and the full test suite runs.

### Basic commands

The two commands you will use most often:

**Run all tests:**
```bash
pytest -v
```

**Run a specific test by name:**
```bash
pytest tests/test_products.py::<test_function_name> -v -s
```
Explanation of the above cmd:
```
pytest <path_to_file>::<test_function_name> -v -s
```

### Additional / extra commands

**Run all tests with print output visible:**
```bash
pytest -v -s
```

**Run only the products + auth test file:**
```bash
pytest tests/test_products.py -v
```

**Run only the comments test file:**
```bash
pytest tests/test_comments.py -v
```

**Run tests matching a keyword:**
```bash
pytest -v -k "valid_id"
```

### Useful pytest flags

| Flag | Description |
|------|-------------|
| `-v` | Verbose output (show each test name) |
| `-vv` | More verbose (detailed error messages) |
| `-s` | Show `print()` output |
| `-x` | Stop at the first failure |
| `-k "keyword"` | Run only tests matching the keyword |
| `--tb=short` | Shorter tracebacks on failure |

### Deactivating the virtual environment

When you are done working on the project:

```bash
deactivate
```

---

## ✅ Test Cases Implemented

### Products Endpoints

Implemented in `tests/test_products.py`.

| # | Test Case | Endpoint | Method | Scenario | What it Validates |
|---|-----------|----------|--------|----------|-------------------|
| 1 | Get all products | `/products` | GET | Positive | Status 200, response structure (products, total, skip, limit), all 22 product fields, nested objects (`dimensions`, `meta`, `reviews`), data types, business logic |
| 2 | Get product by valid ID | `/products/{id}` | GET | Positive | Status 200, single product returned, returned ID matches requested ID, all 22 fields present with correct types |
| 3 | Get product by invalid ID | `/products/99999` | GET | Negative | Status 404, error message in response, message mentions the invalid ID |
| 4 | Search products by keyword | `/products/search?q={keyword}` | GET | Positive | Status 200, response structure, all returned products contain the keyword in title/description/category/brand/tags |
| 5 | Test pagination | `/products?limit&skip&select` | GET | Positive | Status 200, exact number of returned products matches `limit`, `skip` value respected, only selected fields returned, page 1 and page 2 contain different products |
| 6 | Create a new product | `/products/add` | POST | Positive | Status 201 (Created), auto-generated ID, all submitted fields returned correctly |
| 7 | Update an existing product | `/products/{id}` | PUT | Positive | Status 200, product ID unchanged, submitted fields updated, other fields preserved |
| 8 | Delete a product | `/products/{id}` | DELETE | Positive | Status 200, `isDeleted: true`, valid `deletedOn` timestamp, original product data preserved |

### Authentication Endpoints

Implemented in `tests/test_products.py`.

| # | Test Case | Endpoint | Method | Scenario | What it Validates |
|---|-----------|----------|--------|----------|-------------------|
| 9 | Login with valid credentials | `/auth/login` | POST | Positive | Status 200, returns `accessToken` and `refreshToken` (JWT format), correct user data (id, username, email, etc.) |
| 10 | Login with invalid credentials | `/auth/login` | POST | Negative | Status 400, error message returned, NO tokens returned, NO user data leaked (tests multiple scenarios: wrong username, wrong password, both wrong, empty credentials) |

### Extra Test Cases — Comments Endpoints

Implemented in `tests/test_comments.py`. These tests cover the [Comments endpoint](https://dummyjson.com/docs/comments) of the DummyJSON API.

| # | Test Case | Endpoint | Method | Scenario | What it Validates |
|---|-----------|----------|--------|----------|-------------------|
| 11 | Get all comments | `/comments` | GET | Positive | Status 200, response structure (comments, total, skip, limit), all 5 comment fields, nested `user` object (id, username, fullName), data types, business logic across **all** comments |
| 12 | Get a single comment by ID | `/comments/{id}` | GET | Positive | Status 200, single comment returned (not a list), returned ID matches requested ID, all 5 fields present with correct types, nested `user` object validated |
| 13 | Limit & Skip comments (pagination) | `/comments?limit&skip&select` | GET | Positive | Status 200, exact number of returned comments matches `limit`, `skip` value respected, first comment has the expected ID after skipping, page 1 and page 2 contain different comments |
| 14 | Get all comments by post ID | `/comments/post/{postId}` | GET | Positive | Status 200, response structure, **filter logic**: every returned comment has `postId` matching the requested post ID, full field/type validation on all comments |
| 15 | Add a new comment | `/comments/add` | POST | Positive | Status 201 (Created), auto-generated ID, submitted fields (`body`, `postId`) returned correctly, nested `user` object populated based on the `userId` sent in the request |
| 16 | Update an existing comment | `/comments/{id}` | PUT | Positive | Status 200, comment ID unchanged, submitted field (`body`) updated, other fields (`postId`, `likes`, `user`) preserved after partial update |
| 17 | Delete a comment | `/comments/{id}` | DELETE | Positive | Status 200, `isDeleted: true`, valid `deletedOn` timestamp, original comment data preserved in the response |

---

## 🧪 What the Tests Validate

Each test case verifies multiple aspects of the API response:

- **Status codes** — confirms the API returns the correct HTTP status (200, 201, 400, 404)
- **JSON structure** — verifies all expected top-level keys are present
- **Field presence** — ensures every expected field exists in the response
- **Data types** — confirms each field is the correct type (int, str, list, dict, etc.)
- **Nested objects** — validates the structure of nested data (`dimensions`, `meta`, `reviews`, `user`)
- **Business logic** — checks logical constraints (positive prices, ratings 0-5, valid emails, etc.)
- **Filter logic** — verifies that endpoints filtering by parameter (e.g. comments by post ID) return only matching results
- **Negative paths** — verifies the API fails correctly with invalid input

---

## 📝 Notes

- The DummyJSON API **simulates** create, update, and delete operations but does not persist data to a real database.
- All endpoints used in this project are publicly available — no API key required.
- Tests use the demo user `emilys` (password: `emilyspass`) provided by DummyJSON.

---

## 📚 Resources

- [DummyJSON Documentation](https://dummyjson.com/docs)
- [DummyJSON Comments Endpoint](https://dummyjson.com/docs/comments)
- [pytest Documentation](https://docs.pytest.org/)
- [requests Documentation](https://requests.readthedocs.io/)
