# Deploy Team Code Lab to Railway

1. Create a Railway service from this GitHub repository.
2. Keep the service's source/root directory at the repository root.
3. Railway installs the Python dependencies from `requirements.txt`.
4. The start command is configured in `railway.json` and `Procfile`: `gunicorn --bind 0.0.0.0:$PORT main:app`.
5. Deploy and open the generated public domain.

No Telegram bot token, PostgreSQL database, or other environment variable is needed. Railway provides the `PORT` value automatically.

## Important behavior

The site calculates sequential team codes and creates invite-shaped links using the imported conversion algorithm. It does not verify that a generated code points to an active or joinable game room.
