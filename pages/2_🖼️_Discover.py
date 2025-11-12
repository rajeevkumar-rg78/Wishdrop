
import streamlit as st
import pandas as pd
from utils.storage import list_profiles, get_profile
from utils.price import simulate_price_history, buy_or_wait_signal

st.header("🖼️ Discover — Personalized Sales")

products = pd.read_csv("data/sample_products.csv")
profiles = ["Select"] + list_profiles()
chosen = st.sidebar.selectbox("Active Profile", profiles, index=0)

if chosen == "Select" or not chosen:
    st.info("Select a profile (or create one in **👤 Profile**) to personalize results.")
    st.stop()

prof = get_profile(chosen)

st.sidebar.markdown("---")
st.sidebar.subheader("Extra Filters")
min_disc = st.sidebar.slider("Minimum Discount %", 0, 60, 10, step=5)
q = st.sidebar.text_input("Search (name/brand/category)")

df = products.copy()
if prof.get("brands"):
    df = df[df["brand"].isin(prof["brands"])]
if prof.get("stores"):
    df = df[df["store"].isin(prof["stores"])]
if prof.get("categories"):
    df = df[df["category"].isin(prof["categories"])]
pref = prof.get("price_pref","Mid-range")
if pref == "Luxury Only":
    df = df[df["msrp"] >= 200]
elif pref == "Budget":
    df = df[df["price"] <= 80]

df = df[df["discount_pct"] >= min_disc]
if q:
    ql = q.lower()
    df = df[df.apply(lambda r: ql in r["name"].lower() or ql in r["brand"].lower() or ql in r["category"].lower(), axis=1)]

if df.empty:
    st.warning("No matches. Relax filters or update brands/stores in your profile.")
    st.stop()

st.caption(f"Showing {len(df)} items for **{chosen}**.")

cols = st.columns(4, gap="large")
if "price_cache" not in st.session_state:
    st.session_state.price_cache = {}

for i, row in df.reset_index(drop=True).iterrows():
    with cols[i % 4]:
        st.image(row["image_url"], use_container_width=True)
        st.markdown(f"**{row['name']}**")
        st.caption(f"{row['brand']} • {row['category']} • {row['store']}")
        st.markdown(f"${row['price']:,.2f}  ~  ~~${row['msrp']:,.2f}~~  •  **-{int(row['discount_pct'])}%**")
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("❤️ Save", key=f"save_{row['id']}"):
                saved = st.session_state.get("saved", set())
                saved.add(row["id"])
                st.session_state["saved"] = saved
                st.toast("Saved to board")
        with c2:
            if st.button("🔔 Track", key=f"track_{row['id']}"):
                tracked = st.session_state.get("tracked", {})
                tracked[row["id"]] = tracked.get(row["id"], 10)
                st.session_state["tracked"] = tracked
                st.toast("Tracking with 10% threshold")
        with c3:
            st.link_button("🛒 Buy", row["product_url"])

        with st.expander("Price Trend & Advice"):
            if row["id"] not in st.session_state.price_cache:
                st.session_state.price_cache[row["id"]] = simulate_price_history(row["price"], days=60)
            series = st.session_state.price_cache[row["id"]]
            st.line_chart(series)
            rec, note = buy_or_wait_signal(series, row["price"])
            st.markdown(f"**Recommendation: {rec}**")
            st.caption(note)
