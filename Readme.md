# Python API Development - full-fledged API using FastAPI
-----------
This program example is a social media API created in Python using FastAPI following freeCodeCamp tutorial: https://youtu.be/0sOvCWFmrtA


## Description
This API has nine seperate functions under four categories: Users, Authentication, Posts, Vote.

For now, the API is deployed on Heroku with documentation available on https://fastapi-chris1eev1.herokuapp.com/docs 
However, the Heroku cloud free tier will end somewhere in November 2022 leading to the interruption of the service. 
It would still work on a local machine as demonstrated on the video linked below. 
Type `uvicorn app.main:app` in the command line to run the server (or `uvicorn main:app` from the app folder)


## Technology
Python and its various libraries:
- `fastapi` to build APIs with Python
- `sqlalchemy` Object Relational Mapper (ORM) to work with Python objects instead of writing SQL queries
- `alembic` for database migration
- `pydantic` for data validation and settings management
- `pytest` to write and run tests
- `jose` to provide a method to securely transfer claims (here, using JWS)
...

Postgre SQL

Heroku (cloud deployment)


## Limitations
- just to learn
- heroku not available in few months time


## Examples
**Users:** (1) Create a user with an email and a password. (2) Find a user with a given ID, returns email, id, and 'created at' time stamp.

**Authentication:** In order to have access to all API request options, a user must log in using their email and password. 

**Posts:** (1) Get all posts available on the database, will return post content, title, id, and 'created at' time.(2) Get one post on the platform by giving post ID. 
(3) Create post by providing title and content. (4) Update post by providing post ID, and then title and/or content. (5) Delete post by providing post ID.

**Vote:** (1) Vote (= like) a post by providing the post ID.


## Video