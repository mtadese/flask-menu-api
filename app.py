from flask import Flask, json, jsonify, request

app = Flask(__name__)

#create a menu card to be displayed  for guest's orders
menucard = [{'Item' : 'Rice', 'Price':100},{'Item': 'Plantain','Price':50},{'Item':'Chicken','Price':200},{'Item':'Beef', 'Price':150},{'Item':'Fish','Price':200},{'Item':'Chapman','Price':150}]
orders = []

#display hello-world on homepage
@app.route('/') 
def hello_world():
    response = jsonify('Hello world!')
    response.status_code = 200
    return response

#display the menu card on the menu page/inteface
@app.route('/menu',methods = ['GET', 'PUT', 'DELETE'])
def show_menu():
    if request.method == 'GET':
        response = jsonify({'Menu':menucard})
        response.status_code = 200
        return response

# PUT Method to add an item to the menucard
    elif request.method == 'PUT':
        response = {}
        payload = request.get_json()
        item = payload["item1"]
        f = False
        for i in menucard:
            if i ==item:
                f = True
        if not f:
            menucard.append(item)
            response = jsonify({'Status': 'Added','Item':item})
            response.status_code =201
        else:
            response = jsonify({'Status': 'Already There','Item':item})
            response.status_code =400
        return response


#DELETE Method to delete an item from the menucard
    elif request.method == 'DELETE':
        response = {}
        payload = request.get_json()
        itemid = payload["id"]
        if itemid == 0:
            item = menucard[itemid]
            del menucard[itemid]
            response = jsonify({'Status':'Deleted','Item':item})
            response.status_code = 200
            return response

        response = jsonify({'Status':'Not in Menu','ItemID':itemid})
        response.status_code = 404
        return response

@app.route('/orders', methods = ['GET', 'POST'])
def order():

#GET Request for obtaining the list of already ordered items
    if request.method == 'GET':
        response = ' '
        if len(orders)==0:
            response = jsonify({'Your orders':'Haven\'t ordered anything yet'} )
            response.status_code = 404
        else :
            response = jsonify({'Your orders':orders})
            response.status_code = 200
        return response

# POST Method to add an item to orders
    elif request.method == 'POST':
        response = {}
        payload = request.get_json()
        id1 = int(payload['id'])
        if id1== len(menucard):
            response = jsonify({'Status': 'Not in menu'})
            response.status_code = 404
        elif menucard[id1] in orders:
            for i in orders:
                if i['Item'] == menucard[id1]['Item']:
                    i['Quantity']+=1
            response = jsonify({'Status': 'Updated quantity','Item':menucard[id1]})
            response.status_code =200
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)
