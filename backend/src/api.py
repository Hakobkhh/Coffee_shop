import os
import re
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)



'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

@app.route('/login-results')
def login_results():
    return 'Login complete'

'''
    GET /drinks
        - a public endpoint
        - contains only the drink.short() data representation
        - returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def retrieve_drinks():

    try:
        all_drinks = Drink.query.all()

        all_drinks_list = []

        for drink in all_drinks:
            all_drinks_list.append(drink.short())

        return jsonify({
            'success': True,
            'drinks': all_drinks_list
             })

    except Exception as e:
        abort(404)

'''
    GET /drinks-detail
        - Requires the 'get:drinks-detail' permission
        - Contains the drink.long() data representation
        - returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(jwt):

    try:
        all_drinks = Drink.query.all()

        all_drinks_list = []

        for drink in all_drinks:
            all_drinks_list.append(drink.long())

        return jsonify({
            'success': True,
            'drinks': all_drinks_list
             })

    except Exception as e:
        abort(404)



'''
    POST /drinks
        - Creates a new row in the drinks table
        - Requirs the 'post:drinks' permission
        - Contains the drink.long() data representation
        - returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

def drink_is_valid(body):
    """
    Check if drink provided in request body is valid
    """
    if not 'title' in body:
        print('1')
        abort(400)

    elif not 'recipe' in body:
        print('2')
        abort(400)

    elif len(body) != 2:
        print('3')
        abort(400)

    elif not body['title']:
        print('4')
        abort(400)


    recipe = body['recipe']

    # regex to match hex color code
    regx = r'^#(?:[0-9a-fA-F]{1,2}){3}$'
# @TODO delete tese print statements
    for ingredient in recipe:
        if not 'name' in ingredient:
            print('5')
            abort(400)
        elif not ingredient['name']:
            print('6')
            abort(400)
        elif not 'color' in ingredient:
            print('7')
            abort(400)
        elif not re.search(regx, ingredient['color']):
            # check if the string is a valid hex color code
            print('8')
            abort(400)
        elif not 'parts' in ingredient:
            print('9')
            abort(400)
        elif not isinstance(ingredient['parts'], int):
            print('10')
            abort(400)

    return True

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink():

    body = request.get_json()

    if drink_is_valid(body):
        try:
            new_drink = Drink()
            new_drink.title = body['title']
            new_drink.recipe = json.dumps(body['recipe'])

            new_drink.insert()

            return jsonify({'success': True,
                            'drinks': new_drink.long()},
                           )

        except:
            return abort(422)

'''

    PATCH /drinks/<id>
        - where <id> is the existing model id
        - it should respond with a 404 error if <id> is not found
        - it should update the corresponding row for <id>
        - it should require the 'patch:drinks' permission
        - it should contain the drink.long() data representation
    - returns status code 200 and json {"success": True, "drinks": drink}
     where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    body = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        print(f'________________: {drink_is_valid(body)}')
        if drink is None:
            abort(404)

        if drink_is_valid(body):

            drink.title = body['title']

            drink.recipe = json.dumps(body['recipe'])

            drink.update()
            return jsonify({'success': True,
                            'drinks': drink.long()})
    except Exception as e:
        print(e)
        abort(422)



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error, message = "unprocessable"):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": message
                    }), 422

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
      }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
      }), 400


@app.errorhandler(401)
def auth_error(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "autherror_gexam"
      }), 401
