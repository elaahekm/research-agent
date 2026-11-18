import ollama

from agent import MODEL, SYSTEM, calculator, search_web

TESTS = [
    ("What is 15% of 2400?", "calculator"),
    ("Calculate 123 * 45", "calculator"),
    ("What is 1000 divided by 8?", "calculator"),
    ("What is the population of Tehran?", "search_web"),
    ("Who is the president of France?", "search_web"),
    ("What is the latest news about AI?", "search_web"),
    ("Hi, how are you?", "none"),
    ("What is 20% of the population of Iran?", "search_web"),
    ("Convert 5 kilometers to miles", "calculator"),
]


def first_tool(question):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        tools=[search_web, calculator],
    )
    calls = response.message.tool_calls
    if not calls:
        return "none"
    return calls[0].function.name


if __name__ == "__main__":
    score = 0
    for question, expected in TESTS:
        got = first_tool(question)
        ok = got == expected
        score += ok
        print("OK" if ok else "WRONG", question, "->", got)
    print("Score:", score, "/", len(TESTS))