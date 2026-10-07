# Team Code Lab

## Local run

- Start the Replit `Website` workflow, or run `python main.py`.
- The web app listens on `PORT` when set, otherwise port `5000`.
- `GET /` serves the website; `POST /api/generate` generates 10 results; `GET /health` is the health check.

## Behavior

- Public access: no Telegram, accounts, channel checks, or database.
- Supports a team code or invite URL, predefined offsets, and custom offsets from 0 to 10,000.
- The website reuses the imported code conversion algorithm.
- Generated codes and links are not verified against live Brawl Stars rooms.

## Railway

The repository is configured to run `gunicorn --bind 0.0.0.0:$PORT main:app`. No environment secrets or database are required.
