from ddgs import DDGS


def web_search(query):
    results = DDGS().text(query, max_results=3)
    lines = []
    for r in results:
        lines.append(r["title"] + ": " + r["body"])
    return "\n".join(lines)


if __name__ == "__main__":
    print(web_search("Tehran population"))