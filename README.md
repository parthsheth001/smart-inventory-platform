## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Test: `python test.py`

## API Endpoints
- GET /products - Get all products
- GET /products/<id> - Get single product
- POST /products - Create product
- DELETE /products/<id> - Delete product


## Setup with Docker

### Prerequisites
- Docker and Docker Compose installed
- Python 3.8+

### Running the Application

1. Start PostgreSQL:
```bash
   docker-compose up -d
```

2. Create virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. Run the application:
```bash
   python app.py
```

4. Run tests:
```bash
   python test.py
```

### Stopping the Application
```bash
    docker-compose down
```

To remove all data:
```bash
    docker-compose down -v
```
```

#### **4.3: Create .gitignore**

Don't commit sensitive files:
```
venv/
__pycache__/
*.pyc
.env
*.db