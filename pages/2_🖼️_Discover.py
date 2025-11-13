import streamlit as st
import pandas as pd
from utils.storage import list_profiles, get_profile
from utils.price import simulate_price_history, buy_or_wait_signal

# --------------------------------------
# Page Setup
# --------------------------------------
st.set_page_config(page_title="Discover – WishDrop", page_icon="🛍️", layout="centered")
st.header("🛍️ Discover — Personalized Luxury Sales")

# Fix long dropdowns
st.markdown("""
<style>
div[data-baseweb="select"] > div {
    max-height: 250px !important;
    overflow-y: auto !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------
# Load Products
# --------------------------------------
@st.cache_data
def load_products():
    return pd.read_csv("data/sample_products.csv")

products = load_products()

# --------------------------------------
# Profile Selection
# --------------------------------------
profiles = ["Select"] + list_profiles()
chosen = st.sidebar.selectbox("Active Profile", profiles)

if chosen == "Select":
    st.info("Select or create a profile in the **Profile** tab to personalize your sales feed.")
    st.stop()

prof = get_profile(chosen)

# --------------------------------------
# Sidebar Filters
# --------------------------------------
st.sidebar.subheader("Filters")
min_disc = st.sidebar.slider("Minimum Discount %", 0, 80, 10)
query = st.sidebar.text_input("Search (brand/store/category/name)")

# --------------------------------------
# Apply Profile Filters
# --------------------------------------
df = products.copy()

# Brand filter
if prof.get("brands"):
    df = df[df["brand"].isin(prof["brands"])]

# Store filter
if prof.get("stores"):
    df = df[df["store"].isin(prof["stores"])]

# Category filter
if prof.get("categories"):
    df = df[df["category"].isin(prof["categories"])]

# Price preference
price_pref = prof.get("price_pref", "Mid-range")
if price_pref == "Luxury Only":
    df = df[df["msrp"] >= 250]
elif price_pref == "Budget":
    df = df[df["price"] <= 80]

# Minimum discount
df = df[df["discount_pct"] >= min_disc]

# Search filter
if query:
    q = query.lower()
    df = df[
        df.apply(
            lambda r:
                q in r["name"].lower()
                or q in r["brand"].lower()
                or q in r["category"].lower()
                or q in r["store"].lower(),
            axis=1
        )
    ]

if df.empty:
    st.warning("No matching items. Adjust filters or update your profile preferences.")
    st.stop()

# Clean caption
st.caption(f"Showing **{len(df)}** items for **{chosen}**")

# --------------------------------------
# Display Grid
# --------------------------------------
cols = st.columns(2, gap="large")

if "saved" not in st.session_state:
    st.session_state["saved"] = set()

if "tracked" not in st.session_state:
    st.session_state["tracked"] = {}

if "price_cache" not in st.session_state:
    st.session_state.price_cache = {}

# Store Icons
STORE_ICONS = {
    "Nordstrom": "🖤", "Bloomingdale's": "🛍️", "Saks Fifth Avenue": "🤍",
    "Neiman Marcus": "💎", "Bergdorf Goodman": "👑",
    "Chanel": "⚫", "Prada": "🪩", "Gucci": "🟩",
    "Louis Vuitton": "🧡", "Burberry": "🤎",
    "Sephora": "💄", "Ulta Beauty": "🪞",
    "Macy's": "⭐", "Amazon": "🟧", "Target": "🎯",
    "Best Buy": "🔵", "Apple Store": "",
    "Costco": "🅲", "Home Depot": "🛠️"
}

# --------------------------------------
# Product Loop
# --------------------------------------
for i, row in df.reset_index(drop=True).iterrows():
    with cols[i % 2]:

        # Image
        img = row["image_url"].replace("800x1000", "500x650")
        st.image(img, use_container_width=True)

        # Info
        icon = STORE_ICONS.get(row["store"], "🛒")
        st.markdown(f"### {row['name']}")
        st.caption(f"{icon} {row['store']} • {row['brand']} • {row['category']}")

        # Price Formatting
        st.markdown(
            f"""
            <div style="font-size:18px; font-weight:600; margin-top:3px;">
                <span style="color:#d00000;">${row['price']:.2f}</span>
                &nbsp;&nbsp;
                <span style="color:gray; text-decoration: line-through;">
                    ${row['msrp']:.2f}
                </span>
                &nbsp;&nbsp;
                <span style="color:green;">-{int(row['discount_pct'])}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Buttons
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("❤️ Save", key=f"save_{row['id']}"):
                st.session_state["saved"].add(row["id"])

        with c2:
            if st.button("🔔 Track", key=f"track_{row['id']}"):
                st.session_state["tracked"][row["id"]] = 10

        with c3:
            st.link_button("🛒 Buy", row["product_url"])

        # Price Trend
        with st.expander("📉 Best Price Trend & Recommendation"):
            if row["id"] not in st.session_state.price_cache:
                st.session_state.price_cache[row["id"]] = simulate_price_history(row["price"], days=60)

            series = st.session_state.price_cache[row["id"]]
            st.line_chart(series)

            rec, note = buy_or_wait_signal(series, row["price"])
            st.markdown(f"**Recommendation: {rec}**")
            st.caption(note)
