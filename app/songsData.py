from app import app
from config import client, DB_NAME
from bson.json_util import dumps
from flask import request, jsonify
from pymongo import MongoClient
import json
import sys
import ast
from bson import ObjectId, json_util


db = client[DB_NAME]

@app.route('/')
def ping_server():
    """
    Default Route to check if the application is working
    """
    message = {
        'message': 'YOUSICIAN - Your Personal Music Teacher.',
        'status': '200'
    }
    return jsonify(message)


@app.route('/songs')
def get_stored_songs():
    """
    Returns a list of songs with the data provided
    """
    try:
        _songs = db.song_tb.find()
        songs = json.loads(json_util.dumps(_songs))
        return jsonify(songs), 200
    except:
        return "Error", 500
    finally:
        if type(db)==MongoClient:
            db.close()


@app.route('/songs/avg/diff/')
def avg_diff():
    """
    Returns the average difficulty for all songs.
    Takes an optional parameter "level" to filter for only songs from a specific level.
    """
    try:
        condition = {}
        level = request.args.get('level')

        if level:
            condition['level'] = int(level)
        else:
            level = 'N/A'

        _avg_difficulty = db.song_tb.aggregate([
            {'$match': condition},
            {'$group': {'_id': '_id', 'avg_diff': {'$avg': '$difficulty'}}}
        ])
        avg_difficulty = list(_avg_difficulty)

        result = {
            "level": level,
            "average_difficulty": avg_difficulty[0]["avg_diff"]
        }
        return jsonify(result), 201
    except:
        return 'Error', 500
    finally:
        if type(db) == MongoClient:
            db.close()


@app.route('/songs/search/')
def song_search_by_string():
    """
    Returns a list of songs matching the search string.
    Takes a required parameter "message" containing the user's search string.
    The search take into account song's artist and title.
    The search case insensitive.
    """

    try:
        message = request.args.get('message')

        if not message:
            return 'No search string provided', 400
        else:
            _songs = db.song_tb.find({"$or":[ {'title': {"$regex" : message, "$options": "$i"}}, {'artist': {"$regex" : message, "$options": "$i"}} ]})
            songs = json.loads(json_util.dumps(_songs))
            if songs:
                return jsonify(songs), 200
            else:
                return 'No song found for the message provided', 404
    except:
        return 'Error', 500
    finally:
        if type(db) == MongoClient:
            db.close()


@app.route('/songs/rating', methods=['POST'])
def rate_a_song():
    """
    Adds a rating for the given song.
    Takes required parameters "song_id" and "rating"
    Ratings should be between 1 and 5 inclusive.
    """

    data = request.json
    song_id = None
    rate = None

    for k, v in data.items():
        if k == 'song_id':
            song_id = v
        elif k == 'rate':
            if type(v) == int:
                rate = v
            else:
                return 'Rating must be a Integer Value', 400


    if not song_id or not rate:
        return 'Bad Request. Song Id or Rating is missing', 400
    if rate < 1 or rate > 5:
        return 'Invalid value for rating. Rating can only be 1-5', 400

    try:
        if db.song_tb.count_documents({ '_id': ObjectId(song_id) }, limit = 1) != 0:
            r = db.rating_collection_tb.insert_one({
            "value": rate,
            "song_id": song_id
            })
            return 'Rating Added', 200

        else:
            return 'Song Id not found', 404

    except:
        return 'Error', 500
    finally:
        if type(db) == MongoClient:
            db.close()


@app.route('/songs/rating_analytics/')
def avg_rate():
    """
    Returns the average, the lowest and the highest rating of the given song id.
    """

    try:
        condition = {}
        song_id = request.args.get('songid')
        if song_id:
            condition['song_id'] = song_id
        else:
            return "Song ID not provided", 400

        _songs = db.rating_collection_tb.aggregate([
            {'$match': condition},
            { "$group": {"_id": "_id", "max_rate": { "$max": "$value" }, "min_rate": { "$min": "$value" }, "avg_rate": { "$avg": "$value" } }}
        ])

        analytics = list(_songs)
        if not analytics:
            return 'No rating records found for song id', 404
        result = {
            "song_id": song_id,
            "max rate": analytics[0]["max_rate"],
            "min rate": analytics[0]["min_rate"],
            "avg rate": analytics[0]["avg_rate"],
        }
        return jsonify(result), 201

        resp = dumps(_songs)
        return resp
    except:
        return 'Error', 500
    finally:
        if type(db) == MongoClient:
            db.close()