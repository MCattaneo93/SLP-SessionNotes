from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#@app.before_first_request
#def log_database_info():
#    database_name = db.engine.execute("SELECT current_database();").scalar()
#    print(f"Connected to database: {database_name}")

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'




@app.route('/create_user')
def create_user():
    existing_user = User.query.filter_by(username='testuser').first()
    if existing_user is not None:
        db.session.delete(existing_user)
        db.session.commit()
        return {'message': 'Existing user deleted and recreated'}
    
    user = User(username='testuser')
    db.session.add(user)
    db.session.commit()
    print(os.getenv('DATABASE_URL'))
    return {'message': 'User created'}


if __name__ == '__main__':
    app.run(debug=True)
