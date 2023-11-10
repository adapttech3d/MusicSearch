#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:21:01 2023

@author: icecold
"""

import requests
import json

# Retrieving your Last.fm API key
with open("config.json") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]

def search_lastfm(query):
    # Define the Last.fm API endpoint for search
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={query}&api_key={API_KEY}&format=json"

    try:
        # Send a GET request to the Last.fm API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract and process the search results
            if 'results' in data and 'trackmatches' in data['results']:
                tracks = data['results']['trackmatches']['track']
                for track in tracks:
                    print("Song Name:", track['name'])
                    print("Artist:", track['artist'])
                    print("Album:", track['album'])
                    print("\n")
            else:
                print("No results found.")

        else:
            print("Failed to retrieve data from Last.fm. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    search_query = input("Enter a search query: ")
    search_lastfm(search_query)
