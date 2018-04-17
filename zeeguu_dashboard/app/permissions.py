from functools import wraps

from flask import redirect, session
import app as application
import app.util
import json

def check_session():
    if not 'sessionID' in session.keys():
        session['sessionID'] = '0'

    permission_bool = app.util.api_get('has_session').text
    permission_bool = json.loads(permission_bool)
    if permission_bool == 1:
        return True
    return False

#General decorator to check if the teacher is logged in
def has_session(func):

    @wraps(func)
    def session_wrapper(*args, **kwargs):

        if check_session():
           return func(*args, **kwargs)
        else:
          return redirect("login")

    return session_wrapper


#Decorator to check if the teacher has access to a page. CURRENTLY ONLY WORKS FOR CLASS PERMISSIONS
def has_class_permission(func):

    @wraps(func)
    def class_permission_wrapper(class_id):
        if not check_session():
            return redirect('401')
        permission_bool = app.util.api_get('get_class_permissions/' + str(class_id)).text
        permission_bool = json.loads(permission_bool)
        if permission_bool == 1:
            return func(class_id)
        else:
            return redirect('401')

    return class_permission_wrapper

def has_student_permission(func):

    @wraps(func)
    def student_permission_wrapper(user_id):
        if not check_session():
            return redirect('401')
        permission_bool = app.util.api_get('get_user_permissions/' + str(user_id)).text
        permission_bool = json.loads(permission_bool)
        if permission_bool == 1:
            return func(user_id)
        else:
            return redirect('401')

    return student_permission_wrapper