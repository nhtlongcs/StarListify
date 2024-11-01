import os 
import dotenv
import argparse
import numpy as np
import pandas as pd
from .utils import find_latest_file
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()

def load_data(username):
    df = pd.read_csv(find_latest_file(username))
    topic_df = pd.read_csv(f'topics_{username}.csv')
    return df, topic_df

def compose_repo_text(row):
    return f'<Repo name> {row["repo_name"]} <Topics> {row["topics"]} <Content> {row["readme_content"]}'

def compose_topic_text(row):
    return f'<Title> {row["title"]} <Description> {row["description"]}'

def add_all_text_columns(df, topic_df):
    df['AllText'] = df.apply(compose_repo_text, axis=1)
    topic_df['AllText'] = topic_df.apply(compose_topic_text, axis=1)

def encode_texts(model, df, topic_df):
    repo_vec = model.encode(df['AllText'].to_list(), normalize_embeddings=True)
    topic_vec = model.encode(topic_df['AllText'].to_list(), normalize_embeddings=True)
    return repo_vec, topic_vec

def calculate_scores(repo_vec, topic_vec):
    return repo_vec @ topic_vec.T

def assign_listified_topics(df, topic_df, indices):
    df['listified'] = df.apply(lambda x: [topic_df.iloc[i]['title'] for i in indices[x.name]][0], axis=1)

def save_to_csv(df, username):
    selected_columns = ['repo_owner', 'repo_name', 'listified', 'topics']
    df[selected_columns].to_csv(f'star_listified_{username}.csv', index=False)

def main(model_name):
    username = os.getenv('GH_USER_ID', None)
    df, topic_df = load_data(username)
    add_all_text_columns(df, topic_df)
    
    model = SentenceTransformer(model_name, trust_remote_code=True)
    repo_vec, topic_vec = encode_texts(model, df, topic_df)
    
    score = calculate_scores(repo_vec, topic_vec)
    indices = np.argsort(-score, axis=1)
    
    assign_listified_topics(df, topic_df, indices)
    save_to_csv(df, username)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Categorize GitHub stars.')
    parser.add_argument('--model', type=str, default='dunzhang/stella_en_400M_v5', help='SentenceTransformer model name')
    args = parser.parse_args()
    main(args.model)