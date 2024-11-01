import os
def find_latest_file(user_id):
    """
    Find the latest CSV file for the user based on naming convention.
    """
    files = [f for f in os.listdir() if f.startswith(f"{user_id}_starred_repos-") and f.endswith(".csv")]
    if not files:
        return None
    return max(files, key=os.path.getctime)