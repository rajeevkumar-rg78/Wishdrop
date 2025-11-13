import streamlit as st
import pandas as pd
from utils.storage import save_board, get_board
from utils.price import simulate_price_history, buy_or_wait_signal
from utils.storage import list_profiles

# --------------------------------------------
# GLOBAL SCROLL FIX (selectbox & multiselect)
# --------------------------------------------
st.markdown("""
<style>
div[data-baseweb="select"] > div {
    max-height: 250px !important;
    overflow-y: auto !important;
}
div[role="listbox"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}
div[data-baseweb="popover"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# HEADER
# --------------------------------------------
st.header("❤️ Boards & Alerts")

products = pd.read_csv("data/sample_products.csv")

# --------------------------------------------
# STORE ICONS
# --------------------------------------------
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
    "Sephora": "💄",
    "Ulta Beauty": "🪞",
    "Macy's": "⭐",
    "Amazon": "🟧",
    "Target": "🎯",
    "Best Buy": "🔵",
    "Apple Store": "",
    "Costco": "🅲",
    "Home Depot": "🛠️"
}

# --------------------------------------------
# USER PROFILE SELECTOR (DROPDOWN instead of typing)
# --------------------------------------------
profiles = list_profiles()
user = st.sidebar.selectbox("Active Profile", ["Select"] + profiles)

if user == "Select":
    st.info("Select your profile in the left sidebar.")
    st.stop()

# --------------------------------------------
# LOAD BOARD DATA
# --------------------------------------------
board_data = get_board(user)

if "saved" not in st.session_state:
    st.session_state["saved"] = list(board_data.get("saved", []))

if "tracked" not in st.session_state:
    st.session_state["tracked"] = dict(board_data.get("tracked", {}))

saved_ids = st.session_state["saved"]
tracked_items = st.session_state["tracked"]

# =====================================================
# ⭐ SAVED ITEMS SECTION
# =====================================================
st.subheader("⭐ Saved Items")

if not saved_ids:
    st.info("No saved items yet. Click ❤️ in Discover to save products.")
else:
    cols = st.columns(2, gap="large")

    for i, pid in enumerate(saved_ids):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            img = item["image_url"].replace("800x1000", "400x500")
            st.image(img, use_container_width=True)

            store_icon = STORE_ICONS.get(item["store"], "🛒")

            st.markdown(f"### {item['name']}")
            st.caption(f"{store_icon} {item['store']} • {item['brand']} • {item['category']}")

            # PREMIUM PRICE FORMAT
            st.markdown(
                f"""
                <div style="font-size:18px; font-weight:600; margin-top:6px;">
                    <span style="color:#d00000;">${item['price']:.2f}</span>
                    &nbsp;&nbsp;
                    <span style="color:gray; text-decoration: line-through;">
                        ${item['msrp']:.2f}
                    </span>
                    &nbsp;&nbsp;
                    <span style="color:green;">-{int(item['discount_pct'])}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("❌ Remove", key=f"remove_{pid}"):
                st.session_state["saved"].remove(pid)
                st.experimental_rerun()

# =====================================================
# 🔔 PRICE ALERTS
# =====================================================

st.subheader("🔔 Price Alerts")

if not tracked_items:
    st.info("No alerts set. Use 🔔 Track in Discover.")
else:
    cols = st.columns(2, gap="large")

    for i, (pid, threshold) in enumerate(tracked_items.items()):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            img = item["image_url"].replace("800x1000", "400x500")
            st.image(img, use_container_width=True)

            store_icon = STORE_ICONS.get(item["store"], "🛒")

            st.markdown(f"### {item['name']}")
            st.caption(f"{store_icon} {item['store']} • {item['brand']} • {item['category']}")

            st.markdown(
                f"**Current Price:** ${item['price']:.2f}  \n"
                f"Alert triggers if price drops **{threshold}%** below today.",
                unsafe_allow_html=True
            )

            with st.expander("📉 Price Trend & AI Advice"):
                series = simulate_price_history(item["price"], days=60)
                st.line_chart(series, use_container_width=True)

                rec, note = buy_or_wait_signal(series, item["price"])
                st.markdown(f"**AI Suggestion: {rec}**")
                st.caption(note)

            if st.button("❌ Stop Tracking", key=f"stop_{pid}"):
                del st.session_state["tracked"][pid]
                st.experimental_rerun()

# =====================================================
# 💾 SAVE BOARD BUTTON
# =====================================================
st.sidebar.markdown("---")

if st.sidebar.button("💾 Save Board"):
    save_board(
        user,
        {
            "saved": st.session_state["saved"],
            "tracked": st.session_state["tracked"]
        }
    )
    st.sidebar.success("Board saved successfully!")
