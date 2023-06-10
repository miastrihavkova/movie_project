from project import app
import unittest
import json

#data and constants for testing
headers = {"Content-Type": "application/json"}
data = [
  {
    "title": "Piráti z Karibiku: Prokletí Černé perly",
    "description": "Akční dobrodružství s kapitánem Jackem Sparrowem a jeho úsilím získat zpět prokletý poklad.",
    "release_year": 2003
  },
  {
    "title": "Matrix",
    "description": "Vědecko-fantastický film, který sleduje příběh Neo, který objevuje, že svět, ve kterém žije, je virtuální realita.",
    "release_year": 1999
  },
  {
    "title": "Pán prstenů: Společenstvo Prstenu",
    "description": "Fantasy epos, který vypráví o dobrodružstvích hobita jménem Frodo a jeho snaze zničit mocný prsten.",
    "release_year": 2001
  },
  {
    "title": "Forrest Gump",
    "description": "Dramatický film, který sleduje příběh Forresta Gumpa, jednoduchého muže s neobyčejným životem.",
    "release_year": 1994
  },
  {
    "title": "Vykoupení z věznice Shawshank",
    "description": "Drama o přátelství mezi dvěma vězni a jejich snaze uniknout ze věznice Shawshank.",
    "release_year": 1994
  }
]

class Test(unittest.TestCase):

    # tests for basic functionality
    ###############################

    # test for successful exit code
    def test_01_status_code(self) -> None:
        tester = app.test_client()
        response = tester.get("/movies")
        result = response.status_code
        self.assertEqual(result, 200)

    # test for json format of output content
    def test_02_content(self) -> None:
        tester = app.test_client()
        response = tester.get("/movies")
        self.assertEqual(response.content_type, "application/json")

    # test for posting first movie
    def test_03_post_first_movie(self) -> None:
        tester = app.test_client()
        response = tester.post("/movies", data=json.dumps(data[0]), headers=headers)
        check = list(data[0].values())
        check.insert(0, 1)
        assert response.json == check

    # test for posting all movies with id check
    def test_04_post_all_movies(self) -> None:
        tester = app.test_client()
        for i in range(1, len(data)):
            response = tester.post("/movies", data=json.dumps(data[i]), headers=headers)
            check = list(data[i].values())
            check.insert(0, i + 1)
            assert response.json == check

    # test for getting all movies
    def test_05_get_all_movies_(self) -> None:
        tester = app.test_client()
        check = [list(dictionary.values()) for dictionary in data]
        for i in range(len(check)):
            check[i].insert(0, i + 1)
        response = tester.get("/movies")
        assert response.json == check

    # test for getting single movie
    def test_06_find_movie(self) -> None:
        tester = app.test_client()
        for i in range(len(data)):
            path = "movies/{id}".format(id = i + 1)
            response = tester.get(path)
            check = list(data[i].values())
            check.insert(0, i + 1)
            assert response.json == check

    # test for updating movie
    def test_07_update_movie(self) -> None:
        tester = app.test_client()
        for movie in data:
            movie['description'] = str(movie['description']) + '..'
        check = [list(dictionary.values()) for dictionary in data]
        for j in range(len(check)):
            check[j].insert(0, j + 1)
        for i in range(len(data)):
            path = "movies/{id}".format(id = i + 1)
            response = tester.put(path, data=json.dumps(data[i]), headers=headers)
            assert response.json == check[i]

    # tests for error handling
    ##########################

    # test for invalid id in get by id
    def test_08_invalid_id(self) -> None:
        tester = app.test_client()
        response = tester.get("/movies/4567")
        assert response.status_code == 404

    # test for missing data in post function
    def test_09_incomplete_data(self) -> None:
        tester = app.test_client()
        incomplete = { "title": None, "desciption": None, "release_year": None }
        response = tester.post("/movies", data=json.dumps(incomplete), headers=headers)
        assert response.status_code == 400

    # test for invalid id when updating
    def test_10_invalid_id_for_update(self) -> None:
        tester = app.test_client()
        some_data = { "title": "Movie", "desription": "Nice movie", "release_year": 0 }
        response = tester.put("/movies/4567", data=json.dumps(some_data), headers=headers)
        assert response.status_code == 404

if __name__ == "__main__":
    unittest.main()