replay_tool/
├── core/                          # Core business logic
│   ├── gann.py
│   ├── replay_engine.py
│   ├── session_picker.py
│   ├── __init__.py
│   └── __pycache__/
│
├── data/                          # Data access & repositories
│   ├── candle_repository.py
│   ├── data_loader.py
│   ├── session_repository.py
│   ├── trade_repository.py
│   ├── __init__.py
│   └── __pycache__/
│
├── ui/                            # Streamlit UI
│   ├── app.py                     # Main entrypoint
│   ├── chart.py                   # Chart utilities
│   ├── controls.py                # UI controls (buttons, selectors)
│   ├── __init__.py
│   ├── __pycache__/
│   └── pages/
│       └── chart.py               # Full-screen chart page
│
├── utils/                         # Shared helpers
│   ├── exchange_utils.py
│   ├── utils_db.py
│   ├── __init__.py
│   └── __pycache__/
│
├── .gitignore
├── README.md
└── vs.bat                         # Batch file to start environment
