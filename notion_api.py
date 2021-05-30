from typing import List

import requests


def fetch_tasks(token: str, database_id: str) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-05-13",
    }
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=headers,
        json={"filter": {"or": [{"property": "Type", "select": {"equals": "Task 🔨"}}]}},
    )
    resp.raise_for_status()

    payload = resp.json()
    return payload["results"]