# 🏋️ GYM Management System (Streamlit)

A simple gym membership manager with a Streamlit UI: create an account, log
in, track daily steps/calories/exercise, update your profile, and view
progress charts.

## Features

- Create Account — generates a unique Roll No + GYM ID
- Login — authenticate with Roll No + password
- Daily Update — log steps, calories, or exercises (auto-estimates calories
  from steps/exercise duration)
- Update Profile — edit personal details (Roll No, GYM ID, Gender are fixed)
- Progress Charts — steps line chart, calories bar chart, exercise log table
- Data persisted locally in `database.json` (same format as the original
  CLI version, so an existing database keeps working)

## Setup

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Project structure

```
.
├── app.py             # Streamlit app
├── requirements.txt   # dependencies
├── database.json      # created automatically on first account (gitignored)
└── README.md
```

## Notes

- `database.json` is gitignored so member data isn't pushed to GitHub.
- No passwords are hashed in this demo — don't use real passwords / deploy
  publicly as-is if that matters for your use case.
