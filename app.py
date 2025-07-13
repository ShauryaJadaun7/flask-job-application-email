from flask import Flask ,request,render_template,redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_mail import Mail, Message
from flask import flash


app = Flask(__name__)
app.secret_key = 'secret_key'
# Email config

# Looking to send emails in production? Check out our Email API/SMTP product!
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = XXXX
app.config['MAIL_USERNAME'] = 'Add user name'
app.config['MAIL_PASSWORD'] = 'Add your mailtrap pass here'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
mail = Mail(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datauser.db'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register" , methods = ['GET','POST'])

def register():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route("/login" , methods = ['GET','POST'])

def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else :
            return render_template('login.html',error = 'Inavalid user Credentials')

    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        jobs = [
            {"title": "Software Engineer", "department": "Tech", "salary": "8 LPA"},
            {"title": "Data Analyst", "department": "Analytics", "salary": "6.5 LPA"},
            {"title": "HR Executive", "department": "HR", "salary": "5 LPA"},
            {"title": "Marketing Manager", "department": "Marketing", "salary": "7.5 LPA"},
            {"title": "Finance Associate", "department": "Finance", "salary": "6 LPA"},
        ]
        return render_template('dashboard.html' , name=user.name, jobs=jobs )
    return redirect('/login')

@app.route('/apply_job', methods=['POST'])
def apply_job():
    # make sure this is imported at the top
        job_title = request.form['job_title']

        if 'email' not in session:
            return redirect('/register')

        user = User.query.filter_by(email=session['email']).first()

        try:
            msg = Message(
                subject=f"Job Application: {job_title}",
                recipients=["your_email@gmail.com"],
                body=f"""
    Name: {user.name}
    Email: {user.email}
    Applied for: {job_title}
                """,
                reply_to=user.email
            )
            mail.send(msg)
            flash(f'Application for "{job_title}" sent successfully!', 'success')  # success message
        except Exception as e:
            flash(f'Failed to send application: {e}', 'danger')  # error message

        return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run()

