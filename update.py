import os
import requests

SOURCE_URL = (
    "https://www.googleapis.com/drive/v3/files/"
    "1T3TbRXbggKIzrvClvZhxxMgCVNberZpe"
    "?key=AIzaSyDkw4AHbGOawpa2v0x4kipmwAOjsCz2r5I&alt=media"
)

GIST_ID = os.environ["GIST_ID"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

GIST_FILENAME = "lunexis.txt"


def main():
    print("Downloading JSON...")

    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    servers = data.get("servers", [])

    links = []

    for server in servers:
        uri = server.get("uri")

        if uri:
            links.append(uri.strip())

    # Убираем дубликаты, сохраняя порядок
    links = list(dict.fromkeys(links))

    if not links:
        raise RuntimeError("No configs found")

    content = "\n".join(links) + "\n"

    print(f"Found {len(links)} configs")

    # Обновляем Gist
    url = f"https://api.github.com/gists/{GIST_ID}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload = {
        "files": {
            GIST_FILENAME: {
                "content": content
            }
        }
    }

    r = requests.patch(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    r.raise_for_status()

    print("Gist updated successfully")


if __name__ == "__main__":
    main()
