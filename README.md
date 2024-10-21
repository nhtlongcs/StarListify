

# StarListify

**StarListify** is a Python package designed to help users classify their GitHub stars history into organized category lists. This tool fetches starred repositories, extracts valuable information including README content, and categorizes them based on user-defined criteria or hashtags derived from the README files.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## How does it work?
- Fetch starred repositories from a specified GitHub user account.
- Generate a list of categories based on the starred repositories and user-defined criteria.
- For each repository README, retrieve the most relevant topic using a embeddings-based model.

## Installation

To install `StarListify`, you can clone the repository and install the required dependencies:

```bash
git clone https://github.com/nhtlongcs/starListify.git
cd starListify
pip install -r requirements.txt
```

## Usage (wip)

```bash
python fetch-gh-stars.py <username>
python cluster-gh-stars.py <username>
python categorize-gh-stars.py <username>
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or would like to contribute to the project, please fork the repository and submit a pull request. Ensure to follow coding conventions and include tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize the sections, add more specific examples, or include additional information about your project as needed!