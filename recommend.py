import pandas as pd

def recommender_sigmoid_kernel(title, sig, df, anime_indices):
    idx = anime_indices[title]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1: 11]
    indices = [i[0] for i in sig_scores]
    return df['title_en'].iloc[indices]

def recommender_nearest_neighbors(title, df, model):
    data = df[df['title_en'] == title].drop('title_en', axis=1)
    n_neighbors_idx = model.kneighbors(data.values, return_distance=False)
    return df['title_en'].iloc[n_neighbors_idx[0]]