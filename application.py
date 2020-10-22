from flask import Flask, session, render_template, url_for, request, redirect, send_from_directory

import os
import json

from string import Template
from mail import send_message

from functools import wraps

application = Flask(__name__)

email_template = Template("""\
Subject: New Message From Website

From: $name
Email: $email
Message:
$message
""")

env = os.environ['CG_FLASK_ENV']

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not ('logged_in' in session and session['logged_in']):
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# @application.route('/login',methods=['POST','GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if (username == admin_username) and (password == admin_password):
#             session['logged_in'] = True
#             return redirect('/')
#         else:
#             return "<h3>Wrong user name or password.</h3>"
#     elif request.method == 'GET':
#         return render_template('login.html')


@application.route('/')
@application.route('/index')
def index():
    template_kwargs = {
        'env': env,
    }
    return render_template('coming_soon.html',**template_kwargs)

@application.route('/gallery')
def gallery():
    static_assets_folder = os.path.join('static','assets')
    # make list of files in assets that have 'carousel' in them
    # include the path so we can pass it to the templates
    carousel_imgs = [os.path.join(static_assets_folder,img) for img in os.listdir(static_assets_folder) if 'carousel' in img]
    # create all the attributes the css will need so we can define things in 
    # a for-loop in the templates
    carousel_data = []
    for i,img in enumerate(carousel_imgs):
        carousel_data.append({
            'id': i,
            'data-slide-to': i,
            'src': img,
            'alt': 'Slide %d' % i
        })
    template_kwargs = {
        'env': env,
        'carousel_data': carousel_data,
    }
    return render_template('gallery.html',**template_kwargs)    

@application.route('/contact',methods=['POST'])
# @login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        email_kwargs = {
            'name': name,
            'email': email,
            'message': message
        }
        # print(email_kwargs)
        formatted_email = email_template.substitute(**email_kwargs)
        # print('\n\n')
        # print(formatted_email)
        send_message(formatted_email)
        return redirect('/')

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
    application.run()