import requests
import os


def fetch_readme():
    url = "https://raw.githubusercontent.com/i-pj/SnakeGame/main/README.md"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch README.md: " + str(response.status_code))


content = fetch_readme()

directory = "data"
filename = "README.md"

filepath = os.path.join(directory, filename)
with open(filepath, "w") as file:
    file.write(content)
