#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:16:16 2023

@author: icecold
"""
import requests
import sqlite3
import json

# Retrieve and set your Last.fm API key
with open("config.json") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]

def create_connection():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('lastfm.db')
    return conn

def fetch_albums_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT artist_name, album_title FROM Album')
    return cursor.fetchall()

def insert_jazz_data(conn, album_id, artist_name, album_title, track_title):
    # Prepare an SQL INSERT statement for the Jazz table
    insert_query = '''
    INSERT INTO Jazz (album_id, artist_name, album_title, track_title)
    VALUES (?, ?, ?, ?);
    '''

    # Execute the INSERT statement with jazz data
    cursor = conn.cursor()
    cursor.execute(insert_query, (album_id, artist_name, album_title, track_title))
    conn.commit()

# Make a fresh Jazz table using executescript()
conn = create_connection()  # Call the create_connection function to obtain the database connection
cur = conn.cursor()  # Create a cursor for executing SQL statements

# Make a fresh Jazz table using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Jazz;
CREATE TABLE Jazz (
    album_id  TEXT,
    artist_name TEXT,
    album_title TEXT,
    track_title TEXT
);

''')
input('Pausing to check database table structure')




def get_album_info(artist_name, album_title):
    # Define the Last.fm API endpoint for getting album info
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist={artist_name}&album={album_title}&api_key={API_KEY}&format=json"

    try:
        # Send a GET request to the Last.fm API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and process the album info
            album_info = data.get('album', {})
            album_id = album_info.get('mbid', 'N/A')
            track_list = album_info.get('tracks', {}).get('track', [])

            if album_info:
                for track in track_list:
                    track_title = track.get('name', 'N/A')

                    # Insert jazz data into the database
                    conn = create_connection()
                    insert_jazz_data(conn, album_id, artist_name, album_title, track_title)
                    conn.close()

            else:
                print("No results found for the album info.")
        else:
            print("Failed to retrieve data from Last.fm. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    conn = create_connection()
    albums = fetch_albums_from_db(conn)
    conn.close()  # Close the database connection

    for artist_name, album_title in albums:
        print(f"Fetching info for: {artist_name} - {album_title}")
        get_album_info(artist_name, album_title)