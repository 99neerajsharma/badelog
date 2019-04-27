from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/alumniLogin")
def alumniLogin():
    return render_template("alumniLogin.html")

@app.route("/adminLogin")
def adminLogin():
    return render_template("adminLogin.html")

@app.route("/studentLogin")
def studentLogin():
    return render_template("studentLogin.html")

@app.route("/contact")
def contacts():
    return render_template("contact.html")
    
if __name__ == "__main__":
    app.run(debug=True)