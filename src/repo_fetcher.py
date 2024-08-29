import os
import subprocess


def clone_repository(repo_url, repo_path):
    if os.path.exists(repo_path):
        print("Repository already exists, skipping clone")
    else:
        subprocess.run(["git", "clone", repo_url, repo_path])


def extract_repository(repo_path):
    documents = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    metadata = {"file_name": file_path}
                    documents.append({"content": content, "metadata": metadata})
                    print(f"Successfully extracted: {file_path}")
            except UnicodeDecodeError:
                print(f"Skipping file {file_path} due to encoding error")
    print(f"Total documents extracted: {len(documents)}")
    return documents


def main(repo_url=None):
    if repo_url is None:
        repo_url = input("Enter the GitHub repository URL: ")
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("data", repo_name)
    clone_repository(repo_url, repo_path)
    documents = extract_repository(repo_path)
    return documents


if __name__ == "__main__":
    main()
