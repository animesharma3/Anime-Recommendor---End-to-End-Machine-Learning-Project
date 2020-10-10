# Importing Necessary Libraries
from flask import Flask, render_template, request
from recommend import recommender_sigmoid_kernel, recommender_nearest_neighbors
import requests
import numpy as np
import pandas as pd
import pickle
import random

# Loading the datasets
df_population = pd.read_csv('anime_population.csv')
df_sample = pd.read_csv('anime_sample.csv')
anime_indices = pd.Series(df_sample.index, index=df_sample['title_en'])

# Loading necessary files
sig = pickle.load(open('sig.pkl', 'rb'))
file2 = open('model.pkl', 'rb')
model = pickle.load(file2)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<title>', methods=['POST', 'GET'])
def recommend(title):
    title = request.form['title'].strip()

    # Nearest Neighbors Recommendation System
    titles_nn = recommender_nearest_neighbors(title, df_population.drop(['Unnamed: 0', 'created_at', 'description', 'title_en_jp', 'title_ja_jp', 'poster_image', 'age_rating', 'age_rating_guide', 'show_type', 'status'], axis=1), model)

    # NLP Based Recommendation System
    try:
        titles_sk = recommender_sigmoid_kernel(title, sig, df_sample, anime_indices)
    except KeyError as e:
        titles_sk = []

    if len(titles_sk) != 0:
        titles = pd.concat([titles_sk, titles_nn], axis=0).drop_duplicates().values
    else:
        titles = titles_nn.values
    for t in titles:
        if t == title:
            continue
        try:
            poster_img = df_population[df_population['title_en'] == t]['poster_image'].values
        except:
            poster_img = ''
    animes.append([t, poster_img])

    # Data to send to front-end - animes, title, description, poster image, streaming link(if any)
    animes = []
    try:
        description = df_population[df_population['title_en'] == title]['description'].values
        poster_image = df_population[df_population['title_en'] == title]['poster_image'].values
    except KeyError as e:
        if e.args[0] == 'description':
            description = 'No Descripition Provided'
        elif e.args[0] == 'poster_img':
            poster_image = ''
    try:
        stream_link = requests.get('https://kitsu.io/api/edge/anime/{}/streaming-links'.format(df_population[df_population['title_en']==title].index.values[0])).json()['data'][0]['attributes']['url']
    except:
        stream_link = ''
    return render_template('recommend.html', animes=animes, title=title, description=description, poster_image=poster_image, stream_link=stream_link)

if __name__ == "__main__":
    app.run(debug=True)
