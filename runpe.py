#!flask/bin/python
from app import app
context=('bob.crt', 'bob.key')
#app.run(host='0.0.0.0',port='5000', debug = False)
app.run(host='0.0.0.0',port='5000', debug = False, ssl_context=context)