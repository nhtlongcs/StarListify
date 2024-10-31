import os
import pandas as pd
from tqdm import tqdm
import dotenv
import argparse
from gh_list import ListHandler

dotenv.load_dotenv()

def get_env_variable(var_name, error_message):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(error_message)
    return value

def load_data(username):
    star_listified_path = f'star_listified_{username}.csv'
    topics_path = f'topics_{username}.csv'
    df = pd.read_csv(star_listified_path)
    gh_desc = pd.read_csv(topics_path).set_index('title')['description'].to_dict()
    return df, gh_desc

def create_and_populate_lists(df, gh_desc, list_handler, reset_lists):
    available_lists = list_handler.available_lists(raw=True)
    print(f'There are {len(available_lists)} star lists available in your account.')
    print(f'The limit is 32 lists per account.')
    print(f'You have {32 - len(available_lists)} lists left.')
    print(f'You have {len(df["listified"].unique())} lists to create.')
    print(f'Please make sure that you have enough lists left.')
    input('Press Enter to continue...')
    if reset_lists:
        print('This will reset all lists. Be careful!')
        input('Press Enter to continue...')
        for listname in available_lists:
            print(f'Deleting list {listname} ...')
            list_handler.delete_list(listname)
        print('All lists have been deleted.')
    

    df['repo'] = df['repo_owner'] + '/' + df['repo_name']
    for listname, group in df.groupby('listified'):
        repos = group['repo'].tolist()
        status = list_handler.create_list(name=listname, desc=gh_desc[listname])
        if status:
            print(f'Creating list {listname} ... ')
            add_repos_to_list(repos, listname, list_handler)
        else:
            print(f'Error creating list {listname}, check your cookie and username again')
            print('Maybe not enough space left')
    
def add_repos_to_list(repos, listname, list_handler):
    success_repos = []
    for repo in tqdm(repos):
        try:
            list_handler.add_repo(repo, listname)
            success_repos.append(repo)
        except Exception as e:
            print(f'Error adding {repo} to {listname}: {e}')
            print('Maybe the repo is broken')
            print('Skipping...')
    print(f'Added {len(success_repos)} repos to {listname}')

def main(reset_lists=False):
    username = get_env_variable('GH_USER_ID', 'Please set the GH_USER_ID environment variable')
    cookie = get_env_variable('GH_COOKIE', 'Please set the GH_COOKIE environment variable')
    
    df, gh_desc = load_data(username)
    list_handler = ListHandler(user=username, cookie=cookie)
    
    create_and_populate_lists(df, gh_desc, list_handler, reset_lists)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update GitHub star lists.')
    parser.add_argument('--reset', action='store_true', help='Reset all existing lists before creating new ones')
    args = parser.parse_args()

    main(reset_lists=args.reset)