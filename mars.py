from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def mission():
    return 'Миссия Колонизация Марса'


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    return "Человечество вырастает из детства.<br>" \
           "Человечеству мала одна планета.<br>" \
           "Мы сделаем обитаемыми безжизненные пока планеты.<br>" \
           "И начнем с Марса!<br>" \
           "Присоединяйся!"


@app.route('/image_mars')
def image_mars():
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Привет, Марс!</title>
        </head>
        <body>
            <h1>Жди нас, Марс!</h1>
            <img src={url_for('static', filename='img/mars.png')} />
            <h4>Вот она какая, красная планета.</h4>
        </body>
    </html> 
           '''


@app.route('/promotion_image')
def promotion_image():
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Колонизация</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
            <link href="{url_for('static', filename='css/style.css')}" rel="stylesheet">
        </head>
        <body>
            <h1>Жди нас, Марс!</h1>
            <img src={url_for('static', filename='img/mars.png')} />
            <div class="alert alert-primary">
                Человечество вырастает из детства.
            </div>
            <div class="alert alert-secondary">
                Человечеству мала одна планета.
            </div>
            <div class="alert alert-warning">
                Мы сделаем обитаемые безжизненные пока планеты.
            </div>
            <div class="alert alert-danger">
                И начнем с Марса!
            </div>
            <div class="alert alert-success">
                Присоединяйся!
            </div>
        </body>
    </html>
           '''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
