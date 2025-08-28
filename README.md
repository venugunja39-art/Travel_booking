# Travel Booking System (Django Project)
A web-based travel booking application built with **Django**.
It allows users to register, log in, search travel options (Flights, Trains, Buses), book tickets with seat availability validation, and cancel bookings. Admins can manage travel schedules and user bookings from the Django admin panel.
## Features
* User Registration & Login (Authentication & Authorization)
* Search available travel options (Flights, Trains, Buses)
* Book tickets with seat validation (reduces available seats after booking)
* View and cancel bookings
* Admin dashboard to manage users, travel options, and bookings
##  Tech Stack
* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, Bootstrap
* **Database**: SQLite (default Django DB)
* **Deployment**: GitHub / PythonAnywhere

## Project Structure
travel_booking/
│── booking/              # App for travel and booking logic
│── travel_project/       # Main Django project settings
│── templates/            # HTML templates
│── manage.py             # Django project manager
##  How to Run Locally

1. Clone the repository

   ```bash:
  
   git clone https://github.com/venugunja39-art/travel_booking.git
   cd travel_booking
   ```

2. Create Virtual Environment & Install Dependencies

   ```bash:
   
   python -m venv venv
   venv\Scripts\activate   # On Windows
   pip install -r requirements.txt
   ```

3. Run Migrations

   ```bash
   python manage.py migrate
   ```

4. Create Superuser (for admin access)

   ```bash
   python manage.py createsuperuser
   ```

5. Run Server

   ```bash
   python manage.py runserver
   ```

6. Visit site:

   * User site: `http://127.0.0.1:8000/`
   * Admin panel: `http://127.0.0.1:8000/admin/`

## Future Enhancements

* Add Payment Gateway
* Email Notifications for Bookings
* Multiple Language Support
## Author
Developed by **Venu Gunja** as part of a backend development assignment for **Travel Lykke Internship**.
