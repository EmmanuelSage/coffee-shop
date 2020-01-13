import os
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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    """Get all drinks public endpoint"""

    try:
        # query and format all drinks
        drinks = Drink.query.all()
        formatted_drinks = [drink.short() for drink in drinks]

        # return resonse if successful
        return jsonify({
            'success': True,
            'drinks': formatted_drinks,
        }), 200

    except Exception:
        # return internal server error
        abort(500)

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    """Get the details of a specific drink"""
    try:
        # Query and format drinks
        drinks = Drink.query.all()
        formatted_drinks = [drink.long() for drink in drinks]

        # return long() formatted response
        return jsonify({
            'success': True,
            'drinks': formatted_drinks,
        }), 200

    except Exception:
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    """creates a new drink"""
    try:
        # get response data
        data = request.get_json()
        title = data.get('title', None)
        recipe = data.get('recipe', None)

        # inserts a new drink
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        # return success response
        return jsonify({
            'success': True,
            'drinks': drink.long(),
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


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
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
