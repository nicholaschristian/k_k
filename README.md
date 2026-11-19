# Key & Kin

Marketing site and inquiry inbox for Key & Kin, a mobile specialty coffee cart.

- Public site: one page (how booking works, drinks, packages, events, about, FAQ, inquiry form)
- `/admin`: single owner login to read inquiries and mark them new / contacted / booked / declined

Stack follows the other Shao Box apps: Flask app factory, PyMongo, Flask-WTF, Flask-Login, gunicorn + `mongo:7` in Docker.

## Editing content

All copy, drinks, packages, prices, FAQ and contact details live in `app/content.py`.
Lines marked `PLACEHOLDER` (prices, phone, email, Instagram, service area, roaster) were invented and must be confirmed before launch.
Rebuild after editing: `docker compose up -d --build web`.

## Running

```bash
cp .env.example .env          # fill in SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD_HASH
docker compose run --rm web flask hash-password   # paste result into .env, escaping $ as $$
docker compose up -d --build
```

Served on host port **5045**. Health check: `GET /healthz`.

## Tests

Tests run against a real Mongo. The host's 27017 is another app's (with auth), so use a throwaway one:

```bash
docker run -d --rm --name kk-test-mongo -p 127.0.0.1:27099:27017 mongo:7
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
MONGO_URI=mongodb://localhost:27099/ .venv/bin/python -m pytest
docker stop kk-test-mongo
```

## Next steps

- Email notification to the owner on each new inquiry (SMTP or a transactional email service)
- Real photos of the cart and drinks once they exist
- Public hosting with TLS; then set `SESSION_COOKIE_SECURE=true` and `TRUST_PROXY_HEADERS=true`
