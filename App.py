#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 10:59:47 2023

@author: IceCold
"""

from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search_lastfm():
    if request.method == 'POST':
        query = request.form['query']

        conn = sqlite3.connect('lastfm.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT artist_name, album_title, track_title
            FROM Jazz
            WHERE
                artist_name LIKE ? OR
                album_title LIKE ? OR
                track_title LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))

        search_results = cursor.fetchall()

        conn.close()

        if search_results:
            return render_template('index.html', search_results=search_results)
        else:
            return render_template('index.html', no_matches=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
