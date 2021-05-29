#! /usr/bin/env python
import json
import subprocess
from typing import List, Callable, Generator

import requests

DEPENDENCY_FOR_KEY = 'Dependency for'
DEPENDS_ON_KEY = 'Depends on'


def read_config() -> dict:
    # keys: notion_token, database_id
    with open("config.json") as f:
        return json.load(f)


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


def task_name(task_id, id_to_task):
    return id_to_task[task_id]['properties']['Projects']['title'][0]['plain_text']


def split_long_sentences(sentence, chars_per_line=15):
    sentence = sentence.strip()
    if len(sentence) <= chars_per_line:
        return sentence

    words = sentence.split(' ')
    line, length = [], 0
    for word in words:
        if length > chars_per_line:
            result = f'{" ".join(line)}\\n{split_long_sentences(sentence[length:])}'
            return result

        line.append(word)
        length += len(word) + 1  # spaces

    return " ".join(line)


def compose_graph_content(dependencies, task_name: Callable[[str], str]) -> Generator[str, None, None]:
    yield 'digraph {'
    for task_id in dependencies:
        if not dependencies[task_id]:
            node = split_long_sentences(task_name(task_id))
            yield f'"{node}";'

        for dep_id in dependencies[task_id]:
            node_from = split_long_sentences(task_name(task_id))
            node_to = split_long_sentences(task_name(dep_id))

            yield f'"{node_from}" -> "{node_to}";'

    yield '}'


if __name__ == '__main__':
    config = read_config()
    tasks = fetch_tasks(token=config['notion_token'], database_id=config["database_id"])

    id_to_task = {task['id']: task for task in tasks}

    dependencies = {
        task['id']: [d['id'] for d in task['properties'][DEPENDS_ON_KEY].get('relation', [])] for task in tasks
    }
    next_steps = {
        task['id']: [d['id'] for d in task['properties'][DEPENDENCY_FOR_KEY].get('relation', [])] for task in tasks
    }
    output_dot_filename = "steps.dot"
    output_picture_name = "steps.png"

    with open(output_dot_filename, "w") as f:
        lines = compose_graph_content(next_steps, task_name=lambda x: task_name(x, id_to_task=id_to_task))
        f.write("\n".join(lines))

    subprocess.run(["dot", "-Tpng", output_dot_filename, "-o", output_picture_name], check=True)
