from flask import render_template
from .app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from monApp.forms import LoginForm


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')


@app.route("/login/", methods=(
    "GET",
    "POST",
))
def login():
    unForm = LoginForm()
    unUser = None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
    if unUser:
        login_user(unUser)
        next = unForm.next.data or url_for("index", name=unUser.username)
        return redirect(next)
    return render_template("login.html", form=unForm)


if __name__ == "__main__":
    app.run()
