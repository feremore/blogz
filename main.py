from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'
class Blog_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_content= db.Column(db.String(255))
    owner_id = db.Column(db.Interger, foreign_key=True)
    
    def __init__(self,blog_title,blog_content):
        self.blog_title = blog_title
        self.blog_content = blog_content
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(50))
    blogs = db.Column(db.Blog_Post,foreign_key=True)
    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
@app.route('/login',methods=['POST']
def login():
    if request.method == 'POST':
        username = request.form['username']
        
return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    return render_template('signup.html')
@app.route('/')
def index():
    
    blog_list= Blog_Post.query.all()
    
    return render_template('blog.html',blog_list=blog_list)
@app.route('/blog')
def build_blog():
    blog_list= Blog_Post.query.all()
    

    id_blog = request.args.get('id')
    blog_post = Blog_Post.query.get(id_blog)


    return render_template('blog.html',blog_post=blog_post, blog_list=blog_list)

    
    
@app.route('/add-blog-post',methods=['POST','GET'])
def add_blog():
    
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
        blog_post = Blog_Post(blog_title,blog_body)
        db.session.add(blog_post)
        db.session.commit()
        
        return redirect('/blog?id={0}'.format(blog_post.id))

    
    return render_template('add-post.html')

if __name__=='__main__':
    app.run()