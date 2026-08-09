# Ceedek Digital Business Platform

A full-stack business platform for Ceedek Digital, a fictional global technology and business solutions company. Built as a professional portfolio project.

## About

Ceedek Digital provides technology services to small businesses, startups, and growing organisations, including web development, business automation, data analytics, custom software development, and AI solutions.

This project is a complete business platform consisting of a public marketing website, an authenticated client portal, and an internal admin system for managing clients, projects, and quote requests.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL (SQLite for local development)
- **Version Control:** Git / GitHub

## Local Setup

1. Clone the repository
2. Create a virtual environment:
```
   python -m venv venv
```
3. Activate it (Windows PowerShell):
```
   .\venv\Scripts\Activate.ps1
```
4. Install dependencies:
```
   pip install -r requirements.txt
```
5. Create a `.env` file in the project root with:
```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
```
6. Run the development server:
```
   python manage.py runserver
```
7. Visit `http://127.0.0.1:8000/` in your browser

## Project Status

Currently in early foundational development.