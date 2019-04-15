    
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Shooter1$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#create Blog class 
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120)) 
    body = db.Column(db.String(500))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

#check for input
def not_empty(input):
    if input:
        return True




#redirect to main blog page
@app.route('/')
def index():
    return redirect('/blog')




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
