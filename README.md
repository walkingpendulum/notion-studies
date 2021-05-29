# notion-studies

This project is about me getting know [Notion](https://notion.so) HTTP API. The practical task is to visualize tasks dependencies graph withing specific project. 

## Concept
1. Fetch all tasks (__pages__) within specific project (__database__) via [Notion HTTP API](https://developers.notion.com/docs/getting-started)
1. Build dependency graph (I expect tasks to have "Depends on"/"Dependency for" properties of "relation" type).
1. Generate [graph in dot format](https://www.graphviz.org/doc/info/lang.html).
1. Render dependency graph via [graphviz](https://www.graphviz.org/about/) tool

## Configuration
There should be `config.json` file (will be ignored by git) with following content:
```json
{
  "notion_token": "secret_ABCDXXXYYYZZZ",
  "database_id": "123abc456efg"
}
```

## How to use it
`./main.py && open steps.png`

## External requirements
- [dot executable](https://www.graphviz.org/download/#executable-packages) - part of graphviz package
