# Web-Based Stock Trading Application 

## Overview
This is a Flask-based web application designed to simulate stock trading. Users can sign up, log in, and manage their stock portfolios by buying and selling stocks. The app provides real-time stock data, user authentication, and session management.

## Features
- **User Authentication:** Secure sign-up and login functionality.
- **Stock Trading:** Buy and sell stocks, manage your portfolio.
- **Real-time Graphical Data:** Fetches real-time stock data using a public API for showing Trends.
- **Admin Panel:** Admins can manage users and stocks, and handle user queries.
- **User Testing:** Conducted with a group of 10 participants for feedback and improvements.

## Technologies Used
- **Backend:** Flask, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Data Visualization:** Matplotlib
- **Other Libraries:** Requests, Pytz

## Setup Instructions (Run In Terminal)
1. Clone the repository:
   ```bash
   git clone https://github.com/adityasinghal25/Trading-App.git

2. Navigate to the project directory:
   ```bash
   cd Trading-App

3. Install the required packages: Download the 'requirements.txt' file and then run the following command in terminal
    ```bash
   pip install -r requirements.txt

4. Setup BootStrap on your system:
   ```bash
     https://getbootstrap.com/docs/5.3/getting-started/download/
After installing Bootstrap transfer the 'bootstrap.min.css' file into Static Folder of the Project Directory.

5. Run the Application
   ```bash
   python app.py

10. Open your browser and go to http://127.0.0.1:5000 to access the app.

## Usage
- **Home Page:** The main landing page.
- **Sign Up:** Register a new user account.
- **Login:** Log in with your username and password.
- **Admin Panel:** Access for admin users to manage the application.
- **User Dashboard:** Manage your stock portfolio and view trading history.




## Project Structure 
```
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
   
