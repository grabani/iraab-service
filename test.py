from app import app

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=56733, debug=True)
