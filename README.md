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

The backend is built in Python's Flask framework. 

The backend implements 3 core classes: 
  1. User
  2. Test
  3. Result

Other classes were implemented as they were necessary to full functionality of the core classes.

The User class is intended to be used by the admins (or staff) of the service rather than the students. This design choice was made 
from a user experience perspective; students taking tests on the site reqiure only their unique id and the unique test code provided 
by their test administrator.

### User class

The user class uses the following attributes:
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

