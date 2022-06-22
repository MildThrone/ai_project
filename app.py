from checker_v2 import similarity_rating
from extensions import *

# from models import Test, User, Role


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_SALT')
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    course = db.Column(db.String(255))
    code = db.Column(db.String(20), unique=True)
    test_file = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, author, course, code, filename):
        self.author = author
        self.course = course
        self.code = code
        self.test_file = filename

    def persist(self):
        db.session.add(self)
        db.session.commit()
        print("persisted")
        self.create_file()

    def create_file(self):
        file = open("{0}/{1}".format(os.getenv('TESTS_PATH'), self.test_file), 'w')
        file.write(json.dumps(request.json['questions']))

        file.close()


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    student = db.Column(db.String(50))
    score = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, code, student, score):
        self.code = code
        self.student = student
        self.score = score

    def persist(self):
        db.session.add(self)
        db.session.commit()


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    confirmed = db.Column(db.DateTime)
    roles = db.relationship('Role',
                            secondary=user_roles,
                            backref=db.backref('users',
                                               lazy='dynamic'),
                            )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify(self, password):
        print(self.password)
        found = self.query.filter_by(email=self.email).first()
        if found:
            if check_password_hash(found.password, password):
                # print("Passwd match")
                self.name = found.name
                return True
            else:
                # print("Passwd no match")
                return False
        else:
            print("User not found")
            return False

    def persist(self):
        db.session.add(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))


db.create_all()


#
#   Decorators
#
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1]
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
                session['user'] = data['user']
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 403

        except BaseException as error:
            return jsonify({'error': str(error)}), 403

        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1]
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
                session['student'] = data['student']
                session['code'] = data['code']
            except jwt.InvalidTokenError as e:
                print(str(e))
                return jsonify({'error': 'Invalid token'}), 403

        except BaseException as error:
            print(str(error))
            return jsonify({'error': "Backend error"}), 403

        return f(*args, **kwargs)
    return decorated


#
# App Routes
#


"""
    Request structure:
        {
            "student": "student details",
            "code": "test code"
        }
"""


@app.route('/', methods=['POST'])
def index():
    student = request.json['student']
    code = request.json['code']

    found = Result.query.filter_by(student=student).first()
    if found and code == found.code:
        return make_response(
            jsonify({
                "message": "Test already taken by student",
                "student": found.student,
                "score": found.score,
                "date": found.date
            }),
            201
        )
    else:
        # generate jwt for student taking the test
        token = jwt.encode({'student': student,
                            'code': code,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
                           app.config['SECRET_KEY'])

        return make_response(
            jsonify({
                "message": "test available",
                "token": token
            }),
            200
        )


"""
    Request structure:
    {
        "name":"Janet B",
        "email": "janet@hmail.com",
        "password": "password",
        "conf_passwd": "password"
    }
"""


@app.route('/register', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    conf_pass = request.json['conf_passwd']
    if password != conf_pass:
        return make_response(
            jsonify(
                {'message': 'Passwords do not match'}
            ),
            215
        )
    else:
        user = User(name, email, password)
        user.persist()
        return make_response(
            jsonify(
                {'message': 'Success'}
            ),
            200
        )


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    user = User(name="guest", email=auth.username, password=auth.password)
    if user.verify(auth.password):
        token = jwt.encode({'user': auth.username,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
                           app.config['SECRET_KEY'])
        return make_response(
            jsonify({
                'token': token,
                'message': 'user logged in'
            }),
            200
        )
    else:
        return make_response(
            jsonify({
                'message': 'user login failed'
            }),
            201
        )


"""
    Request structure:
    {
        "author": "James Webb",
        "course":"AI",
        "code":"CA1004",
        "questions":{
            "1":["question", "answer", 5],
            "2":["question2", "answer2", 5],
            "3":["question3", "answer3", 5],
            "4":["question4", "answer4", 5]
        }    
    }
"""


@app.route('/create-test', methods=['POST'])
@token_required
def create_test():
    code = request.json['code']
    print(code)
    found = Test.query.filter_by(code=code).first()
    if found:
        return jsonify({
            'error': 'test code exists'
        }), 409
    else:
        test = Test(request.json["author"], request.json["course"], request.json['code'],
                    filename="{0}.txt".format(request.json['code']))
        test.persist()
        return jsonify({
            'message': 'test uploaded'
        }), 200


questions = {}
answers = {}
marks = {}


@app.route('/get-test/<string:code>')
@student_required
def get_test(code):
    with open("{0}/{1}.txt".format(os.getenv('TESTS_PATH'), code), 'r') as handle:
        parsed = json.load(handle)

    session['code'] = code
    session['score'] = 0

    for i in parsed:
        questions[i] = parsed[i][0]
        answers[i] = parsed[i][1]
        marks[i] = parsed[i][2]
    return jsonify({'questions': questions}), 200


"""
    Request structure:
    {
        "num_id": 1,
        "answer": "answer",
        "end": "False|True"
    }
"""


@app.route('/answer', methods=['POST'])
@student_required
def answer():
    user_answer = request.json['answer']
    q_no = request.json['num_id']

    mark = similarity_rating(answers.get(q_no), user_answer)

    print(answers.get(q_no))
    print(user_answer)
    print(mark)
    print(marks.get(q_no))
    print(marks)
    print(answers.keys())
    print(answers)
    print(marks.keys())
    if mark >= 0.9:
        mark = round(1 * marks[q_no])
    elif mark >= 0.85:
        mark = 0.85 * marks[q_no]
    elif mark >= 0.7:
        mark = 0.5 * marks[q_no]
    else:
        mark = 0

    session['score'] += mark

    if request.json['end']:
        result = Result(session['code'], session['user'], session['score'])
        result.persist()

    return make_response(
        jsonify({
            "score": mark
        }),
        200
    )


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return make_response(
        jsonify({
            "message": "logged out successfully"
        }),
        200
    )


if __name__ == '__main__':
    db.create_all()
    app.run()
