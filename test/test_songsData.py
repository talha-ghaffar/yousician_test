import unittest
import os
from app import app
import json
from config import client
import copy

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


#### tests ####

    def test_get_initial_response(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_get_songs(self):
        response = self.app.get('/songs',content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/songs/?abc=2',content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/songs/',content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_avg_diff(self):
        response = self.app.get('/songs/avg/diff/?level=9',content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/songs/avg/diff/',content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/songs/avg/diff/?level=2',content_type='application/json')
        self.assertEqual(response.status_code, 500)


    def test_song_search(self):
        response = self.app.get('/songs/search/?message=the',content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/songs/search/?message=THE',content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/songs/search/?message=tHe',content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/songs/search/?message=xzxz',content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/songs/search/?message=',content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/songs/search/',content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/songs/avg/diff/',content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/songs/avg/diff/?level=2',content_type='application/json')
        self.assertEqual(response.status_code, 500)


    def test_add_rating(self):
        sample_song = self.app.get('/songs',content_type='application/json')
        sample_id = sample_song.json[0]['_id']['$oid']
        vals = {
            "song_id":sample_id,
            "rate":3
        }
        response = self.app.post('/songs/rating',data = json.dumps(vals),content_type='application/json')
        self.assertEqual(response.status_code, 200)

        id_missing_vals = copy.deepcopy(vals)
        id_missing_vals['song_id'] = ''
        response = self.app.post('/songs/rating',data = json.dumps(id_missing_vals),content_type='application/json')
        self.assertEqual(response.status_code, 400)

        rating_missing_vals = copy.deepcopy(vals)
        rating_missing_vals['rate'] = None
        response = self.app.post('/songs/rating',data = json.dumps(rating_missing_vals),content_type='application/json')
        self.assertEqual(response.status_code, 400)

        bad_rating_vals = copy.deepcopy(vals)
        bad_rating_vals['rate'] = 6
        response = self.app.post('/songs/rating',data = json.dumps(bad_rating_vals),content_type='application/json')
        self.assertEqual(response.status_code, 400)

        invalid_song_id_vals = copy.deepcopy(vals)
        invalid_song_id_vals['song_id'] = str(sample_id[::-1])
        response = self.app.post('/songs/rating',data = json.dumps(bad_rating_vals),content_type='application/json')
        self.assertEqual(response.status_code, 400)



        #response = self.app.post('/api/v1/create',content_type='application/json')
        #self.assertEqual(response.status_code, 400)

 
if __name__ == "__main__":
    unittest.main()