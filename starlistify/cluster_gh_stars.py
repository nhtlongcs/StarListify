import os
import re
import rich
import dotenv
import argparse
import pandas as pd
from .utils import find_latest_file

dotenv.load_dotenv()

def load_user_preferences(preference=None, use_reference=False):
    if preference is None:
        print("No preference provided. Using default preference.")
        print("You can provide your preferences using the --preferences argument.")
        preference = """
        I prefer topic bit more detailed, diverse, like career, research, softskills, personal finance, productivity etc. 
        Please create 2 topic named 'life-long learning' and 'life-logging' caused im researching on it.
        life-logging should include ego-centric data, knowledge graph, temporal graph, user intent understanding, nlp extraction/ named entity recognition related topics.
        I am a competitive programmer, so include topics like algorithms, data structures.
        Include a interview preparation topic, include topics like system design, leetcode, behavioral questions.
        """
    if use_reference:
        from gh_list import ListHandler
        cookie = os.getenv('GH_COOKIE', None)
        username = os.getenv('GH_USER_ID')
        assert cookie is not None, 'Please set the GH_COOKIE environment variable to use this feature.'
        lh = ListHandler(user=username, cookie=cookie)
        references = lh.available_lists(raw=True)
        preference += f"\n\nReference: {references} This is a reference to create new topics. Please create new topics based on this reference. Do not copy the reference."
    return preference

def get_github_username():
    return os.getenv('GH_USER_ID', None)

def get_latest_file(username):
    return find_latest_file(username)

def load_topics_from_file(filename):
    df = pd.read_csv(filename)
    return df['topics'].dropna().str.split(',').explode().str.strip().tolist()

def get_gemini_response(prompt):
    import google.generativeai as genai
    model_name = "gemini-1.5-flash"
    model_version = "002"
    system_instruction = "You are a helpful assistant."
    api_key = os.getenv("GENAI_KEY")
    assert api_key, "Please set the GENAI_KEY environment variable."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(f"{model_name}-{model_version}", system_instruction=system_instruction)
    generation_config = {"temperature": 0.25}
    
    return model.generate_content(prompt, generation_config=generation_config).text

def parse_response(response):
    pattern = re.compile(
        r"\[start\]\s*Topic id: (\d+)\s*Topic title: (.*?)\s*Topic description: (.*?)\s*Highlighted keywords: (.*?)\s*Reasoning: (.*?)\s*\[end\]",
        re.DOTALL
    )
    matches = pattern.findall(response)
    return [
        {
            "id": int(match[0]),
            "title": match[1].strip(),
            "description": match[2].strip(),
            "keywords": match[3].strip(),
            "reasoning": match[4].strip()
        }
        for match in matches
    ]

def save_topics_to_csv(parsed_data, username):
    df_topics = pd.DataFrame(parsed_data)
    df_topics.to_csv(f'topics_{username}.csv', index=False)

def main(preferences=None, use_reference=False):
    

    username = get_github_username()
    assert username is not None, 'Please set the GH_USER_ID environment variable.'
    filename = get_latest_file(username)
    topics = load_topics_from_file(filename)
    preference = load_user_preferences(preferences, use_reference)

    prompt = f"""\n\nGiven the keywords {topics}, cluster them into topics with high-level meaning.
    User Preference: {preference}.
    Return minimum 3 and maximum 25 topics.
    Then, for each topic, provide your final prediction in the format:
    [start]
    Topic id: [id]
    Topic title: [icon][title][title length <= 32 characters]
    Topic description: [details][topic description length <= 160 characters]
    Highlighted keywords: [name 3-5 keywords]
    Reasoning: [A brief summary of your reasoning]
    [end]
    ----------------------------------------
    """
    
    response = get_gemini_response(prompt)
    parsed_data = parse_response(response)
    rich.print(parsed_data)
    save_topics_to_csv(parsed_data, username)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster GitHub stars into topics.")
    parser.add_argument('--preferences', type=str, help='Your preferences for topics generation.')
    parser.add_argument('--use-reference', action='store_true', help='Use reference lists from GitHub.')
    args = parser.parse_args()
    main(args.preferences, args.use_reference)
