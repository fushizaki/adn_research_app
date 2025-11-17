from flask import render_template
from appJurassique import app

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

if __name__ == "__main__":
    app.run()