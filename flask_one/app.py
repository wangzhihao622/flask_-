
from flask import Flask,render_template,request,redirect,url_for,session,g
import  config

#新加的
from models import User,Question,Answer
from exts import db

from decorators import login_required
from sqlalchemy import or_
app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)


@app.route('/')
# @login_required
@app.route('/index/')
def index():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        # user = User.query.filter(User.telephone ==telephone,User.password ==password).first()
        user = User.query.filter(User.telephone ==telephone).first()
        if user and user.check_password(password):
            session['user_id'] =user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:

        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    #手机号验证，如果被注册了，就不能注册了
    user = User.query.filter(User.telephone ==telephone).first()
    if user:
        return  u'该手机号码已被注册，请更换手机号码'
    else:
        # password1要和password2相等才可以
        if password1 !=password2:
            return u'两次密码不相等，请核对后填写'
        else:
            user =User(telephone=telephone,username=username,password=password1)
            db.session.add(user)
            db.session.commit()
            # 如果注册成功，就让页面跳转到登录页面
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    # session.pop('use_id')
    session.clear()
    return redirect(url_for('login'))

# 发布问答
@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method =='GET':
        return render_template('question.html')
    else:
        title    = request.form.get('title')
        content  = request.form.get('content')
        question = Question(title=title,content=content)
        # user_id  = session.get('user_id')
        # user     = User.query.filter(User.id == user_id).first()
        # print(user)
        question.author = g.user
        # print(question)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail<question_id>/')
def detail(question_id):
    # print(question_id)
    question_model = Question.query.filter(Question.id == question_id).first()
    num=Answer.query.filter_by(question_id = question_id).count()
    # print(num)统计评论数
    return render_template('detail.html',question=question_model,num=num)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content  = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer   = Answer(content=content)
    # user_id  = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    # create_time = Question.query.filter_by( Question.id== question_id).first()
    context = {
        'questions': Answer.query.order_by('-create_time').all()
    }
    # return render_template('detail.html.', **context)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id,**context))

@app.route('/search/')
def search():
    q = request.args.get('q')
    # title,content   或
    # condition=or_(Question.title.contains(q), Question.content.contains(q)))
    # questions = Question.query.filter(condition).order_by('-create_time')
    # 与
    # questions = Question.query.filter(Question.title.contains(q), Question.content.contains(q))

    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q)))\
        .order_by('-create_time')
    return render_template('index.html',questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    user_id =session.get('user_id')
    # print('id',user_id)
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user':user}
    # return {}
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

# before_request->视图函数->context_processor

if __name__=='__main__':
    app.run()

