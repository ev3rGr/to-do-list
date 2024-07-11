import socket

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from functions import (
    add_task,
    get_task,
    delete_task,
    edit_statu,
    e_check,
    add_user,
    u_check,
    get_id
)

app = Flask(__name__)
app.secret_key = ["mysecretkey"]

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Process the form data
        print(f"Received data: {email}")
        print(f"Received data: {password}")
        if u_check(email, password):
            id_user = get_id(email)
            session["id_user"] = id_user
            return redirect("/")
        else:
            return render_template("login.html", error = "inccorect username or password")
    return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('first')
        lastname = request.form.get('last')
        email = request.form.get('email')
        password = request.form.get('password')
        repassoword = request.form.get('repassword')
        if e_check(email):
            return render_template("register.html", message = "email already exist !",
                            firstname = firstname,
                            lastname = lastname
                            )
        if password != repassoword:
            return render_template("register.html",
                                    error = "Passwords do not match",
                                    firstname = firstname,
                                    lastname = lastname,
                                    email = email
                                    )
        # Process the form data
        print(f"Received data: {firstname}")
        print(f"Received data: {lastname}")
        print(f"Received data: {email}")
        print(f"Received data: {password}")
        print(f"Received data: {repassoword}")
        add_user(  firstname,
                   lastname,
                   email,
                   password
                   )
        return redirect("/login")
    return render_template("register.html")

@app.route("/", methods = ['POST', 'GET'])
def home():
    if "id_user" in session:
        id_user = session["id_user"]
        if request.method == "POST":
            task = request.form.get("text").strip()
            if task != "":
                add_task(task,id_user)
        tasks = get_task(id_user)
        return render_template("home.html", tasks = tasks)
    else:
        return redirect("/login")

@app.route("/delete/<id>", methods = ["POST","GET"])
def delete(id):
    if "id_user" in session:
        id_user = session["id_user"]
        delete_task(id,id_user)
        return redirect("/")
    else:
        redirect("/login")

@app.route("/finish/<id>", methods = ["POST","GET"])
def finish(id):
    if "id_user" in session:
        id_user = session["id_user"]
        edit_statu(id,id_user)
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("id_user",None)
    return redirect("/login")

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    app.run(host = s.getsockname()[0], debug = True)