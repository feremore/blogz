from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'
class Blog_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_content= db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self,blog_title,blog_content,owner):
        self.blog_title = blog_title
        self.blog_content = blog_content
        self.owner = owner
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship("Blog_Post", backref='owner')
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return self.username
@app.before_request
def require_login():
    allowed_routes = ['login','signup','build_blog','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid username', 'error') 
            return render_template('login.html')
        if not password == user.password:
            flash('Invalid password', 'error')
            return render_template('login.html')
        else:
            session['username']=username
            return redirect('/add-blog-post')
        
    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify   = request.form['verify']
        if username.strip()=='' or password.strip()=='' or verify.strip()=="":
            flash('Invalid username or password.', 'error')
            return render_template('signup.html',username=username)
        
        existing_user = User.query.filter_by(username=username).first()
        if password == verify:
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username']=username
                return redirect('/add-blog-post')
            else:
                flash('Username not avaliable.', 'error')
    return render_template('signup.html')
@app.route('/')
def index():
    
    user_list= User.query.all()
    
    return render_template('index.html',user_list=user_list)
@app.route('/blog',methods=['POST','GET'])
def build_blog():

    
    user = request.args.get('user')
    username = User.query.filter_by(username=user).first()
    if username:
        user_blog = Blog_Post.query.filter_by(owner=username).all()
        
            
        return render_template('singleUser.html',user_blog = user_blog)
    blog_list= Blog_Post.query.all()
    

    id_blog = request.args.get('id')
    blog_post = Blog_Post.query.get(id_blog)

    
    return render_template('blog.html',blog_post=blog_post, blog_list=blog_list)

    
    
@app.route('/add-blog-post',methods=['POST','GET'])
def add_blog():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        title_error=''
        body_error=''
        
            
        if blog_title.strip()=='':
            title_error='Please enter a title for your blog.'
            
        if blog_body.strip()=='':
            body_error='Please enter a body for your blog'
        if title_error!='' or body_error!='':    
            return render_template('add-post.html',body_error=body_error,title_error=title_error, blog_title=blog_title, blog_body=blog_body)
        blog_post = Blog_Post(blog_title,blog_body,owner)
        db.session.add(blog_post)
        db.session.commit()
        
        return redirect('/blog?id={0}'.format(blog_post.id))

    
    return render_template('add-post.html')
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__=='__main__':
    app.run()