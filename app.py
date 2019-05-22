from flask import Flask,url_for,render_template,request,  redirect,url_for, flash,abort
from flask_login import LoginManager , login_required , UserMixin , login_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, SignatureExpired
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12292091'
app.config['MYSQL_PASSWORD'] = 'Neeraj@mysql'
app.config['MYSQL_DB'] = 'sql12292091'

# object of MySql
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return None

class User(UserMixin):
    def __init__(self , first , last , email , password , id , active=False):
        self.id = id
        self.first = first
        self.last = last
        self.email = email
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.email , key='secret_key')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0
    
    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.email, user)

    def get_email(self, email):
        return self.users.get(email)    
    
    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)
    
    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'neera99j@gmail.com'           #use your gmail ID
app.config['MAIL_PASSWORD'] = ''	#Use Password of gmail ID
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)


flag = 0

def globally_change():
    global  flag 
    flag = 1
@app.route("/", methods=['GET' , 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registeredUser = users_repository.get_email(email)
        if registeredUser != None and registeredUser.password == password and registeredUser.active == True:
            globally_change()
            # print("value of flasg is :;",flag)
            print('Logged in..')
            login_user(registeredUser)
            return redirect(url_for('login_page'))
        else:
            return abort(401)
             # pyautogui.alert('Please signup first!', "alert")  # always returns "OK"
            # return render_template("home.html")
    else:
        return render_template("home.html")

@app.route("/login_page")
def login_page():
    print("flag is ",flag)
    if flag == 1:
        return render_template("login.html")
    else:
        return "Please Login first"

string = "b17100@students.iitmandi.ac.in"   #default webmail 
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        global first_db
        global last_db
        global email_
        global password_db
        userDetails = request.form
        firstName = userDetails['firstName']
        first_db = firstName
        lastName = userDetails['lastName']
        last_db = lastName
        email = userDetails['email']
        email_ = email
        print(email_)
        global string
        string = email
        password = userDetails['password'] 
        password_db = password
        new_user = User(firstName , lastName , email , password , users_repository.next_index())
        users_repository.save_user(new_user)
        return redirect(url_for('verification_page'))

    return render_template("signup.html")

token=""
random_URL = URLSafeSerializer('secret_key')
@app.route("/verification_page")
def verification_page():
    global random_URL
    random_URL = URLSafeSerializer('secret_key')
    global token
    token = random_URL.dumps(string, salt='email-confirm')
    #Put email ID of sender in <sender>
    msg = Message('Email confirmation', sender = 'neera99j@gmail.com', recipients = [string])
    msg.body = "Activate your account by clicking the link: "
    domain = "http://localhost:5000/confirm_email/"
    msg.body += domain
    msg.body += token
    mail.send(msg)
    return "Please see your email for verification"
    
@app.route('/confirm_email/<token_recv>')
def confirm_email(token_recv):
    try:
        email = random_URL.loads(token_recv, salt='email-confirm')
        cur = mysql.connection.cursor()
        print("email is ",email_)
        cur.execute("INSERT INTO Login(Email, FirstName,LastName,password) VALUES(%s,%s, %s,%s)",(email_,first_db,last_db,password_db))
        cur.execute("Delete from Login")
        mysql.connection.commit()
        cur.close()
    except SignatureExpired :
        return '<h2>The token is expired!</h2>'
    registeredUser = users_repository.get_email(email)
    #set registered user to be active means user's account is verified.
    registeredUser.active = True
    return '<h2>The token works!</h2>'

@app.route('/profile/<enroll_no>')
def profile_page(enroll_no):
    global alumni_no
    alumni_no = enroll_no
    return render_template('profile.html')

@app.route("/login_page/alumni")
def alumniLogin():
    return render_template("alumni.html")

@app.route("/login_page/students")
def adminLogin():
    return render_template("students.html")

@app.route("/login_page/faculty")
def studentLogin():
    return render_template("faculty.html")

@app.context_processor
def context_processor():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Alumni Where EnrollmentNumber=%s",[alumni_no])
    alumni_basic_information = cur.fetchall()
    cur.execute("SELECT * FROM Contact_Details Where EnrollmentNumber=%s",[alumni_no])
    contact_deatils = cur.fetchall()
    cur.execute("SELECT * FROM Worked_In Where EnrollmentNumber=%s",[alumni_no])
    Worked_In = cur.fetchall()
    cur.execute("SELECT * FROM Higher_Studies Where EnrollmentNumber=%s",[alumni_no])
    Higher_Studies = cur.fetchall()
    cur.execute("SELECT * FROM Semester_Exchange Where EnrollmentNumber=%s",[alumni_no])
    sem_exchange = cur.fetchall()
    cur.execute("SELECT * FROM Contributed_To Where EnrollmentNumber=%s",[alumni_no])
    contribution = cur.fetchall()
    cur.close()
    return dict(username=string, alumni=alumni_basic_information, contact=contact_deatils, work=Worked_In, study=Higher_Studies, sem_exchange=sem_exchange, contribution=contribution)
    
if __name__ == "__main__":
    app.run(debug=True)
