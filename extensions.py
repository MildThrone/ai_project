import os
import json
from flask import Flask, request, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
import datetime
from functools import wraps
import jwt as jwt
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(os.getenv('DB_USER'), os.getenv('DB_PASS'), os.getenv('DB_HOST'),
                                                os.getenv('DB_NAME'))
