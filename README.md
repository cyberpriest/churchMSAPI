# Church Management System API

A FastAPI-based REST API for managing church operations including members, services, attendance, and categories.

## ✨ Features

- **Member Management** - Add, update, delete, and list church members
- **Service Management** - Manage church services and schedules
- **Attendance Tracking** - Record and monitor member attendance
- **Category System** - Organize members by categories
- **Admin Dashboard** - SQLAdmin interface for data management
- **JWT Authentication** - Secure API endpoints with JWT tokens
- **Role-Based Access Control** - Admin, Pastor, Moderator roles

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: JWT with bcrypt
- **Admin Panel**: SQLAdmin
- **ORM**: SQLAlchemy
- **Server**: Uvicorn (development) / Gunicorn (production)

## 📦 Installation

### Prerequisites
- Python 3.9+
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/cyberpriest/churchMSAPI.git
cd churchMSAPI
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Configure environment**
```bash
copy .env.example .env
# Edit .env with your values (optional for development)
```

5. **Run the server**
```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 🚀 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user

### Members
- `GET /members/` - List all members
- `POST /members/` - Create new member
- `GET /members/{member_id}` - Get member details
- `PUT /members/{member_id}` - Update member
- `DELETE /members/{member_id}` - Delete member

### Services
- `GET /services/` - List all services
- `POST /services/` - Create service
- `PUT /services/{service_id}` - Update service
- `DELETE /services/{service_id}` - Delete service

### Categories
- `GET /categories/` - List categories
- `POST /categories/` - Create category
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Attendance
- `GET /attendance/` - List attendance records
- `POST /attendance/` - Record attendance
- `PUT /attendance/{attendance_id}` - Update attendance

## 📖 Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Admin Panel**: http://localhost:8000/admin

## 🌐 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key_here
SESSION_SECRET_KEY=your_session_key_here
DATABASE_URL=sqlite:///./church.db
JWT_EXPIRE_MINUTES=20
```

## 📊 Database Models

### User
- id, email, password, full_name, roles, created_at

### Member
- id, first_name, last_name, email, phone, address, category_id

### Service
- id, service_name, date, time, location, description

### Category
- id, name, description

### Attendance
- id, member_id, service_id, date, status

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- CORS configuration
- Environment variables for secrets
- SQL injection prevention via SQLAlchemy ORM

## 📈 Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

Quick start: Deploy to Render with PostgreSQL in minutes!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**CyberPriest** - Church Management System

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- SQLAlchemy for ORM
- SQLAdmin for admin interface
- Render for hosting

---

**Happy coding! 🚀**