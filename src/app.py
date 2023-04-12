from flask import Flask, request, jsonify, make_response
import bcrypt
import asyncio
from prisma import Client
from flasgger import Swagger , swag_from
import tracemalloc
tracemalloc.start()


app = Flask(__name__)
app.config['DEBUG'] = True  ## Makes server reload when changing the code

swagger = Swagger(app)

prisma = Client()






@app.route('/', methods=['GET'])
def home():
    return "Welcome Home"




# Get list of users route  || FOR DEV MODE ONLY
@app.route('/users', methods=['GET'])
async def users() :
    """Get list of users
    Route for DEV mode only.
    ---
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
        # val = []
        # asyncio.run(rr(val))
        # print(val)


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
                return make_response(jsonify( {'info':'wrong password'} ), 200)
        else : ## Username don't exist
            return make_response(jsonify( {'info':'username not found'} ), 200)
        
    except :
        return make_response(jsonify( {'info':'login error'} ), 400)






# Signup route
@app.route('/signup', methods=['POST'])
async def signup():
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
            return make_response(jsonify( {'info':'username exist'} ), 200)
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
                return make_response(jsonify( {'info':'register fail'} ), 200)
        
    except Exception as e :
        print(e)
        return make_response(jsonify( {'info':'login error'} ), 400)




@app.route('/user/delete', methods=['DELETE'])
async def delete() :
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









async def main() :
    # Connecting to database here don't work
    # await prisma.connect()
    
    app.run()



if __name__ == '__main__':
    asyncio.run(main())
    