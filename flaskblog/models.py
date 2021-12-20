from flaskblog import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Seriaalizer

# ====================================================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    @staticmethod
    def get_reset_token(self, expires_sec=1800):
        s = Seriaalizer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    
    def verify_reset_token(token):
        s = Seriaalizer(app.config['SECRET_KEY'])
        
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            return None
        return User.query.get(user_id)
        
    def __repr__(self) -> str:
        return f'User("{self.username}, {self.email}, {self.image_file}")'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f'Post("{self.title}, {self.date_posted}")'