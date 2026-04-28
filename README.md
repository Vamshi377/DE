# DE Internal Answer API

This project is now a small Python API that you can deploy and call from another computer using `curl`.

## Local Run

```cmd
python app.py
```

The API starts on port `8000` by default.

## Example curl Commands

```cmd
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/answers
curl http://127.0.0.1:8000/answers/backend/wk1
curl "http://127.0.0.1:8000/answers/backend/wk4?format=json"
```

## Deploy

You can deploy this on any Python hosting platform that supports a start command.

- Install dependencies with `pip install -r requirements.txt`
- The production start command is `gunicorn app:app`
- `Procfile` is included for platforms that detect it automatically

After deployment, call your live URL like:

```cmd
curl https://your-app-url/answers/backend/wk1
curl https://your-app-url/answers/backend/wk6
curl https://your-app-url/answers/backend/deploy
```

## Routes

- `GET /health` - health check
- `GET /answers` - list all available answer keys
- `GET /answers/backend/wk1` - get answer as plain text
- `GET /answers/backend/wk1?format=json` - get answer as JSON

## Files

- `app.py` - Python API
- `requirements.txt` - deployment dependency list
- `Procfile` - production start command
- `answers\backend\wk1.txt` to `answers\backend\wk6.txt` - week-wise answers

## Add a New Answer

1. Create a new text file such as:

```txt
answers\backend\wk7.txt
```

2. Put your answer inside that file.
3. Access it with:

```cmd
curl https://your-app-url/answers/backend/wk7
```

## Notes

- The API reads directly from the `answers` folder.
- Plain text output is easiest for exams and quick terminal lookup.
- Existing `.cmd` files can stay, but the API is now the main way to use the project remotely.
