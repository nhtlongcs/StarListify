from .fetch_gh_stars import main as fetch_main
from .cluster_gh_stars import main as cluster_main
from .categorize_gh_stars import main as categorize_main
from .update_gh_lists import main as update_main
import argparse

def main():
    parser = argparse.ArgumentParser(description="GitHub Starred List CLI")
    parser.add_argument("action", choices=["fetch", "generate", "categorize", "update"], help="Action to perform")
    parser.add_argument("--preferences", help="Preferences for generating list")
    parser.add_argument("--use-reference", action="store_true", help="Use reference list for generating list")
    parser.add_argument("--model", type=str, default='dunzhang/stella_en_400M_v5', help="Embedding model to use for categorization")
    parser.add_argument("--reset", action="store_true", help="Reset github list (for update new starred lists)")

    args = parser.parse_args()

    if args.action == "fetch":
        fetch_main()
    elif args.action == "generate":
        cluster_main(preferences=args.preferences, use_reference=args.use_reference)
    elif args.action == "categorize":
        categorize_main(args.model)
    elif args.action == "update":
        update_main(reset_lists=args.reset)

if __name__ == "__main__":
    main()