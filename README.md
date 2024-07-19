# Stock Trading Web App

## Overview
This is a Flask-based web application designed to simulate stock trading. Users can sign up, log in, and manage their stock portfolios by buying and selling stocks. The app provides real-time stock data, user authentication, and session management.

## Features
- **User Authentication:** Secure sign-up and login functionality.
- **Stock Trading:** Buy and sell stocks, manage your portfolio.
- **Real-time Data:** Fetches real-time stock data using a public API.
- **Admin Panel:** Admins can manage users and stocks, and handle user queries.
- **User Testing:** Conducted with a group of 10 participants for feedback and improvements.

## Technologies Used
- **Backend:** Flask, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Data Visualization:** Matplotlib
- **Other Libraries:** Requests, Pytz

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-trading-app.git

2. Navigate to the project directory:
3. ```bash
   cd stock-trading-app

4. Install the required packages:
5. ```bash
   pip install -r requirements.txt

6. Setup Database:
7. ```bash
   python setup_db.py

8. Run the Application
9. ```bash
   python app.py

10. Open your browser and go to http://127.0.0.1:5000 to access the app.

## Usage
- **Home Page:** The main landing page.
- **Sign Up:** Register a new user account.
- **Login:** Log in with your username and password.
- **Admin Panel:** Access for admin users to manage the application.
- **User Dashboard:** Manage your stock portfolio and view trading history.




## Project Structure 
stock-trading-app/
│
├── app.py                    # Main application file
├── requirements.txt          # List of dependencies
├── setup_db.py               # Script to set up the database
├── templates/                # HTML templates
│   ├── index.html            # Home page
│   ├── login.html            # Login page
│   ├── signup.html           # Signup page
│   └── ...                   # Other HTML files
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── ...
└── README.md 
   
