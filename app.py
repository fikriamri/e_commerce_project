from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
import logging, sys
from blueprints import app, manager
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

## Initiate flask-restful instance
api = Api(app, catch_all_404s=True)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        ## Define log format and create a rotating log with max size of 10mb and max backup up to 10
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s") # %s itu untuk format seperti .format
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=10000, backupCount=10) # '../storage/log/app.log' mundur satu folder karena 'app' pindah ke dalam blueprints/__init__.py / Bisa juga dengan memindahkan folder storage 
        log_handler.setLevel(logging.NOTSET)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        ## if you want to jsonify 500 error, you cannot. But you can set debug=False
        app.run(debug=False, host='0.0.0.0', port=5020)