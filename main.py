#! /usr/bin/env python
import json

from display import render_dot
from graphs import compose_graph_content
from notion_api import fetch_tasks

DEPENDENCY_FOR_KEY = 'Dependency for'
DEPENDS_ON_KEY = 'Depends on'


def read_config() -> dict:
    # keys: notion_token, database_id
    with open("config.json") as f:
        return json.load(f)


def task_name(task_id, id_to_task):
    return id_to_task[task_id]['properties']['Projects']['title'][0]['plain_text']


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
    output_picture_name = "steps.png"

    dot_content = "\n".join(compose_graph_content(next_steps, task_name=lambda x: task_name(x, id_to_task=id_to_task)))
    render_dot(content=dot_content, output_picture_name=output_picture_name)
