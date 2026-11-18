# research-agent

A small tool-using agent that runs locally with Ollama (llama3.2:3b). It decides on its own whether to answer directly, search the web, or use a calculator.

## How it works

- `web_tool.py`: web search with DuckDuckGo (ddgs)
- `calc_tool.py`: safe calculator (only + - * /, no eval)
- `agent.py`: the model picks a tool, the tool runs, and the result goes back to the model. This repeats up to 4 steps.
- `eval.py`: checks which tool the model picks on 9 questions

## Run

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
python agent.py
```

## Tests

```
python -m pytest
ruff check .
```

CI runs both on every push (GitHub Actions).

## Evaluation

`python eval.py` scores 8 / 9 on tool choice.

## Decisions

- Calculator uses `ast`, not `eval`, so it cannot run unsafe code.
- A system prompt fixed two problems: using a tool for a greeting, and writing percentages wrong (15 instead of 0.15). Greeting question went from wrong to correct (7/9 to 8/9).
- temperature 0 for more stable behavior.
- The calculator error message tells the model what to do next.

## Known limitations

- "What is 20% of the population of Iran?" still fails. The model calls the calculator with text instead of searching first, then answers from its own memory. A 3B model is weak at chaining two tools.
- Eval checks only the first tool choice, not the correctness of the final answer.

## Next

- Try a bigger model for multi-step tool use
- Eval the final answers, not only tool choice
- Docker