    
from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy 

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
    title = db.Column(db.String(120)) 
    body = db.Column(db.String(500))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body


#create User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True) 
    password = db.Column(db.String(50)) 

    #TODO blogs which signifies a relationship between the blog table and this user, 
    # thus binding this user with the blog posts they write.
    #blogs = not sure how to specify foreign key
    ########stopped @ 'Add User Class' last bullet pt#############

    def __init__(self, username, password):
        self.username = username
        self.password = password

#check for input
def not_empty(input):
    if input:
        return True


#we want this func to run for every request
@app.before_request
#check for to see if they are logged in
def require_login():
    #create list of pages OK to view without being logeed in.
    allowed_routes = ['login', 'signup']
    #if there is not a username key in session dict (not logged in),
    # then redirect to login
    #enpoint is given path
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')





#redirect to main blog page
@app.route('/')
def go_to_root():
    return redirect('/blog')

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
            return redirect('/')
        else:
            #TODO explain why login failed
            return '<h1>error</h1>'

    return render_template('login.html')

#route to signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO validation

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
            #TODO remember user
        else:
            #TODO - already exists message
            return '<h1>Duplicate User</h1>'    
    return render_template('signup.html')

#route to log out
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

#route to show all blogs on main page, and show indiv posts        
@app.route('/blog', methods=['POST', 'GET'])
def show_all_posts():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    #TODO: order by id desc 

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

    
    #form validatation
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        new_blog = Blog(blog_title, blog_body)
        
        
        if not_empty(blog_title) and not_empty(blog_body):    
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id 
            return redirect('/blog?id={0}'.format(blog_id))
        
        elif not not_empty(blog_title) and not not_empty(blog_body):
            title_error = 'Please enter a title.'
            body_error = 'Please enter content.'
            blogs = Blog.query.all()
            return render_template('newpost.html',title="Add Blog Entry", blogs=blogs, body_error=body_error, title_error=title_error)

        elif not not_empty(blog_title):
            title_error = 'Please enter a title.'
            blogs = Blog.query.all()
            return render_template('newpost.html',title="Add Blog Entry", blogs=blogs, body_error=body_error, title_error=title_error)

        elif not not_empty(blog_body):
            body_error = 'Please enter content.'
            blogs = Blog.query.all()
            return render_template('newpost.html',title="Add Blog Entry", blogs=blogs, body_error=body_error, title_error=title_error)
    
     
    blogs = Blog.query.all()
    
    return render_template('newpost.html', title="Add Blog Entry", blogs=blogs, body_error=body_error, title_error=title_error)   
    





#optional route to delete blog posts
@app.route('/delete-post', methods=['POST'])
def delete_post():
    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return redirect('/blog')




if __name__ == '__main__':
    app.run()
