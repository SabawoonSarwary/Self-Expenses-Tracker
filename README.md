# Self Expenses Tracker

## 📽️ Demo  
Watch a full walkthrough of the project on YouTube:  
👉 [Self Expenses Tracker – Final Project Demo (CS50x)](https://youtu.be/IOfacfcY438)

---

## 📘 Description  
**Self Expenses Tracker** is a personal finance web application that helps users monitor and manage their daily expenses.  
Built as a final project for **Harvard University's CS50x** course, the app allows users to register securely, log in, and track their spending by adding, editing, and deleting expense records. It provides a clear, organized view of where money is being spent, making it ideal for budgeting and financial awareness.

---

## 🎯 Motivation  
The inspiration for creating this application came from the everyday struggle many people face when trying to keep track of their expenses. In regions like Afghanistan, where financial tools are limited and often inaccessible, having a simple, free, and user-friendly application can make a real difference in personal finance management. I wanted to build something practical that could be used by students, workers, and families alike to gain better control over their spending habits.

---

## ✅ Features  
- 🔐 User registration and login system with secure password hashing  
- ➕ Add expenses with category, amount, and description  
- ✏️ Edit or delete existing expenses  
- 📊 View all expenses in a table format  
- 🔍 Sort and filter expenses by date or category  
- 📱 Clean, mobile-friendly interface using Bootstrap  
- 🧾 Data stored locally using SQLite  
- 📅 Date-wise sorting to track monthly or weekly expenses  

---

## 🛠 Technologies Used  
- **Python** – for the backend logic  
- **Flask** – web framework used to handle routing, sessions, and templating  
- **SQLite** – lightweight SQL database used for storing user data and expenses  
- **HTML/CSS** – to build and style the web pages  
- **Jinja** – for templating and dynamic HTML rendering  
- **JavaScript** – for client-side interactions  
- **Bootstrap** – to ensure responsiveness and mobile compatibility  

---

## 🧪 Development Process  
I began the project by identifying the essential features needed in a basic expense tracker: user authentication, data entry, editing and deleting records, and displaying the data in an organized manner.  
I set up the Flask environment and created routes for register, login, logout, and the main dashboard. After configuring the SQLite database, I created a model to handle the structure of the users and expenses tables. Then I built the frontend using Bootstrap to keep it clean and responsive. Finally, I added sorting and filtering features to make it easy for users to analyze their data.

---

## 🚧 Challenges Faced  
One of the biggest challenges I faced was implementing session management and secure password handling. CS50’s lectures helped me understand the theory, but applying it in a Flask environment was a learning curve.  
Another challenge was designing a user-friendly interface. I had to learn how to use Bootstrap effectively to make the site look professional while also being functional on smaller screens.  
Debugging the form submissions and making sure users could only edit their own data was also tricky, but I learned a lot about request validation and route protection in Flask.

---

## 📚 What I Learned  
Through building this project, I greatly improved my understanding of web development with Flask. I became more confident working with routes, templates, sessions, and databases.  
I also improved my ability to write clean, maintainable code and to think critically about user interaction and security.  
Importantly, this project showed me the value of breaking problems down into smaller parts and building each piece step-by-step.

---

## 🌱 Future Improvements  
If I continue this project, I’d like to add the following features:
- Export expenses as PDF or CSV
- Visual reports using graphs and charts (e.g., pie charts by category)
- User-defined categories
- Budget planning and alerts when spending exceeds a certain limit
- Multi-language support for local users
- Cloud deployment for easier access across devices

---

## 👤 About the Author  
My name is Sabawoon Sarwary, a self-taught programmer from Afghanistan. I began learning programming in high school and have worked through CS50x as a way to deepen my knowledge and skills.  
This final project is a representation of what I’ve learned and how I’ve grown throughout the course.

---

## 🚀 How to Run the Project Locally  

### 1. Clone the Repository  
```bash
git clone https://github.com/SabawoonSarwary/Self-Expenses-Tracker.git  
cd Self-Expenses-Tracker  
```

### 2. Install Dependencies  
Make sure you have Python and pip installed. Then run:  
```bash
pip install -r requirements.txt
```

### 3. Run the Application  
```bash
flask run
```

Then visit `http://127.0.0.1:5000` in your browser.

---

## 📝 Final Thoughts  
Completing this project helped me bring together all the topics I learned in CS50—problem-solving, algorithms, web programming, and software design. It gave me the confidence to continue building useful tools for real-world needs.  
CS50 taught me that great programmers are not those who never fail, but those who keep trying and improving. This project is my first real step into the world of software development.
