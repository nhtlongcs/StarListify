import rich
import re
from utils import find_latest_file
import pandas as pd
import os 
username = 'nhtlongcs'
filename = find_latest_file(username)
df = pd.read_csv(filename)
topics = df['topics'].dropna().str.split(',').explode().str.strip().tolist()
preference = "I prefer topic bit more detailed, diverse, like career, research, softskills, personal finance, productivity etc. Please create 2 topic named 'life-long learning' and 'life-logging' caused im researching on it."

def gemini_response(prompt):
    import google.generativeai as genai
    # https://aistudio.google.com/app/apikey
    model_name = "gemini-1.5-flash"
    model_version = "002"
    system_instruction = "You are a helpful assistant."
    api_key = os.getenv("GENAI_KEY")
    assert api_key, "Please set the GENAI_KEY environment variable."
    model = genai.GenerativeModel(
        f"{model_name}-{model_version}",
        system_instruction=system_instruction,
    )
    generation_config = {
        "temperature": 0.25,
    }
    genai.configure(api_key=api_key)

    return model.generate_content(
        prompt, generation_config=generation_config
    ).text
# Example usage
prompt = """Given the keywords {topics}, cluster them into topics with high-level meaning.
User Preference: {preferences}.
Return minimum 3 and maximum 25 topics.
Then, for each topic, provide your final prediction in the format:
[start]
Topic id: [id]
Topic title: [title]
Topic description: [details]
Reasoning: [A brief summary of your reasoning]
[end]
----------------------------------------
"""
response = gemini_response(prompt.format(topics=topics, preferences=preference))

# Define regex pattern to parse the log into structured data
pattern = re.compile(
    r"\[start\]\s*Topic id: (\d+)\s*Topic title: (.*?)\s*Topic description: (.*?)\s*Reasoning: (.*?)\s*\[end\]",
    re.DOTALL
)

# Extract data using regex
matches = pattern.findall(response)

# Create a list of dictionaries for the parsed data
parsed_data = [
    {
        "id": int(match[0]),
        "title": match[1].strip(),
        "desc": match[2].strip(),
        "reasoning": match[3].strip()
    }
    for match in matches
]
rich.print(parsed_data)

df_topics = pd.DataFrame(parsed_data)
df_topics.to_csv(f'topics_{username}.csv', index=False)
