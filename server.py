from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello flask</h1>'


@app.route('/usr/<name>')
def user(name):
    return 'Hello, {}'.format(name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
