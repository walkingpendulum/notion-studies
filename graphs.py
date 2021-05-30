from typing import Callable, Generator, Optional

from display import split_long_sentences


def compose_graph_content(
        dependencies: dict,
        task_name: Callable[[str], str],
        color: Callable[[str], Optional[str]],
) -> Generator[str, None, None]:
    yield 'digraph {'

    def repr_node(task_id: str) -> str:
        modifiers = {
            "color": f'{color(task_id)}' if color(task_id) else None,
            "style": "filled",
            "label": f'"{split_long_sentences(task_name(task_id))}"'
        }
        modifiers_ = ', '.join([f"{k}={v}" for k, v in modifiers.items() if v])
        return f'"{task_id}" [{modifiers_}]'

    all_nodes = sorted(set(dependencies) | set(dep_id for task_id in dependencies for dep_id in dependencies[task_id]))
    for node_id in all_nodes:
        yield f"{repr_node(node_id)};"

    for task_id in sorted(dependencies):
        for dep_id in sorted(dependencies[task_id]):
            yield f'"{task_id}" -> "{dep_id}";'

    yield '}'
