# flask-job-application-email
A Flask web application for job applications with user authentication and real-time email notifications via Mailtrap.io. Users can register, log in, view job listings, and apply for jobs. Each application sends an email instantly, viewable in your Mailtrap.io inbox.

## Features

- User registration and login with password hashing
- Dashboard displaying available job roles
- Apply for jobs and send application emails
- Real-time email delivery via Mailtrap.io
- SQLite database for user data
- Bootstrap-based responsive UI

## Setup Instructions

1. **Clone the repository**  
   ```
   git clone <your-repo-url>
   cd email_send proj
   ```

2. **Install dependencies**  
   ```
   pip install flask flask_sqlalchemy flask_mail bcrypt
   ```

3. **Configure Mailtrap.io**  
   The app is pre-configured to use Mailtrap SMTP.  
   You can view real-time emails sent by the app in your Mailtrap inbox.

4. **Run the application**  
   ```
   python app.py
   ```

5. **Access the app**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## File Structure

- `app.py` - Main Flask application
- `instance/datauser.db` - SQLite database
- `templates/` - HTML templates (index, login, register, dashboard)
- `static/` - Static files (CSS, JS, images)

## Notes

- You can see real-time emails sent by the app in your [Mailtrap.io](https://mailtrap.io) inbox.
- Change the Mailtrap credentials in `app.py` if you use your own Mailtrap account.

## License

MIT
