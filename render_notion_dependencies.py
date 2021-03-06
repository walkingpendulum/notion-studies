#! /usr/bin/env python
import argparse
import json
import os
import shlex
import subprocess
import tempfile
from collections import ChainMap
from typing import Optional, List

from graphs import compose_graph_content
from notion_api import fetch_tasks

DEPENDENCY_FOR_KEY = 'Dependency for'
DEPENDS_ON_KEY = 'Depends on'
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")


def read_config_from_disk() -> dict:
    # keys: notion_token, database_id
    try:
        with open("config.json") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"Config file not found, skip loading from disk")
        return {}


def read_config_from_env() -> dict:
    config = {}
    if NOTION_TOKEN:
        config.update({"notion_token": NOTION_TOKEN})

    if DATABASE_ID:
        config.update({"database_id": DATABASE_ID})

    return config


def task_name(task_id: str, id_to_task: dict) -> str:
    return id_to_task[task_id]['properties']['Projects']['title'][0]['plain_text']


def status_color(task_id: str, id_to_task: dict) -> Optional[str]:
    return id_to_task[task_id]['properties'].get("Status", {}).get("select", {}).get("color")


def task_url(task_id: str) -> str:
    return f"https://www.notion.so/{task_id.replace('-', '')}"


def run_cmd(command: List[str]):
    print(f"Execute: {' '.join(map(shlex.quote, command))}")
    subprocess.run(command, check=True)


def render_dot(content: str, output_picture_name: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".dot", prefix="graph_", mode="w", delete=False) as temp_obj:
        temp_obj.write(content)

    _, extension = os.path.splitext(output_picture_name)  # extension is like '.png'
    extension = extension[1:]
    print(f"Deduced extension is {extension}")

    try:
        run_cmd(["dot", f"-T{extension}", temp_obj.name, "-o", output_picture_name])
    finally:
        try:
            os.unlink(temp_obj.name)
        except Exception:
            pass


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Request all tasks from notion and render dependencies graph from them",
    )
    parser.add_argument("--output", help="Path where output picture will be stored", required=True)

    return parser


def main(argv=None):
    args = make_parser().parse_args(argv)

    output_picture_name = args.output

    config = ChainMap(read_config_from_env(), read_config_from_disk())

    tasks = fetch_tasks(token=config['notion_token'], database_id=config["database_id"])
    id_to_task = {task['id']: task for task in tasks}
    next_steps = {
        task['id']: [d['id'] for d in task['properties'][DEPENDENCY_FOR_KEY].get('relation', [])] for task in tasks
    }

    dot_content = "\n".join(compose_graph_content(
        next_steps,
        task_name=lambda x: task_name(x, id_to_task=id_to_task),
        color=lambda x: status_color(x, id_to_task=id_to_task),
        url=task_url,
    ))
    render_dot(content=dot_content, output_picture_name=output_picture_name)


if __name__ == '__main__':
    main()
