replay_tool/
│
├── ui/                         # 🎨 User interface (Streamlit)
│   ├── __init__.py
│   ├── app.py                  # Main entry (Streamlit app)
│   ├── chart.py                # Plotly candlestick chart + overlays
│   └── controls.py             # UI controls (instrument/session picker, playback speed, manual trade buttons)
│
├── core/                       # 🧠 Core replay + session logic
│   ├── __init__.py
│   ├── replay_engine.py        # Candle-by-candle replay engine
│   ├── session_picker.py       # Select sessions (NY, London, random date picker)
│   └── strategy_runner.py      # (Optional placeholder — skip automation if manual only)
│
├── data/                       # 📊 Data handling (DB + ETL)
│   ├── __init__.py
│   ├── data_loader.py          # Import candles (CSV/API → DB)
│   ├── candle_repository.py    # Store/fetch OHLCV candles from DB
│   ├── session_repository.py   # Store/fetch extracted sessions
│   └── trade_repository.py     # Store/fetch manual trades
│
├── utils/                      # 🔧 Helpers + integrations
│   ├── __init__.py
│   ├── exchange_utils.py       # MetaTrader/Binance/Bybit/Kraken connectors
│   └── utils_db.py             # Postgres engine + helpers (create tables, save/load)
│   
│
├── tests/                      # 🧪 Unit tests
│   ├── __init__.py
│   ├── test_sessions.py        # Test session extraction + picker
│   ├── test_replay.py          # Test replay engine step-by-step
│   └── test_db.py              # Test DB save/load
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── __init__.py                 # (Optional, makes project pip-installable)
