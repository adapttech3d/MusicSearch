#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:32:54 2023

@author: icecold
"""

import requests
import sqlite3
import json

# Retrieving your Last.fm API key
with open("config.json") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]


def create_connection():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('lastfm.db')
    return conn  # Return the database connection

conn = create_connection()  # Call the create_connection function to obtain the database connection
cur = conn.cursor()  # Create a cursor for executing SQL statements

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;


CREATE TABLE Artist (
    artist_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_name    TEXT UNIQUE
);


CREATE TABLE Album (
    album_id  TEXT,
    artist_name  TEXT,
    album_title   TEXT
);


''')
input('Pausing to check database table structure')



def insert_album_data(conn, album_data):
    # Prepare an SQL INSERT statement for the Albums table
    insert_query = '''
    INSERT INTO Album (artist_name, album_title, album_id)
    VALUES (?, ?, ?);
    '''

    # Execute the INSERT statement with album data
    cursor = conn.cursor()
    cursor.execute(insert_query, album_data)
    conn.commit()

def get_top_jazz_albums():
    # Define the Last.fm API endpoint for getting top jazz albums
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopalbums&tag=jazz&api_key={API_KEY}&format=json&limit=101"

    try:
        # Send a GET request to the Last.fm API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a connection to the SQLite database outside the loop
            conn = create_connection()

            # Extract and process the top jazz albums
            if 'albums' in data and 'album' in data['albums']:
                albums = data['albums']['album']
                for album in albums:
                    album_data = (album['artist']['name'], album['name'], album.get('mbid', 'AABBCCDDEE'))

                    # Insert album data into the database
                    insert_album_data(conn, album_data)

                    print("Album Name:", album['name'])
                    print("Artist:", album['artist']['name'])
                    print("Album MBID:", album.get('mbid', 'N/A'))  # Print the album ID
                    print("\n")

                # Close the database connection after processing all albums
                conn.close()
            else:
                print("No results found.")
        else:
            print("Failed to retrieve data from Last.fm. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    get_top_jazz_albums()
