# Resellpur - AI Agents (Price Suggestor + Chat Moderation)

This is a complete, ready-to-run Flask project implementing two agents for a second-hand marketplace:

- **Price Suggestor Agent** (`/negotiate`): returns a suggested min/max price and reasoning.
- **Chat Moderation Agent** (`/moderate`): classifies messages as Safe / Abusive / Spam and detects phone numbers.

Features included:
- Flask frontend (responsive) with simple animations (CSS + JS).
- REST API endpoints: `POST /negotiate` and `POST /moderate`.
- Heuristic price algorithm (category baseline + age depreciation + condition factor).
- Moderation rules: phone regex, keyword checks, simple spam heuristics.
- Sample dataset: `data/marketplace.csv` with example rows.
- Tests using pytest.
- Clear project structure and run instructions.

## Run locally (Linux / macOS / WSL / Windows with Python 3.10+)

1. Create virtual env and install requirements:
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run the app (development):
```bash
export FLASK_APP=app.app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

Or use gunicorn for production-like run:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.app:app
```

3. Open http://localhost:5000 in your browser (desktop or mobile).

## API examples (JSON)

### /negotiate
Request:
```json
POST /negotiate
{
  "title": "iPhone 11, 64GB",
  "category": "mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": 24,
  "asking_price": 20000,
  "location": "New Delhi"
}
```
Response:
```json
{
  "suggested_min": 18000,
  "suggested_max": 22000,
  "currency": "INR",
  "method": "baseline_from_dataset + age_depr + condition_factor",
  "reasoning": "computed from dataset baseline and adjustments"
}
```

### /moderate
Request:
```json
POST /moderate
{"message": "Call me at +91 9876543210. Selling quickly!"}
```
Response:
```json
{
  "status": "Unsafe",
  "contains_mobile": true,
  "flags": ["contains_mobile"]
}
```

## Project structure
```
resellpur_project/
  app.py (Flask app)
  agents/
    price_agent.py
    moderation_agent.py
  templates/
    index.html
  static/
    css/style.css
    js/app.js
  data/marketplace.csv
  tests/
    test_agents.py
  README.md
  requirements.txt
```

If you want, I can now:
- Walk through specific files and explain the logic.
- Extend the UI with extra pages or add authentication.
- Connect to a real LLM provider (OpenAI / Hugging Face) if you provide API keys.
