README

by Miriam Střihavková (GitHub: https://github.com/miastrihavkova)

content: simple movie database RESTful API using Flask
requirements: python3, Docker
used libraries: flask, sqlite3, json, os, unittest, typing
features: add movie, update movie by id, get movie by id, get all movies

how to run:
- download / clone movie_project folder from GitHub
- open terminal and go to /movie_project
- create image command: "docker build -t movie_app . "
- run command: "docker run -p 5000:5000 movie_app"
- the API should be accessible on localhost:5000

optional:
- open new terminal window
- search for CONTAINER ID of the running container using "docker ps -a"
- now type this command: "docker exec -it <CONTAINER ID> /bin/bash
- to look at the database use: "cat movie_database.db"
- to run unit tests and fill database with data run: "python3 tests.py"

* for further testing API testing client is recommended (HTTPie was used for this project)
* because this solution is dockerized, the database is created within docker container

sources:
- https://www.sqlitetutorial.net/
- https://www.itnetwork.cz/python/flask/seznameni-s-flask-microframeworkem
- https://www.w3schools.com/js/js_json_intro.asp
- https://flask.palletsprojects.com/en/2.3.x/testing/
- https://betterprogramming.pub/how-to-dockerize-your-flask-api-cc95843ab625
