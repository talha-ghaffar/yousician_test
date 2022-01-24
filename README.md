
# Yousician Backend Test.

To get started: 
1. Clone the repository
2. For running test:
```python
docker-compose docker-compose_test.yml up
```
3. For Running Application:
```python
docker-compose docker-compose up
```

# List of Routes:
A. Returns a list of songs with the data provided by the "songs.json". GET ENDPOINT
```python
/songs
```

B. Returns the average difficulty for all songs. GET ENDPOINT
```python
/songs/avg/diff (for all songs)
/songs/avg/diff/?level=3 (to get for songs of level 3 or use anyother valid number)
```

C. Returns a list of songs matching the search string. GET ENDPOINT
```python
/songs/search/?message=the (for all songs having the in title or artist)
```

D. Adds a rating for the given song. POST ENDPOINT
```python
/songs/rating (takes two parameters as json dict 'song_id' and 'rate')
```

E. Returns the average, the lowest and the highest rating of the given song id.
```python
/songs/rating_analytics/?songid=123 (enter a valid songid replacing 123)
```


You can test the API using postman at `localhost:5000/songs`