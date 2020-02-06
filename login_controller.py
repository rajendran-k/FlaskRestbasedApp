import jwt
import datetime
import Datahandler as datahandler

key = 'asdasd@#$%^7687765'


def login_check(request):
    username= request.username
    password = request.password
    result = datahandler.check_valid_user(username, password)
    if result:
        return True
    else:
        return False


def create_token(request):
      
    token = jwt.encode({'user': request.username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, key, algorithm='HS256')     
    return token.decode('UTF-8')

def validate_token(request, token):
    try:
        data = jwt.decode(token, key, algorithm='HS256')        
    except:       
        return False
    return True        

def registration_check(request_model):
    username = request_model['username']
    password = request_model['password']

    result = datahandler.user_is_present(username)
    if result is False:
        return False
    else:
        return True

def add_user(request_model):
    username = request_model['username']
    password = request_model['password']
    result = datahandler.add_user(username,password)
    if result:
        return "User is added"


