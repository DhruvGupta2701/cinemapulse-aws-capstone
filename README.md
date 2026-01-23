## CinemaPulse – AWS-Ready Movie Analytics & Review Platform

CinemaPulse is a full-stack Flask-based web application that allows users to explore movies, submit reviews, analyze community sentiment, and manage personal favorites. It includes separate dashboards for users and admins and is designed with AWS deployment in mind. The project focuses on clean backend logic, session-based authentication, analytics computation, and a professional UI built without frontend frameworks.

---

## Project Description

CinemaPulse is a movie discovery and analytics platform where:

- Users can browse movies, rate them, leave feedback, and maintain a favorites list.
- The system dynamically calculates movie ratings and sentiment-based analytics.
- Admins can manage movies and moderate feedback.
- The architecture is prepared for cloud deployment on AWS using EC2, DynamoDB, and SNS.
- The application demonstrates how a production-style Flask backend can power a responsive and interactive dashboard-driven platform.

---

## Key Features

### User Features
- User registration & login
- Personalized dashboard
- Browse movies with ratings & analytics
- Submit feedback and ratings
- Auto-updated movie rating (average of all reviews)
- View personal feedback history

### Admin Features
- Admin login
- Add / Update / Delete movies
- View all feedbacks
- Delete inappropriate feedback
- Monitor movie analytics

### Analytics Engine
- Keyword-based sentiment detection
- Community sentiment breakdown (Positive / Neutral / Negative)
- CinemaPulse Score (0–100)
- Trend prediction:
  - Trending Up
  - Stable
  - Trending Down

---

## Technology Stack

| Layer          | Technology                     |
|----------------|---------------------------------|
| Backend        | Python, Flask                  |
| Frontend       | HTML5, CSS3, Vanilla JavaScript |
| Styling        | Custom CSS (Dark Analytics Theme) |
| Authentication | Flask Sessions                 |
| State Storage  | In-memory Python dictionaries  |
| Version Control| Git & GitHub                   |
| Cloud Platform | AWS (EC2, IAM, DynamoDB, SNS)  |

---

## Project Structure

AWS-CinemaPulse/
├── app.py
├── README.md
├── static/
│   ├── css/
│   │   ├── Indexstyle.css
│   │   └── dashboard_style.css
│   └── js/
│       └── Indexscript.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── sample.html
└── venv/

---

## Authentication & Session Flow

- Users can register and log in securely
- Flask sessions are used to maintain login state
- Admin access control planned for future role-based functionality

---

## AWS Deployment Plan

- Deploy the Flask backend on **AWS EC2**
- Configure **Gunicorn** and **Nginx** for production
- Use environment variables for secure configuration
- Assign **IAM roles** for secure service access
- Integrate **DynamoDB** for data storage and **SNS** for notifications

---

##  Future Enhancements

- Expand analytics with ML-based sentiment services (e.g., Amazon Comprehend)
- Replace in-memory storage with DynamoDB tables
- Add email/SMS alerts via SNS when new reviews arrive
- Implement role-based authorization and audit logs
- Improve UI theming with more dashboards and charts

---

## Author
- Palak (AWS Capstone Project)
---

## Note

This project is developed as part of an **AWS Capstone / Internship Project** to demonstrate cloud-based application deployment, modular backend development, and system design principles.

