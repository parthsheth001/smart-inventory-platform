## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Test: `python test.py`

## API Endpoints
- GET /products - Get all products
- GET /product/<id> - Get single product
- POST /create_product - Create product
- DELETE /delete_product/<id> - Delete product
```

---

## 💡 Architectural Observations (Food for Thought)

### **Your Route Naming:**
You used `/get_products`, `/create_product` - this works, but there's a more RESTful pattern:

**Current (works fine):**
```
GET    /get_products
POST   /create_product
GET    /get_product/<id>
DELETE /delete_product/<id>
```

**More RESTful (industry standard):**
```
GET    /products          # The HTTP method implies "get"
POST   /products          # The HTTP method implies "create"
GET    /products/<id>
DELETE /products/<id>
```

Notice the pattern? Same URL, different HTTP methods. This is what most APIs do (including Django REST Framework).

**Should you change it now?** No! It works. But know this pattern exists for Phase 2.

---

## 🎓 What You Just Learned (Write This Down)

- ✅ Flask routing and decorators
- ✅ Handling JSON requests/responses
- ✅ HTTP methods and status codes
- ✅ Basic validation and error handling
- ✅ Writing API tests with requests library
- ✅ List comprehensions with `next()` for searching

**Most importantly:** You proved you can learn a new framework quickly.

---

## 🚀 Phase 2: Add PostgreSQL + Docker

Now that you have working Flask endpoints, let's make the data persist in a real database.

### **Your Next Mission (3-4 days):**

**What you'll add:**
1. **PostgreSQL database** running in Docker
2. **SQLAlchemy ORM** to replace your in-memory list
3. **Database migrations** (optional but professional)
4. **Docker Compose** to run everything together

**What stays the same:**
- Your route structure (mostly)
- Your test file approach
- Your validation logic

---

## 📋 Phase 2 Requirements

### **Database Schema:**
```
Table: products
- id (PRIMARY KEY, AUTO INCREMENT)
- name (VARCHAR, NOT NULL)
- description (TEXT)
- price (DECIMAL)
- category (VARCHAR)
- created_at (TIMESTAMP)