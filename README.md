# Fantasy Duck Sauce 🔮🦆🍅

Download data from AFL Fantasy Draft and processes it with DuckDB.

I want to see the highest performing free agents that are playing this week so I can recruit them.

There's no way to filter by playing status in the UI but we can pull all the data down and process it ourselves.

## Quick Start

```
marimo run app.py
```

## Getting Started

1. Install DuckDB.

    ```
    curl https://install.duckdb.org | sh
    ```
1. Install python dependencies.
    ```
    pip install -r requirements.txt
    ```
1. Login to your draft competition in Chrome.
1. Open Chrome Dev Tools.
1. Go to the Application Tab, Cookies and copy the X-SID value.
1. Run the app.
    ```
    marimo run app.py
    ```
1. Paste in the cookie and league id.
1. Create an .env file to persist your cookie and league id.
    ```
    COOKIE=f5d43a6ed4fa55180a5c7a18_1772282814
    LEAGUE=4465
    ```