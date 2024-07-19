from flask import Blueprint,render_template,request,redirect,flash,url_for
from .models import User,Blog,Comment

from .main import db
from flask_login import login_required,login_user,logout_user,current_user
views=Blueprint("views",__name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    blogs=Blog.query.all()[::-1] # type: ignore
  
    return render_template('home.html',user=current_user,blogs=blogs) 
@views.route('/<user>/my-blog',methods=['GET','POST']) 
@login_required
def my_blog(user):
    blog=Blog.query.filter_by(author=user).all()[::-1]
    return render_template('home.html',user=current_user,blogs=blog)
@views.route('/<username>/create-blog',methods=['GET','POST'])
@login_required
def create_blog(username):
    if request.method=='POST':
        blog=request.form.get('blog') # type: ignore
        if len(blog)<1:  # type: ignore
            flash('Too short!',category='error')
        else:
            new_note = Blog(blog=blog, author=username)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
        
            flash('Note added!', category='success')
            return  redirect(url_for('views.home'))
    return render_template('create-blog.html',user=current_user) 
@views.route('/<user>/update-blog/<id>',methods=['GET','POST'])
@login_required
def update_blog(user,id):
    blog=Blog.query.filter_by(id=id).first()
    if user!=blog.author:
        flash('You do not permitted !',category='error')

    if request.method=='POST':
        blog.blog=request.form.get('blog')
        if len(blog.blog)==1:  # type: ignore
            flash('Too short!',category='error')
        else:
            
           
            db.session.commit()
        
            flash('Blog updated!', category='success')
            return redirect(url_for('views.home'))
          
 

    return render_template('update-blog.html',blog=blog,user=current_user)
@views.route('/<user>/delete-blog/<id>')

@login_required
def delete(user,id):

    blog=Blog.query.filter_by(id=id).first()
    comments=Comment.query.filter_by(blog_id=id).all()
    if blog:
        if user!=blog.author:
            flash('You do not permitted !',category='error')
        else:
            if comments:
                for comment in comments:
                    db.session.delete(comment)
                    db.session.commit()

            db.session.delete(blog)
            db.session.commit()

            flash('Deleted success',category='success')

    
    return redirect(url_for('views.home'))

@views.route('<user>/create-comment/<id>',methods=['GET','POST'])
@login_required
def create_comment(user,id):
    if request.method=='POST':
        comment=request.form.get('comment')

        if not comment:
            flash('It is not empty!',category='error')
        else:
            new_comment=Comment(comment=comment,author=user,blog_id=id)
            db.session.add(new_comment)
            db.session.commit()
          

            print(new_comment.comment)
            
    return redirect(url_for('views.home'))
        
@views.route('<user>/blog/<blogid>/delete-comment/<commentid>',methods=['GET','POST'])
@login_required
def delete_comment(user,commentid,blogid):
    comment=Comment.query.filter_by(id=commentid).first()

    if not comment:
        flash('Comment does not exists!',category='error')
    # elif comment.blog_id!=blogid:
    #     flash(' Comment not in blog!',category='error')
    elif comment.author!=user and comment.blog_id.author!=user:
        flash('You do not allow!',category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
       
    return redirect(url_for('views.home'))
    


