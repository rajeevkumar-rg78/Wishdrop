
# WishDrop v2 — Full App Platform

Pinterest-style discovery + Hopper-style price tracking — personalized by profile (height, weight, sizes, brands, stores, categories, price level).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Cloud)
- Repo main file: `app.py`
- Add `requirements.txt`
- Optional: switch to real retailer APIs later (Nordstrom, Sephora, Amazon, etc.)

## Data
- `data/sample_products.csv` mock items
- `data/profiles.json`, `data/boards.json` store local state (use DB in prod)
