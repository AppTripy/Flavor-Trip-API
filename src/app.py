from flask import Flask, request, jsonify, make_response
import bcrypt
from prisma import Client
from flasgger import Swagger 
from flask_cors import CORS


app = Flask(__name__)
app.config['DEBUG'] = True  ## Makes server reload when changing the code



# Access to XMLHttpRequest at 'http://127.0.0.1:5000/login' from origin 'http://localhost:19006' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
# Fix the above error --|
CORS(app)



## Swagger config
app.config['SWAGGER'] = {
    'title': 'Flavor Trip API',
    'description':'<div style="color:white;font-size: 30px; font-weight: 900;margin-top:70px;margin-top:50px;background-color:#0284c7;padding:10px 10px;" > Flavor Trip</div>',
    "termsOfService": None,
    'version':'0.1',
    'uiversion': 3,
}
swagger = Swagger(app)



## Prisma ORM instance
prisma = Client()





# Home route
@app.route('/', methods=['GET'])
def up():
    """Checks if server is up
    ---
    tags: 
        - Dev
    responses:
        200:
          description: Server up.
        400:
          description: Server down.
    """
    return make_response(jsonify( {'info':'server ready'} ), 400)




# Get list of users || FOR DEV MODE ONLY
@app.route('/users', methods=['GET'])
async def users() :
    """Get list of users
    Route for DEV mode only.
    ---
    tags: 
        - Dev
    responses:
        200:
          description: Ok
          content:
            application/json:
              schema:
                type: array
        400:
          description: Bad request. Error during handling request
    """
    try : 
        await prisma.connect()
        userz = await prisma.users.find_many()
        await prisma.disconnect()
        res = []
        for user in userz :
            res.append({'username':user.username,'password':user.password})
        return make_response(jsonify( res ), 200)
    except :
        return make_response(jsonify( {'info':'GET /users error'} ), 400)







# Login route
@app.route('/login', methods=['POST'])
async def login():
    """Log in a user
    ---
    tags: 
        - User
    parameters:
        - in: body
          name: user
          description: The user to create.
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
              password:
                type: string
            example:
                username: simo
                password: Azerty
              
    responses:
        200:
          description: Log in success/fail
          content:
            application/json:
              schema:
                type: array
        400:
          description: Bad request. Error during handling request
    """
    try :
        # Get username and password from the request
        username = request.json['username']
        password = request.json['password']
        
        # Connect to db
        await prisma.connect()
        user = await prisma.users.find_unique(
            where={
                'username':username,
            },
        )
        await prisma.disconnect()

        if (user) : ## Exisitng username
            if (user.password == password) :
                return make_response(jsonify( {'info':'login success'} ), 200)
            else :
                return make_response(jsonify( {'info':'wrong password'} ), 201)
        else : ## Username don't exist
            return make_response(jsonify( {'info':'username not found'} ), 202)
        
    except :
        return make_response(jsonify( {'info':'login error'} ), 400)






# Signup route
@app.route('/signup', methods=['POST'])
async def signup():
    """Register a user
    ---
    tags: 
        - User
    parameters:
        - in: body
          name: user
          description: The user to register.
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
              password:
                type: string
            example:
                username: newuser
                password: Azerty
              
    responses:
        200:
          description: Log in success/fail
          content:
            application/json:
              schema:
                type: array
        400:
          description: Bad request. Error during handling request
    """
    try :
        # Get username and password from the request
        username = request.json['username']
        password = request.json['password']
        
        # Connect to db
        await prisma.connect()
        userExist = await prisma.users.find_unique(
            where={
                'username':username,
            },
        )
        
        if (userExist) : ## Exisitng username
            await prisma.disconnect()
            return make_response(jsonify( {'info':'username exist'} ), 201)
        else : ## Register username
            print('New user')
            newUser = await prisma.users.create(
                data={
                    'username': username,
                    'password': password,
                },
            )
            await prisma.disconnect()

            if (newUser) :
                return make_response(jsonify( {'info':'register sucess'} ), 200)
            else :
                return make_response(jsonify( {'info':'register fail'} ), 202)
        
    except Exception as e :
        print(e)
        return make_response(jsonify( {'info':'login error'} ), 400)




@app.route('/user/delete', methods=['DELETE'])
async def delete() :
    """Delete a user
    ---
    tags: 
        - User
    parameters:
        - in: body
          name: user
          description: The user to delete.
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
              password:
                type: string
            example:
                username: newuser
                password: Azerty
              
    responses:
        200:
          description: Log in success/fail
          content:
            application/json:
              schema:
                type: array
        400:
          description: Bad request. Error during handling request
    """
    try :
        username = request.json['username']
        
        # Connect to db
        await prisma.connect()
        userDelete = await prisma.users.delete(
            where={
                'username':username,
            },
        )
        await prisma.disconnect()

        if (userDelete) :
            return make_response(jsonify( {'info':'delete success'} ), 200)
        else :
            return make_response(jsonify( {'info':'delete fail'} ), 200)

    except Exception as e :
        print(e)
        return make_response(jsonify( {'info':'delete error'} ), 400)








if __name__ == '__main__':
    app.run(port=5000)
    