import ollama

from calc_tool import calculate
from web_tool import web_search

MODEL = "llama3.2:3b"


def search_web(query: str) -> str:
    """Search the web for current information.

    Args:
        query: the search text
    """
    return web_search(query)


def calculator(expression: str) -> str:
    """Calculate a math expression like 12 * (3 + 4).

    Args:
        expression: the math expression
    """
    try:
        return str(calculate(expression))
    except Exception:
        return "error: bad expression"


TOOLS = {"search_web": search_web, "calculator": calculator}


def ask(question):
    messages = [
        {
            "role": "system",
            "content": "Use the calculator for any math. For percentages, "
            "use decimals: 15% of 2400 is 0.15 * 2400.",
        },
        {"role": "user", "content": question},
    ]
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=[search_web, calculator],
    )
    messages.append(response.message)
    if response.message.tool_calls:
        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print("Tool:", name, args)
            if name in TOOLS:
                result = TOOLS[name](**args)
            else:
                result = "error: unknown tool"
            messages.append(
                {"role": "tool", "tool_name": name, "content": result}
            )
        response = ollama.chat(model=MODEL, messages=messages)
    return response.message.content


if __name__ == "__main__":
        print(ask("What is the population of Tehran?"))
