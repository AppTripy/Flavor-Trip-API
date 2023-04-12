import requests
import sys
import json

## TEST THE API

# INSERT INTO users (username, password) VALUES ('alice', 'mypassword1'), ('bob', 'mypassword2'), ('charlie', 'mypassword3'), ('david', 'mypassword4');



URL  = 'http://127.0.0.1:5000'

  
try : 
    
  ## python test.py login simo
  if (sys.argv[1]=='login') :
    data = {"username":sys.argv[2],"password":"mypassword1"}
    res = requests.post(URL+'/login', data=json.dumps(data) , headers={'Content-Type': 'application/json'})


  elif (sys.argv[1]=='signup') :
    data = {"username":sys.argv[2],"password":"azerty"}
    res = requests.post(URL+'/signup', data=json.dumps(data) , headers={'Content-Type': 'application/json'})

    

  elif (sys.argv[1]=='users') :
    res = requests.get(URL+'/users')
  
  print(res.text)


except : 
  print("Couldn't try!")


