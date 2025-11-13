import streamlit as st
import pandas as pd
from utils.storage import list_profiles, get_profile
from utils.price import simulate_price_history, buy_or_wait_signal

# ---------- Page Setup ----------
st.set_page_config(page_title="WishDrop – Discover", page_icon="🛍️", layout="centered")
st.header("🛍️ Discover — Personalized Luxury Sales")

# ---------- Data Load ----------
@st.cache_data
def load_products():
    return pd.read_csv("data/sample_products.csv")

products = load_products()
profiles = ["Select"] + list_profiles()
chosen = st.sidebar.selectbox("Active Profile", profiles, index=0)

if chosen == "Select" or not chosen:
    st.info("Select a profile (or create one in **👤 Profile**) to personalize results.")
    st.stop()

prof = get_profile(chosen)

# ---------- Sidebar Filters ----------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")
min_disc = st.sidebar.slider("Minimum Discount %", 0, 60, 10, step=5)
q = st.sidebar.text_input("Search (brand/store/category/name)")

# ---------- Apply Profile Filters ----------
df = products.copy()

# Filter by profile
if prof.get("brands"):
    df = df[df["brand"].isin(prof["brands"])]

if prof.get("stores"):
    df = df[df["store"].isin(prof["stores"])]

if prof.get("categories"):
    df = df[df["category"].isin(prof["categories"])]

# Filter budget preference
pref = prof.get("price_pref", "Mid-range")
if pref == "Luxury Only":
    df = df[df["msrp"] >= 200]
elif pref == "Budget":
    df = df[df["price"] <= 80]

# Additional filters
df = df[df["discount_pct"] >= min_disc]

if q:
    ql = q.lower()
    df = df[df.apply(
        lambda r: ql in r["name"].lower()
        or ql in r["brand"].lower()
        or ql in r["store"].lower()
        or ql in r["category"].lower(),
        axis=1,
    )]

if df.empty:
    st.warning("No matching luxury items found. Adjust filters or update profile settings.")
    st.stop()

st.caption(f"Showing **{len(df)} items** for **{chosen}**")

# ---------- Store Icons (for visual appeal) ----------
STORE_ICONS = {
    "Nordstrom": "🖤",
    "Bloomingdale's": "🛍️",
    "Saks Fifth Avenue": "🤍",
    "Neiman Marcus": "💎",
    "Bergdorf Goodman": "👑",
    "Chanel": "⚫",
    "Prada": "🪩",
    "Gucci": "🟩",
    "Louis Vuitton": "🧡",
    "Burberry": "🤎",
    "Sephora": "🪞",
    "Ulta Beauty": "💄",
    "Macy's": "⭐",
    "Amazon": "🟧",
    "Target": "🎯",
    "Best Buy": "🔵",
    "Costco": "🅲",
    "Home Depot": "🟧",
    "Nike": "👟",
    "Adidas": "⚪",
    "Apple Store": ""
}

# ---------- Grid (2 columns for mobile) ----------
cols = st.columns(2, gap="large")

# Cache price series so it doesn’t recalc every time
if "price_cache" not in st.session_state:
    st.session_state.price_cache = {}

# ---------- Display Products ----------
for i, row in df.reset_index(drop=True).iterrows():
    with cols[i % 2]:

        # 🖼️ Luxury image preview (smaller for mobile)
        img_url = row["image_url"].replace("800x1000", "500x650")
        st.image(img_url, use_container_width=True)

        # ⭐ Title
        st.markdown(f"### {row['name']}")

        # 🛍️ Store + Brand + Category
        store_icon = STORE_ICONS.get(row["store"], "🛒")
        st.markdown(f"**{store_icon} {row['store']}** • {row['brand']} • *{row['category']}*")

        # 💰 Price display
        st.markdown(
            f"### ${row['price']:,.2f}  &nbsp;&nbsp; "
            f"<span style='color:gray;'>~~${row['msrp']:,.2f}~~</span>  "
            f"<span style='color:green;'>**-{int(row['discount_pct'])}%**</span>",
            unsafe_allow_html=True
        )

        # Buttons: Save / Track / Buy
        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            if st.button("❤️ Save", key=f"save_{row['id']}"):
                saved = st.session_state.get("saved", set())
                saved.add(row["id"])
                st.session_state["saved"] = saved
                st.toast("Saved to board")

        with b2:
            if st.button("🔔 Track", key=f"track_{row['id']}"):
                tracked = st.session_state.get("tracked", {})
                tracked[row["id"]] = tracked.get(row["id"], 10)
                st.session_state["tracked"] = tracked
                st.toast("Tracking with 10% threshold")

        with b3:
            st.link_button("🛒 Buy", row["product_url"])

        # 📉 Price Trend & AI Recommendation
        with st.expander("📉 Best Price Trend & Recommendation"):
            if row["id"] not in st.session_state.price_cache:
                st.session_state.price_cache[row["id"]] = simulate_price_history(
                    row["price"], days=60
                )

            series = st.session_state.price_cache[row["id"]]

            st.line_chart(series, use_container_width=True)
            rec, note = buy_or_wait_signal(series, row["price"])

            st.markdown(f"### 💡 Recommendation: **{rec}**")
            st.caption(note)
