import json
import os
from pathlib import Path
from urllib.parse import parse_qs


BASE_DIR = Path(__file__).resolve().parent
ANSWERS_DIR = BASE_DIR / "answers"


def read_answer(category: str, topic: str) -> str | None:
    answer_file = ANSWERS_DIR / category / f"{topic}.txt"
    if not answer_file.exists():
        return None
    return answer_file.read_text(encoding="utf-8")


def list_answers() -> dict[str, list[str]]:
    data: dict[str, list[str]] = {}
    if not ANSWERS_DIR.exists():
        return data

    for category_dir in sorted(path for path in ANSWERS_DIR.iterdir() if path.is_dir()):
        data[category_dir.name] = sorted(file.stem for file in category_dir.glob("*.txt"))
    return data


def json_response(start_response, status_code: int, payload: dict) -> list[bytes]:
    body = json.dumps(payload, indent=2).encode("utf-8")
    status_text = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }[status_code]
    start_response(status_text, [("Content-Type", "application/json; charset=utf-8")])
    return [body]


def text_response(start_response, status_code: int, body: str) -> list[bytes]:
    status_text = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }[status_code]
    start_response(status_text, [("Content-Type", "text/plain; charset=utf-8")])
    return [body.encode("utf-8")]


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query = parse_qs(environ.get("QUERY_STRING", ""))
    as_json = query.get("format", ["text"])[0].lower() == "json"

    if method != "GET":
        return json_response(start_response, 405, {"error": "Only GET is supported"})

    if path in {"/", ""}:
        payload = {
            "message": "DE internal answer service",
            "endpoints": {
                "health": "/health",
                "list": "/answers",
                "answer": "/answers/<category>/<topic>",
            },
            "examples": [
                "/answers/backend/wk1",
                "/answers/backend/wk4",
                "/answers/backend/deploy",
                "/answers/backend/wk1?format=json",
            ],
        }
        return json_response(start_response, 200, payload)

    if path == "/health":
        return json_response(start_response, 200, {"status": "ok"})

    if path == "/answers":
        return json_response(start_response, 200, {"answers": list_answers()})

    parts = [part for part in path.strip("/").split("/") if part]
    if len(parts) == 3 and parts[0] == "answers":
        _, category, topic = parts
        answer = read_answer(category, topic)
        if answer is None:
            return json_response(
                start_response,
                404,
                {"error": f"No answer found for {category}/{topic}"},
            )

        if as_json:
            return json_response(
                start_response,
                200,
                {"category": category, "topic": topic, "answer": answer},
            )
        return text_response(start_response, 200, answer)

    return json_response(start_response, 404, {"error": "Route not found"})


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving DE internal answers on http://127.0.0.1:{port}")
    with make_server("0.0.0.0", port, app) as server:
        server.serve_forever()
