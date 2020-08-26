from flask import Flask, session, render_template, url_for, request, redirect, send_from_directory

import os
import json

from string import Template
# from mail import send_message

from functools import wraps

application = Flask(__name__)
application.secret_key = os.urandom(12)

env = os.environ['CG_FLASK_ENV']
admin_username = os.environ['CG_ADMIN_USER']
admin_password = os.environ['CG_ADMIN_PASSWORD']

email_template = Template("""\
Subject: New Message From Blog

From: $name
Email: $email
Phone: $phone
Message:
$message
""")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ('logged_in' in session and session['logged_in']):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@application.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == admin_username) and (password == admin_password):
            session['logged_in'] = True
            return redirect('/')
        else:
            return "<h3>Wrong user name or password.</h3>"
    elif request.method == 'GET':
        return render_template('login.html')


@application.route('/')
@application.route('/index')
def index():
    template_kwargs = {
        'env': env
    }
    # return render_template('index.html',**template_kwargs)
    return render_template('coming_soon.html',**template_kwargs)

# @application.route('/products')
# @login_required
# def products():
#     template_kwargs = {
#         'env': env
#     }
#     return render_template('products.html',**template_kwargs)    

# @application.route('/contact',methods=['GET','POST'])
# @login_required
# def contact():
#     template_kwargs = {
#         'env': env
#     }
#     if request.method == 'GET':
#         return render_template('contact.html',**template_kwargs)
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         message = request.form.get('message')
#         email_kwargs = {
#             'name': name,
#             'email': email,
#             'phone': phone,
#             'message': message
#         }
#         formatted_email = email_template.substitute(**email_kwargs)
#         # send_message(formatted_email)
#         print("Commented out send_message() call.")
#         return redirect('/')

# # single post
# @application.route('/blog/<template_str>')
# @login_required
# def blog(template_str):
#     template_str = template_str.replace('-','_') + '.html'
#     template = os.path.join('posts',template_str)
#     print(template_str)
#     return render_template(template)

# # list of posts
# @application.route('/blog')
# @login_required
# def blogs():
#     return render_template('posts.html')

# @application.route('/robots.txt')
# @application.route('/sitemap.xml')
# def static_from_root():
#     return send_from_directory(application.static_folder, request.path[1:])

if __name__ == '__main__':
    application.run(host='0.0.0.0')
