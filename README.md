# student-exam-portal

**Tech Stack:** Django + DRF + SimpleJWT  
**Frontend:** HTML templates for validation

---

## 🚀 Setup (Development)

1. **Create & activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Migrate & seed database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py seed_questions
   ```

3. **Run server**
   ```bash
   python manage.py runserver
   ```

---

## 🌐 URLs

- **API Health:** [http://127.0.0.1:8000/api/health/](http://127.0.0.1:8000/api/health/)
- **Login Template:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📚 API Endpoints

| Method | Endpoint                                 | Description                                 |
|--------|------------------------------------------|---------------------------------------------|
| POST   | `/api/auth/register/`                    | Register `{username, email, password}`      |
| POST   | `/api/auth/token/`                       | Login `{username, password}` → JWT tokens   |
| POST   | `/api/exam/start/`                       | Start exam (auth, `{num_questions}` optional)|
| POST   | `/api/exam/<attempt_id>/submit/`         | Submit answers `{ "answers": { "qid": option_id } }` (auth) |
| GET    | `/api/exam/<attempt_id>/result/`         | Get attempt result (auth)                   |

---

## 🧪 Quick Testing / Example Workflow

1. Start server:
   ```bash
   python manage.py runserver
   ```
2. Register user:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"s1","email":"s1@example.com","password":"Password123"}'
   ```
3. Obtain JWT token:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"s1","password":"Password123"}'
   ```
4. Start exam:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/exam/start/ \
     -H "Authorization: Bearer <access>" \
     -H "Content-Type: application/json" \
     -d '{"num_questions":5}'
   ```
5. Submit answers:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/exam/<attempt_id>/submit/ \
     -H "Authorization: Bearer <access>" \
     -H "Content-Type: application/json" \
     -d '{"answers":{"1":2,"3":7}}'
   ```

---

## 💡 Notes & Improvements

- **Production:** Use secure `SECRET_KEY`, set `DEBUG=False`, use PostgreSQL, enable HTTPS, refresh token flows, and rate-limiting.
- **Testing:** Add automated tests for endpoints.
- **Migrations:** Add migration files to repo (created after `makemigrations`).
- **Frontend:** Remove template views if switching to React; templates are for quick manual validation.

---

## 📦 Next Steps

If you want, I can:
- Create migration files and a zip of this structure for download, or
- Push these files to your `student-exam-portal` repo (provide remote URL and branch), or
- Generate a curl/Postman collection with example responses.

**Let me know which option you prefer!**