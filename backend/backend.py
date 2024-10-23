from flask import Flask, request, redirect, url_for, flash




app = Flask(__name__)


@app.route('/', methods=['GET','POST'])  # Página de inicio
def hom():
    pass







if __name__ == '__main__':
    app.run(debug=True)