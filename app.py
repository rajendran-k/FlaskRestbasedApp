from flask import Flask, jsonify ,request, Response
import Validation as Validation
import json
import Datahandler as datahandler
import login_controller as auth_check
from functools import wraps
import jwt

app= Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated (*args, **kwargs):
        token = request.headers.get('token')
        result = auth_check.validate_token(request,token)
        if result:
            return f(*args, **kwargs)            
        else:
            return jsonify({'message':'Token is invalid'}), 403    
    return decorated        


@app.route('/books')
@token_required
def welcomerequest():
    result = datahandler.get_all_data()
    if result is not True:
        return Response(json.dumps('try adding data'),status = 400, mimetype = 'application/json') 
    return jsonify(result)


@app.route('/token')
def get_token():  
    if not request.authorization:
        return Response(json.dumps('Missing autherrization'),status= 401,mimetype = 'application/json')   

    result = auth_check.login_check(request.authorization)    

    if result is True:
        token = auth_check.create_token(request.authorization)
        return Response(json.dumps(token),status= 200,mimetype = 'application/json')
    else:
        return Response(json.dumps('Wrong credential'),status= 401,mimetype = 'application/json')    
     
@app.route('/register', methods=['POST'])
def registration():
    request_model = request.get_json()
    result = Validation.validate_registraton_model(request_model)    
    if result:
        status = auth_check.registration_check(request_model)
        if status is True:
            return Response(json.dumps('User already exist try another username'),status=403,mimetype = 'application/json') 
        else:
            user_status = auth_check.add_user(request_model)
            return Response(json.dumps(user_status),status=201,mimetype = 'application/json')
    else:
        return Response(json.dumps('Request model is wrong'),status=403,mimetype = 'application/json')


@app.route('/books/<int:Isbn>')
@token_required
def get_books_by_id(Isbn):    
    if(Isbn is False):
        return jsonify("error.. please enter book ISDN")
    else:        
        results = datahandler.search_data(Isbn)     
        if results is not None:               
            return jsonify(results)
        else:
            return jsonify("Please try with another id")       

@app.route('/books', methods=['POST'])
@token_required
def add_book():
    data= request.get_json()
    result = Validation.validate_model(data)
    if result is True:
        duplicate = datahandler.validate_isbn_exist(data["Isbn"])
        if duplicate is False:
            datahandler.insert_data(data)              
            response = Response(json.dumps("Added"), 201 ,mimetype = 'application/json')
            response.headers['Location']= f'/books/' + str(data['Isbn'])
            return response
        else:
            error_help={
            "error":"Invalid data passed",
            "help":"ISBN already exist"
        }
        response = Response(json.dumps(error_help),status= 415 ,mimetype = 'application/json')
        return response    
    else:
        error_help={
            "error":"Invalid data passed",
            "help":"Check the model which is passed"
        }
        response = Response(json.dumps(error_help),status= 415 ,mimetype = 'application/json')
        return response


@app.route('/books/<int:isbn>', methods = ['PUT'])    
@token_required
def update_books(isbn):    
    if isbn is False:
        error_help={
            "error":"ISBN is missing",
            "help":"Check the ISBN which is passed"
        }
        response = Response(json.dumps(error_help),status= 415 ,mimetype = 'application/json')
        return response
    else:
        data=request.get_json()
        result = Validation.validate_update_model(data)   
        if result is True:
            datahandler.update_data_using_isbn(isbn, data)         
            response = Response(json.dumps("Added"), 201 ,mimetype = 'application/json')
            response.headers['Location']= f'/books/' + str(isbn)
            return response
        else:
            error_help={
            "error":"Invalid data passed",
            "help":"Check the model which is passed"
            }
            response = Response(json.dumps(error_help),status= 415 ,mimetype = 'application/json')
            return response

@app.route('/books/<int:isbn>', methods =['DELETE'])
@token_required
def delete_books_by_id(isbn):
    if(isbn is False):
        error_help={
            "error":"Invalid ISBN passed",
            "help":"ISBN should not be empty"
            }
        response = Response(json.dumps(error_help),status= 415 ,mimetype = 'application/json')
        return response
    else:
        result = datahandler.delete_data_using_isbn(isbn)
        if result:
            response = Response(json.dumps("Deleted"), 201 ,mimetype = 'application/json')
            response.headers['Location']= f'/books/' + str(isbn)
            return response
        else:
            error_message={"error":"Invalid ISBN passed",
                    "help":"ISBN not found"
                }
            response = Response(json.dumps(error_message),status= 415 ,mimetype = 'application/json')
            return response         
            





if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5001,debug=True)