from flask import Blueprint,render_template,request,redirect,flash,url_for
from .models import User
from .main import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user,current_user
auth=Blueprint("auth",__name__)





@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=request.form.get('user')
        password=request.form.get('password')
        user_tmp=User.query.filter_by(user=user).first()
        if user_tmp:
            if password!=None:
                if check_password_hash(user_tmp.password,password):
                    flash('Logged in successfully!',category='success')
                    login_user(user_tmp,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Password is wrong!',category='error')



        else:
            flash('Username does not exist!',category='error')
  
    return render_template('login.html',user=current_user)
@auth.route('/sign_up',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        user=request.form.get('user')
        firstName=request.form.get('firstName')
        pw1=request.form.get('password1')
        pw2=request.form.get('password2')
        
        if user==None or firstName==None or pw1 ==None or pw2==None:
            flash("Not None !",category='error')
        else:
            user_tmp=User.query.filter_by(user=user).first()
               
            if user_tmp:
                flash('Username is alredy existed!',category='error')
                

            if len(user)<2:
                flash('Username must be greater than 2 characters',category='error')
            elif len(pw1)<5:
                flash('Password must be greater than 5 characters',category='error')
            elif pw1!=pw2:
                flash('Password is not match',category='error')
            
            else:
               
                new_user=User(user=user,password=generate_password_hash(pw1,method='scrypt',salt_length=20)
                              ,firstName=firstName)
                db.session.add(new_user)
                db.session.commit()
                data={}
                data['user']=user
                data['password']=pw1
                print(data)
              
                login_user(new_user,remember=True)
                flash('Created success',category='success')

                return redirect(url_for('views.home'))
       

    return render_template('sign_up.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


