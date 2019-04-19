    
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Shooter1$@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#secretkey
app.secret_key = 'wP3h#c08LK$chw'

#create Blog class 
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False) 
    body = db.Column(db.String(5000), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


#create User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True) 
    password = db.Column(db.String(50)) 
    #spec relationship (not col)
    blogs = db.relationship('Blog', backref ='owner')

    #blogs which signifies a relationship between the blog table and this user, 
    # thus binding this user with the blog posts they write.
   


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username

#check for input
def not_empty(input):
    if input:
        return True


#we want this func to run for every request
@app.before_request
#check for to see if they are logged in
def require_login():
    #create list of pages OK to view without being logeed in.
    allowed_routes = ['login', 'signup', 'index', 'show_all_posts']
    #if there is not a username key in session dict (not logged in),
    # then redirect to login
    #enpoint is given path
    #square brackets ??
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')





#redirect to main blog page
@app.route('/')
def index():
    users = User.query.all()
    user_id = request.args.get('id')

 #show all posts for user when username is clicked on   
    if not_empty(user_id):
        owner = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('userposts.html', title = 'View user posts', blogs=blogs)
     #TODO add username to page   
    
    
    
    
    else:
        return render_template('index.html', title="Show All Users", users=users)




#route to login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            #session adds key to dict . 
            # remembers that user logged in access like dict
            session['username'] = username
            #flash messages use session object to store message for 
            #next time user comes back
            flash('Logged in')
            return redirect('/')
        else:
            ##### needs work
            users = User.query.all()
            if not username and not password:
                flash('Please enter your username and password', 'error')
            elif not username:
                flash('Please enter your username', 'error')
            elif user and not password:
                flash('Please enter password')
            elif user and user.password != password:
               flash('Incorrect password', 'error')
            elif username not in users:
                flash('Username does not exist', 'errpr')
                return redirect('/signup')
    return render_template('login.html')

#route to signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        

        if not username and not password:
            flash('Please choose a username and password', 'error')
        elif len(username) < 3:
            flash('Username must be longer than 3 characters', 'error')
        elif not existing_user and len(password) <= 3:
            flash('Password must be longer than 3 characters', 'error')
        elif not existing_user and len(password) >3 and password != verify:
            flash('Passwords do not match', 'error')
        elif not existing_user and len(password) >3 and password ==verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Username already exists', 'error')
            return  render_template('signup.html') 
    return render_template('signup.html')

#route to log out
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

#route to show all blogs on main page, and show indiv posts        
@app.route('/blog', methods=['POST', 'GET'])
def show_all_posts():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    #TODO: order by date time desc

    if not_empty(blog_id):
        indiv_post = Blog.query.get(blog_id)
        blog_title = indiv_post.title
        blog_body = indiv_post.body
        return render_template('indivpost.html', title="Show Individual Post", blog_title=blog_title, blog_body = blog_body)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Show All Posts", blogs=blogs)
        
        


#route to display form to add new posts
@app.route('/newpost', methods=['POST', 'GET'])
def add_new_post():

    title_error = ''
    body_error = ''

    owner = User.query.filter_by(username=session['username']).first()

    #form validatation
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        # moved above ---- owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_body, owner)
        
        
        if not_empty(blog_title) and not_empty(blog_body):    
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id 
            return redirect('/blog?id={0}'.format(blog_id))
            
        elif not not_empty(blog_title) and not not_empty(blog_body):
            title_error = 'Please enter a title.'
            body_error = 'Please enter content.'
            return render_template('newpost.html',title="Add Blog Entry", body_error=body_error, title_error=title_error)

        elif not not_empty(blog_title):
            title_error = 'Please enter a title.'   
            return render_template('newpost.html',title="Add Blog Entry", body_error=body_error, title_error=title_error)

        elif not not_empty(blog_body):
            body_error = 'Please enter content.'
                
            return render_template('newpost.html',title="Add Blog Entry", body_error=body_error, title_error=title_error)
    
     
    #blogs = Blog.query.all()
    #blogs = Blog.query.filter_by(owner=owner).all()

    
    return render_template('newpost.html', title="Add Blog Entry", body_error=body_error, title_error=title_error)   
    


@app.route('/myposts', methods=['POST', 'GET'])
def show_my_posts():
    owner = User.query.filter_by(username=session['username']).first()
    blogs = Blog.query.filter_by(owner=owner).all()
    return render_template('myposts.html', title="Show All Posts", blogs=blogs)


#optional route to delete blog posts
@app.route('/delete-post', methods=['POST'])
def delete_post():
    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return redirect('/blog')


@app.route('/userposts', methods=['POST', 'GET'])
def show_user_posts():
    owner = User.query.filter_by(username=session['username']).first()
    blogs = Blog.query.filter_by(owner=owner).all()
    return render_template('myposts.html', title="Show All Posts", blogs=blogs)



if __name__ == '__main__':
    app.run()
