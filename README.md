
# Flask MVC Point of Sale Project

This is a Flask-based MVC (Model-View-Controller) project for a Point of Sale system. This system is designed to provide an interface to sell and buy products, manage stock, and keep track of customer accounts.


## Installation
Clone the repository to your local machine:
```bash
  $ git clone https://github.com/JQuintanaDev/flask-sellpoint.git
```
To get started with this project, you'll need to install the following packages:

- Flask==2.0.3
- Flask_Login==0.6.2
- Flask_SQLAlchemy==2.5.1
- psycopg2==2.9.3
- SQLAlchemy==1.4.39
- SQLAlchemy_Utils==0.38.3
- Werkzeug==2.0.3

You can use pip to install these packages by running the following command:


```bash
  pip install -r requirements.txt
```
    
## Database

This project uses a PostgreSQL database to store data. You'll need to have PostgreSQL installed and running on your system.
## Deployment

Once you have the required packages installed and the database set up, you can run the Flask application using the following command:

```bash
  python app.py runserver
```
This will start the Flask development server and you can access the application by opening a web browser and navigating to the URL shown in the server output.

The application includes the following features:

### Landing Page
The landing page provides a navigation bar for user role permissions.

### Authentication
The application includes authentication using Flask-Login. Users can log in with a username and password.

### Sessions
Session management is included to keep track of active user sessions.

### Sell, Buy, and Stock Management
The application includes interfaces for selling and buying products, as well as managing stock levels.

### Customer Account Management
The application is designed to keep track of customer accounts, including balances and transaction history.



## Authors
This project was created by:

- [@franja1994](https://github.com/JQuintanaDev)

If you have any questions or comments about this project, please feel free to contact me at [franja1994@gmail.com].

