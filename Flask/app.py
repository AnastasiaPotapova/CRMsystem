from flask import Flask
from routes.excursions import excursions_bp
from routes.polls import polls_bp

app = Flask(__name__)
app.register_blueprint(excursions_bp)
app.register_blueprint(polls_bp)

if __name__ == "__main__":
    app.run(debug=True)