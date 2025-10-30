from flask import Flask

app = Flask(__name__)

@app.route('/')
def home ():
    return('this is the environment setting and start on flask')

if __name__ == '__main__':
    app.run()
