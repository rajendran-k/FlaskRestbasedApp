import Datahandler as datahandler

def validate_model(model):
    count = 0
    if model is False:
        return False
    else:
        
        
            if "Name" in model:
                name = model["Name"]
                if type(name) is str:
                     count= count+ 1
            if "Price" in model:                
                price = model["Price"]
                if type(price) is int:
                    count= count+ 1
            if "Isbn" in model:
                isbn = model["Isbn"]
                if type(isbn) is int:
                    count= count+ 1
    if count == 3:
        return True
    else:
        return False   

def validate_update_model(model):
    count = 0
    if model is False:
        return False
    else:
        if "Isbn" in model:
            return False
        if "Name" in model:
            name = model["Name"]
            if type(name) is str:
                count= count+ 1
        if "Price" in model:
            price = model["Price"]
            if type(price) is int:
                count= count+ 1
    if count == 2:
        return True
    else:
        return False    

def validate_isbn_already_exist(isbn, books):
    if (isbn is False) or (books is False):
        return False
    else:
        for book in books:
            if book['Isbn'] == isbn:
                return False
        else:
            return True
def validate_registraton_model(request_model):   
    if not request_model:
        return False
    else:
        if "username" in request_model:
            if "password" in request_model:
                return True
            else:
                return False    
        else:
            return False    
            

            
                
              

