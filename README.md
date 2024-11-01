# StarListify

**StarListify** is a Python package that transforms your GitHub stars into an organized, categorized resource, making it easy to browse and access your starred repositories. By fetching starred repositories and extracting key information—like the README content—it sorts them into lists based on custom user preferences or README-inferred topics.

![example.png](./assets/example.jpeg)

> Organizing resources, especially GitHub stars, can become overwhelming. As someone in the field of information retrieval, I've built **StarListify** to help manage my knowledge base, treating my GitHub stars as an integral part of my “second brain.” With this tool, I can categorize starred repositories based on how I use them, creating a streamlined structure that’s efficient and tailored to my needs.

### Example Usage

```bash
starlistify generate --preferences "I prefer my topics to be detailed and diverse, \
including areas like career, research, soft skills, personal finance, productivity, etc. \
As a competitive programmer, I also need topics on algorithms and data structures. \
Minor topics, like game development and robotics, can be excluded."
```


---

## How It Works

1. **Fetch Starred Repositories:** Retrieve starred repositories for a specified GitHub user account.
2. **Generate Categories:** Create lists based on starred repositories and user-defined criteria.
3. **Retrieve Relevant Topics:** Use an embeddings-based model to extract the most relevant topics from each repository's README.
4. **Update GitHub Lists:** Apply the categorized lists directly to your GitHub account.

---

## Installation

If you're new to Python or package management, it's recommended to use Conda to set up a virtual environment and install dependencies:

```bash
conda create -n starlistify python=3.10
conda activate starlistify
pip install -r requirements.txt
pip install -e .
```

---

## Usage 

To use **StarListify**, you’ll need a GitHub account and a few access keys:

- **GitHub Token**: [Create a token](https://graphite.dev/guides/github-personal-access-token) following the official guide.
- **GitHub User ID**: Use your GitHub username.
- **GitHub Stars Cookie**: Follow [these instructions](https://github.com/haile01/github-starred-list?tab=readme-ov-file#-faq) to get the cookie for starred repo updates.
- **GenAI Key**: Access an LLM model by following [these steps](https://ai.google.dev/gemini-api/docs/api-key) (currently free).

### Set up environment variables:

```env
GH_TOKEN=
GH_USER_ID=
GH_COOKIE=
GENAI_KEY=
```

---

### Running StarListify

Follow these four main steps:

1. **Fetch**:
   ```bash
   starlistify fetch 
   ```
   - Fetches starred repositories for the specified GitHub account and saves them to a file named `<username>_starred_repos-<current-date>.csv` for use in subsequent steps.

2. **Generate**:
   ```bash
   starlistify generate --preferences "Your preferences here" --use-reference
   ```
   - Generates a categorized list based on user-defined preferences, saved as `topics_<username>.csv`. You can refine this list manually to ensure it aligns with your needs. The `--use-reference` flag uses your created list as a reference for generate new lists.

3. **Categorize**:
   ```bash
   starlistify categorize --model "Embeddings-based model"
   ```
   - Uses an embeddings-based model to assign relevant topics from each repository's README, saving results as `star_listified_<username>.csv`. The model can be local or pre-trained. Refer to the [mteb leaderboard](https://huggingface.co/spaces/mteb/leaderboard) for model options.

4. **Update**:
   ```bash
   starlistify update --reset
   ```
   - Updates your GitHub account with the categorized lists. Since GitHub allows only 32 lists, use the `--reset` flag to clear existing lists as needed.

---

## Contributing

Contributions are encouraged! If you have suggestions or improvements, please fork the repository, adhere to coding conventions, and submit a pull request. Including tests for new features is appreciated.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
