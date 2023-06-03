from app import app


@app.route('/')
def home():
    return "hello world!"

@app.route('/irreb')
def irreb():
    return ' هذا'
