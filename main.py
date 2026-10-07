import os

from flask import Flask, jsonify, render_template, request

from code_generator import (
    generate_sequential_codes,
    is_valid_team_code,
    parse_team_code,
)

app = Flask(
    __name__,
    template_folder="site/templates",
    static_folder="site/static",
)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024

PREDEFINED_OFFSETS = {5, 10, 20, 50, 100}
MAX_CUSTOM_OFFSET = 10_000
RESULT_COUNT = 10
ERROR_MESSAGES = {
    "ru": {
        "json": "Нужен JSON-запрос.",
        "input": "Введи код команды или ссылку-приглашение.",
        "length": "Ссылка или код слишком длинные.",
        "invalid_code": "Не удалось распознать код команды.",
        "invalid_offset": "Смещение должно быть целым числом.",
        "offset_range": "Выбери смещение от 0 до 10000.",
        "generation": "Не удалось обработать этот код команды.",
        "range_edge": (
            "Этот код находится у границы диапазона; "
            "для него нельзя создать 10 результатов."
        ),
    },
    "en": {
        "json": "A JSON request is required.",
        "input": "Enter a team code or an invite link.",
        "length": "The code or link is too long.",
        "invalid_code": "Could not recognize that team code.",
        "invalid_offset": "The offset must be a whole number.",
        "offset_range": "Choose an offset from 0 to 10000.",
        "generation": "Could not process that team code.",
        "range_edge": (
            "This code is at the edge of the range, so 10 results "
            "cannot be generated."
        ),
    },
}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/generate")
def generate():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": ERROR_MESSAGES["ru"]["json"]}), 400

    language = payload.get("language", "ru")
    if not isinstance(language, str) or language not in ERROR_MESSAGES:
        language = "ru"
    messages = ERROR_MESSAGES[language]

    raw_input = payload.get("teamCodeOrLink")
    if not isinstance(raw_input, str) or not raw_input.strip():
        return jsonify({"error": messages["input"]}), 400
    if len(raw_input) > 512:
        return jsonify({"error": messages["length"]}), 400

    team_code = parse_team_code(raw_input)
    if not is_valid_team_code(team_code):
        return jsonify({"error": messages["invalid_code"]}), 400

    offset = payload.get("offset", 50)
    if isinstance(offset, bool) or not isinstance(offset, int):
        return jsonify({"error": messages["invalid_offset"]}), 400
    if offset not in PREDEFINED_OFFSETS and not 0 <= offset <= MAX_CUSTOM_OFFSET:
        return jsonify({"error": messages["offset_range"]}), 400

    try:
        codes = generate_sequential_codes(team_code, offset, RESULT_COUNT)
    except ValueError:
        return jsonify({"error": messages["generation"]}), 400

    if len(codes) != RESULT_COUNT:
        return jsonify({"error": messages["range_edge"]}), 422

    language_code = "ru" if language == "ru" else "en"
    results = [
        {
            "index": index,
            "teamCode": item["team_code"],
            "hashCode": item["hash_code"],
            "inviteUrl": (
                "https://link.brawlstars.com/invite/gameroom/"
                f"{language_code}/?tag={item['team_code']}"
            ),
        }
        for index, item in enumerate(codes, 1)
    ]

    return jsonify(
        {
            "baseCode": team_code,
            "offset": offset,
            "results": results,
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=False,
        use_reloader=False,
    )
