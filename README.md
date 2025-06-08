# 🏋️‍♂️ Fitness Class Booking API

A simple RESTful API built with Django & Django REST Framework to manage fitness classes and allow clients to book them.

---

## 🚀 Features

- List available fitness classes  
- Book a fitness class (slots management, duplicate prevention)  
- View bookings by client email  
- Token-based authentication (uses DRF `IsAuthenticated` permission)  
- Logging of success and errors  
- Safe transactional booking with race condition prevention  

---

## 📚 Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- SQLite (default, easily switchable to PostgreSQL/MySQL)  
- Logging with Django logging framework  

---

## 🗂 Project Structure

fitness_booking_api/
├── fitness/ # Your Django app
│ ├── models.py # FitnessClass & Booking models
│ ├── serializers.py # Serializers for API responses
│ ├── views.py # API Views
│ ├── urls.py # API routes
├── fitness_booking_api/ # Project settings
│ ├── settings.py # Django settings + logging setup
├── db.sqlite3 # Database (default)
├── manage.py
├── README.md
├── fitness_booking.log # Log file (auto-generated)

yaml
---

## 🏃‍♂️ Running Locally

1. **Clone repo**

    ```bash
    git clone https://github.com/yourusername/fitness_booking_api.git
    cd fitness_booking_api

2.Setup virtual environment
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3.Install dependencies
    pip install -r requirements.txt

4.Apply migrations
    python manage.py makemigrations
    python manage.py migrate

5.Create superuser 
    python manage.py createsuperuser

6.Run server
    python manage.py runserver



🔑 API Endpoints

    List Fitness Classes
        GET /classes/
        Requires Authentication
            curl -X GET http://localhost:8000/classes/ -H "Authorization: Token <your-token>"

    Book a Class
    POST /book/
    Requires Authentication

    Request Body:
        json
        {
        "class_id": 3,
        "client_name": "John Doe",
        "client_email": "john@example.com"
        }
    curl -X POST http://localhost:8000/book/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Token <your-token>" \
    -d '{"class_id": 3, "client_name": "John Doe", "client_email": "john@example.com"}'


    List Bookings by Client Email
    GET /bookings/?email=user@example.com
    Requires Authentication

        curl -X GET "http://localhost:8000/bookings/?email=user@example.com" -H "Authorization: Token <your-token>"


📝 Logging
    Logs stored in fitness_booking.log in project root

    Includes booking successes, duplicate attempts, errors, and API access info

✨ Future Improvements
    Cancel bookings
    Pagination on list endpoints
    Admin dashboard UI
    Email notifications on booking confirmation