from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user,logout_user, current_user, login_required
from app import app, db,lm,oid
from forms import LoginForm, SignupForm, SigninForm, PostForm, AnswerForm
from models import User, ROLE_USER, ROLE_ADMIN, Post, Answer
from datetime import datetime

@app.route('/', methods= ['GET', 'POST'])
@app.route('/index', methods= ['GET', 'POST'])
#@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    user= g.user
    posts = Post.query.all()
    return render_template("index.html", title='Home',
                     user=user, posts=posts, form=form)


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.nickname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email']=newuser.email
            return redirect(request.args.get('next') or url_for('index'))
   
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
   
    if request.method == 'POST':
        
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            user =User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('Username or Password is invalid' , 'error')
                return redirect(url_for('signin'))
            remember_me=1
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('index'))
                 
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/post/<id>', methods = ['GET', 'POST'])
#@login_required
def post(id):
    form = AnswerForm()
    post_=Post.query.filter_by(id=id).first()
    answers=post_.answers.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            answer = Answer(body = form.answer.data, timestamp = datetime.utcnow(), author = g.user, question=post_)
            db.session.add(answer)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('post', id=post_.id))
        #return redirect(url_for('post', post=post, answers=answers, form=form))
    
    return render_template('post.html', post=post_, answers=answers, form=form)


@app.route('/_add_numbers')
def add_numbers():
    c = request.args.get('c', 0)
    cat = Answer.query.filter_by(id=int(c)).first() 
    likes=cat.likes+1
    cat.likes=likes
    db.session.commit() 
    return jsonify(result=int(cat.likes))
