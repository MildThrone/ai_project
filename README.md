# Auto Answer Checker

## Task Summary

Design an automatic answer checker application that checks and marks written
answers similar to a human being. This software application is to check subjective
answers in an online examination and allocate marks to the user after verifying the
answer. The system requires you to store the original answer for the system. This
facility is provided to the admin. The admin may insert questions and respective
subjective answers in the system. These answers are stored as notepad files. When
a user takes the test, he/she is provided with questions and area to type his
answers. Once the user enters his/her answers the sy stem then compares this
answer to original answer written in database and allocates marks accordingly.
Both the answers need not be exactly same word to word. The system should
consist of in-built artificial intelligence sensors that verify answers and allocate
marks accordingly as good as a human being.

## Design Process

The application is broken into 3 parts: 
  1. Frontend
  2. Backend and 
  3. AI module

The frontend is built in React, Flask for the backend and the AI module implemented in Google Colab and converted into a 
Python package used in the backend. Communication between the backend and frontend employed JSON to send and receive requests/responses.

Tasks were split among team members according to area of expertise.

## AI Module

The AI module uses Natural Language Processing to determine the similarity between the answer provided by the admin or 
staff and the answer enterred by the student via the frontend. 
Sentence Transformers and pretrained models were employed as the NLP tools to compare the sentences.

The logic follows this:
  1. Take two sentences and convert them into vectors
  2. Find the smallest distance (Euclidean) or smallest angle (cosine similarity) between the sentence vectors

Thus, a measure of the semantic similarity between is then produced which is used to score the answer enterred by the student.

### Checker Package

The Checker package is the heart of the answer comparing system. The package uses the 
[bert-base-nli-mean-tokens](https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens) model.

The performance of the model was satisfactory during testing but as the model is currently deprecated, a v2 of Checker was implemented.

### Checker v2 Package

The second version of the checker package, checker_v2, was implemented using the newer 
[all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) model.

This model has the highest average performance among [the pretrained NLP models](https://www.sbert.net/docs/pretrained_models.html).

## Backend

The backend is built in Python's Flask framework. MariaDB is set up as the database for the entire backend. The backend uses an 
Object-Relational Mapper provided by SQLAlchemy to handle translation of the classes to tables in the database.

The backend implements 3 core classes: 
  1. User
  2. Test
  3. Result

Other classes were implemented as they were necessary to full functionality of the core classes.

The User class is intended to be used by the admins (or staff) of the service rather than the students. This design choice was made 
from a user experience perspective; students taking tests on the site reqiure only their unique id and the unique test code provided 
by their test administrator.

### User class

The User class is designed to handle abstraction of administrators on the site.

The user class has the following attributes:
  1. name
  2. email
  3. password
  4. created
  5. confirmed
  6. roles

Functions to verify the existence of users and also persist new users were implemented with appropriate names.

The password is hashed upon creation of each user using werkzeug.security's `generate_password_hash` function. 
Using the `check_password_hash` function from the werkzeug.security package, existing users are verified and logged in.

### Test class

The Test class is designed to handle abstraction of tests administered through the site. The class implements a function 
to store the test questions, answers and associated marks in a text file with the files named according to the unique 
test code assigned by the administrator.

The test class has the following attributes:
  1. author
  2. course
  3. code
  4. test_file
  5. date_created

### Result class

Result handles the results of tests taken by the students on the site. This class has functions to persist the results of 
the tests taken to the database.

This class has the following attributes:
  1. code
  2. student
  3. score
  4. date


## Authentication and Authorization

2 forms of authentication were used in the backend to control access to administrators and the students taking the tests. 
Administrators are controlled using JWT-based authentication while students are authenticated via a session-based system.

## Endpoints

The application backend has 7 endpoints available to the frontend. 

### Index

Endpoint: `\`

Request Structure:
```
{
    "student": "student details",
    "code": "test code"
}
```

Response Structure:
```
Status code: 201
{
    "message": "Test already taken by student",
    "student": "10505050",
    "score": 5,
    "date": "Year-month-day"
}
```

```
Status code: 200
{
    "message": "success"
}
```

### Register

Endpoint: `/register`

Request Structure:
```
{
    "name":"Janet B",
    "email": "janet@hmail.com",
    "password": "password",
    "conf_passwd": "password"
}
```

Response Structure:
```
Status code: 215
{
    'message': 'Passwords do not match'
}
```

```
Status code: 200
{
    'message': 'Success'
}
```

### Login
Endpoint: `/login`

Login details are required and passed in the authentication headers.

```
  username = email
  password = password
```

Response Structure:
```
Status code:200
{
    'token': token,
    message': 'user logged in'
}
```

```
Status code: 201
{
    'message': 'user login failed'
}
```

### Create-test

Endpoint: `/create-test`

Request Structure:
```
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
```

Response Structure:
```
Status code: 409
{
   "error": "test code exists"
}
```

```
Status code: 200
{
    "message": "test uploaded"
}
```

### Get-test

Endpoint: `/get-test/<string:code>`

Response Structure:
```
Status code: 200
{
    "questions": {
        "1": "question",
        "2": "question2",
        "3": "question",
        "4": "question2"
    }
}
```

### Answer

Endpoint: `/answer`

Request Structure:
```
{
    "num_id": 1,
    "answer": "answer",
    "end": "False|True"
}
```

Response Structure:
```
Status code: 200
{
    "score": 5
}
```

### Logout

Endpoint: `/logout`

Response Structure:
```
Status code: 200
{
    "message": "logged out successfully"
}
```
