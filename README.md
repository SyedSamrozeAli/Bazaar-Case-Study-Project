# Bazaar-Case-Study-Project

## 🧠 Design Decisions

1. **Modular Architecture**  
   Django REST Framework is used to structure the project using Models, Serializers, Views, and Permissions. This promotes maintainability and scalability.

2. **Role-Based Access Control**  
   Store admins can only access their own store’s data. Superusers have access to all records.

3. **Caching with Redis (via Memurai)**  
   Redis is used to cache frequently accessed data (like products) to reduce DB load and improve performance.

4. **Relational Database (PostgreSQL)**  
   PostgreSQL is used to handle complex relationships (e.g., Sales → SaleItems → Products).

5. **Throttling & Rate Limiting**  
   Django REST Framework’s throttling system is used to prevent abuse and ensure fair use.

6. **Filtering and Reporting**  
   API supports filters on sales and products by store and date range for reporting needs.

---

## 🚀 Evolution Rationale (v1 → v3)

### **V1: Basic MVP**
- Implemented core models: Product, Store, Sales, Inventory, Supplier.
- Developed CRUD APIs using Django REST Framework.

**Rationale**: Quickly validate core models and business logic.

---

### **V2: Enhanced Features**
- Added filtering and nested serializers.
- Applied request throttling and caching via Redis.
- Created Faker-based fake data generators.
- Store-admin based data restriction logic.
- Authentication implemented

**Rationale**: Improve performance, security, and realism in testing.

---

### **V3: Scalable Architecture**
- Horizontal scalability ready with modular views and caching.
- Redis used for product cache.
- Enhanced API performance with indexes and efficient querysets.

**Rationale**: Move towards a production-ready system by focusing on scalability and async processing.

---
## 🤔 Assumptions

- A user with the "store admin" role manages only one store.
- Products are globally stored but inventory is managed per store.
- A sale is linked to one store and includes multiple sale items.
- Caching service (Redis via Memurai) is running on `127.0.0.1:6379`.
- API requires user authentication.

---

## 🔌 API Design

Below are some sample APIs

APIS Documentation link [ https://documenter.getpostman.com/view/36394142/2sB2cYeMCL ]

### `GET /api/products/`
- **Description**: List products. Filtered based on store admin role.
- **Query Params**: `?ordering=created_at`
- **Response**: Paginated list of products.
- **Throttling**: Enabled

![image](https://github.com/user-attachments/assets/979b400c-ee43-4238-b7b0-b01aee3cae0b)

### `POST /api/sales/`
- **Description**: Create a sale record with multiple items.
- **Request Body**:
```json
{
  "store": 1,
  "sales_items": [
    {"product": 5, "quantity": 12},
    {"product": 2, "quantity": 24}
  ],
   "discount":10
}
```
- **Response**: Sale confirmation with totals.

![image](https://github.com/user-attachments/assets/4619e945-a7b7-4424-b047-4d4e79ba4f8d)


---

## 🛡️ Security

- Token-based authentication (JWT).
- Permissions restrict access based on user roles.
- Throttling to limit abuse.

---

## 📊 Performance

- Cached endpoints reduce redundant DB queries.
- PostgreSQL indexing for faster filters.

---


## 📂 Folder Structure

```
project/
│
├── api/                # App with views, serializers, models
├── config/             # Project settings
├── generate_fake_data.py
├── requirements.txt
└── README.md
```

---
