# 🏥 City Care Hospital — Full Stack DevOps Project

A real-world hospital appointment booking system built with **Flask**, **SQLite**, **Docker**, **Nginx**, and deployed on **AWS EC2** with a **CI/CD pipeline** using GitHub Actions.

---

## 🗂️ Project Structure

```
citycare/
├── app.py                        ← Flask backend & API routes
├── database.py                   ← SQLite database setup & seeding
├── requirements.txt              ← Python dependencies
├── Dockerfile                    ← Docker image instructions
├── docker-compose.yml            ← Multi-container orchestration
├── nginx.conf                    ← Nginx reverse proxy config
├── .dockerignore                 ← Files excluded from Docker build
├── templates/
│   └── index.html                ← Full frontend (HTML/CSS/JS)
└── .github/
    └── workflows/
        └── deploy.yml            ← GitHub Actions CI/CD pipeline
```

---

## ⚙️ Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Frontend    | HTML, CSS, JavaScript   |
| Backend     | Python Flask            |
| Database    | SQLite                  |
| Container   | Docker + docker-compose |
| Web Server  | Nginx (reverse proxy)   |
| Cloud       | AWS EC2                 |
| CI/CD       | GitHub Actions          |
| Monitoring  | AWS CloudWatch          |

---

## 🚀 Run Locally with Docker

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/citycare-hospital.git
cd citycare-hospital

# 2. Start all containers
docker-compose up --build

# 3. Open in browser
http://localhost:80
```

---

## 🔐 Admin Login

- **URL:** http://localhost/admin
- **Username:** admin
- **Password:** citycare123

---

## 🔌 API Endpoints

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | /                           | Home page                |
| GET    | /booking                    | Booking page             |
| GET    | /admin                      | Admin dashboard          |
| POST   | /api/appointments           | Book appointment         |
| GET    | /api/appointments           | Get all appointments     |
| PATCH  | /api/appointments/<id>      | Update status            |
| DELETE | /api/appointments/<id>      | Delete appointment       |
| GET    | /api/stats                  | Dashboard stats          |
| POST   | /api/contact                | Send contact message     |
| POST   | /admin/login                | Admin authentication     |

---

## 🔧 GitHub Secrets Required for CI/CD

Go to your GitHub repo → Settings → Secrets → Add:

| Secret Name       | Value                              |
|-------------------|------------------------------------|
| DOCKER_USERNAME   | Your Docker Hub username           |
| DOCKER_PASSWORD   | Your Docker Hub password           |
| EC2_HOST          | Your EC2 Public IP address         |
| EC2_USER          | ubuntu                             |
| EC2_SSH_KEY       | Contents of your .pem private key  |

---

## ☁️ Deploy on AWS EC2

```bash
# On your EC2 instance (Ubuntu):
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu

# Copy project files to EC2 then run:
docker-compose up -d
```

---

## 👨‍💻 Built By
College DevOps/Cloud Project — Demonstrating full-stack deployment with Docker & AWS.
