import pandas as pd 
from sentence_transformers import SentenceTransformer
import numpy as np
from utils import find_latest_file
username = 'nhtlongcs'
df = pd.read_csv(find_latest_file(username))
topic_df = pd.read_csv(f'topics_{username}.csv')

def compose(row):
    return f'<Repo name> {row["repo_name"]} <Topics> {row["topics"]} <Content> {row["readme_content"]}'

def compose_topic(row):
    return f'<Title> {row["title"]} <Description> {row["description"]}'

df['AllText'] = df.apply(compose, axis=1)
topic_df['AllText'] = topic_df.apply(compose_topic, axis=1)
model = SentenceTransformer('dunzhang/stella_en_400M_v5', trust_remote_code=True)

repo_vec = model.encode(
    df['AllText'].to_list(), normalize_embeddings=True
)
topic_vec = model.encode(
    topic_df["AllText"].to_list(), normalize_embeddings=True
)
print(repo_vec.shape)
print(topic_vec.shape)

# test_cos_sim_arr = cosine_similarity(test_long_vec, misconception_mapping_vec)
score = repo_vec @ topic_vec.T
indices = np.argsort(-score, axis=1)

df['listified'] = df.apply(lambda x: [topic_df.iloc[i]['title'] for i in indices[x.name][:1]], axis=1)
selected_columns = ['repo_owner', 'repo_name', 'listified', 'topics']
df = df[selected_columns]
df.to_csv(f'star_listified_{username}.csv', index=False)