from flask_login import UserMixin
from sqlalchemy import Text
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from flask import current_app 

from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

# User model: Represents a user in the application
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')  # Default to 'user', can be 'admin' or 'user'

    # Relationship to Result: A user can have many results
    results = db.relationship('Result', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return self.id
    
    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset', max_age=expires_sec)['user_id']
        except (SignatureExpired, BadSignature) as e:
            return None  # Invalid or expired token
        return User.query.get(user_id)

    
    def set_password(self, password):
        """Hash the password and store it."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Verify the password."""
        return bcrypt.check_password_hash(self.password, password)


# Quiz model: Represents a quiz
class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key from User (admin)

    # Relationship to Question: A quiz can have many questions
    questions = db.relationship('Question', backref='quiz',  cascade="all, delete-orphan", lazy=True)

    # Relationship to Result: A quiz can have many results (user scores)
    results = db.relationship('Result', backref='quiz', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Quiz {self.title}, Category {self.category}>'

    def get_id(self):
        return self.id


# Question model: Represents a question within a quiz
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)  # The actual text of the question
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # Store 'a', 'b', 'c', or 'd'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  # Foreign key to Quiz

    def __repr__(self):
        return f'<Question {self.question_text[:30]}...>'

    def get_id(self):
        return self.id


# Result model: Represents the user's score on a quiz
class Result(db.Model, UserMixin):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  # Foreign key to Quiz
    score = db.Column(db.Integer, nullable=False)  # User's score in the quiz
    attempted_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp when the quiz was attempted
    answers = db.Column(Text, nullable=True)  # Store answers as a string (JSON, comma-separated, etc.)
    time_taken = db.Column(db.Integer)  # Time in seconds
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Result User {self.user_id} Quiz {self.quiz_id} Score {self.score}>'

    def get_id(self):
        return self.id
