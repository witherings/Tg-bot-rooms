# Team Code Lab

An open-access website that generates 10 sequential Brawl Stars team codes and invite links from a team code or invitation URL.

## Run locally

```sh
python main.py
```

Open `http://localhost:5000`. The site needs no Telegram token, database, sign-in, or subscription check.

## Use

1. Paste a team code or an invite URL containing `tag=...`.
2. Choose an offset (default: 50) or enter a custom value from 0 to 10,000.
3. Generate 10 results, then copy a code or link, copy all links, or open an invite link.

The site reuses the conversion algorithm from the imported project. It calculates codes and invite-shaped links; it does not check whether rooms are active or joinable.

## Railway

Deploy the repository from GitHub. Railway reads `requirements.txt` and the `Procfile`/`railway.json`; it supplies the `PORT` variable. No secrets or database are required.
