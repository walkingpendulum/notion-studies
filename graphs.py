from typing import Callable, Generator

from display import split_long_sentences


def compose_graph_content(dependencies: dict, task_name: Callable[[str], str]) -> Generator[str, None, None]:
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
