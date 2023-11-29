# Django Dockerized E-commerce Project - Fohow
## Created by Pogos Team
This project was created by the talented Pogos team, bringing together expertise in Django, Docker, and other cutting-edge technologies.
## Overview
This Django-based project is a versatile e-commerce platform designed for Fohow, an online store. Utilizing Docker for containerization, it provides a scalable and portable solution for deploying the Fohow online store.
## Features
- **Product Catalog:** Showcase a diverse range of Fohow products with detailed information.
- **Reviews:** Enable customers to leave feedback on products and service.
- **Affiliate Program:** Attract partners and grow your business by offering opportunities to participate in the affiliate program
- **User Authentication:** Secure user accounts and authentication for a personalized shopping experience.
- **Admin Panel:** Simplify store management with an easy-to-use Django administrative panel.

## Tech Stack
- **Backend Framework:** Django, DRF
- **Database:** MySQL
- **Cache:** Redis
- **Task Queue:** Celery
- **Containerization:** Docker
- **Web Server:** Nginx
- **Programming Language:** Python
- **Development Tools:**
    - **Test Coverage:** Coverage
    - **Sorting and Importing:** Isort, Black
    - **Linter and Static Analysis:** Flake8
    - **Docker Compose:** Managing containers and services in Docker Compose

## Getting Started
1. **Clone Repository:**
   ```bash
    git clone https://github.com/ItSoda/Fohow.git
    cd Fohow
2. **Set Up Docker Environment:**
   ```bash
    docker-compose up -d --build
3. **Create Superuser (Administrator):**
   ```bash
    docker-compose exec fohow-api python manage.py createsuperuser
## Access the Application:
Open your browser and go to http://127.0.0.1:8000/ or http://boar-still-alpaca.ngrok-free.app/ to explore the Fohow online store.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

