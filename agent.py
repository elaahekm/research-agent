import ollama

from calc_tool import calculate
from web_tool import web_search

MODEL = "llama3.2:3b"

SYSTEM = (
    "For greetings and chit-chat, answer directly without any tool. "
    "Search for exactly the place or thing named in the question. "
    "After you find a number, use the calculator to finish the math."
)

MAX_STEPS = 4


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
    except (ValueError, SyntaxError, ZeroDivisionError):
        return "error: use only numbers. Call search_web first to get the number you need."


TOOLS = {"search_web": search_web, "calculator": calculator}


def ask(question):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for _ in range(MAX_STEPS):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=[search_web, calculator],
            options={"temperature": 0},
        )
        messages.append(response.message)
        if not response.message.tool_calls:
            return response.message.content
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
    return "error: too many steps"


if __name__ == "__main__":
    print(ask("What is 20% of the population of Iran?"))