import streamlit as st
import pandas as pd
from utils.storage import save_board, get_board
from utils.price import simulate_price_history, buy_or_wait_signal

# -------------------------------------------
# PAGE HEADER
# -------------------------------------------
st.set_page_config(page_title="Boards & Alerts – WishDrop", page_icon="❤️", layout="centered")
st.header("❤️ Boards & Alerts")

products = pd.read_csv("data/sample_products.csv")

# -------------------------------------------
# STORE ICON MAP
# -------------------------------------------
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

# -------------------------------------------
# USER SELECTION (LEFT SIDEBAR)
# -------------------------------------------
user = st.sidebar.text_input("Profile name (same as Discover page)", placeholder="Enter saved profile name")

if not user:
    st.info("Enter your profile name to load your saved items.")
    st.stop()

board_data = get_board(user)

# Prepare session state cleanly
if "saved" not in st.session_state:
    st.session_state["saved"] = set(board_data.get("saved", []))

if "tracked" not in st.session_state:
    st.session_state["tracked"] = dict(board_data.get("tracked", {}))

saved_ids = list(st.session_state["saved"])
tracked_items = dict(st.session_state["tracked"])

# -------------------------------------------
# SAVED ITEMS SECTION
# -------------------------------------------
st.subheader("⭐ Saved Items")

if not saved_ids:
    st.info("No saved items yet.")
else:
    cols = st.columns(2, gap="large")

    for i, pid in enumerate(saved_ids):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            st.image(item["image_url"].replace("800x1000", "400x500"), use_container_width=True)

            icon = STORE_ICONS.get(item["store"], "🛒")
            st.markdown(f"### {item['name']}")
            st.caption(f"{icon} {item['store']} • {item['brand']} • {item['category']}")

            st.markdown(
                f"""
                <div style="font-size:18px; font-weight:600;">
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
                st.rerun()

# -------------------------------------------
# TRACKED ALERTS SECTION
# -------------------------------------------
st.subheader("🔔 Price Alerts")

if not tracked_items:
    st.info("No active price alerts.")
else:
    cols = st.columns(2, gap="large")

    for i, (pid, threshold) in enumerate(tracked_items.items()):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            st.image(item["image_url"].replace("800x1000", "400x500"), use_container_width=True)

            icon = STORE_ICONS.get(item["store"], "🛒")
            st.markdown(f"### {item['name']}")
            st.caption(f"{icon} {item['store']} • {item['brand']} • {item['category']}")

            st.markdown(
                f"**Current Price:** ${item['price']:.2f}  
                Alert triggers if price drops **{threshold}%**.",
                unsafe_allow_html=True
            )

            with st.expander("📉 Price Trend"):
                series = simulate_price_history(item["price"], days=60)
                st.line_chart(series)

                rec, note = buy_or_wait_signal(series, item["price"])
                st.markdown(f"**AI Recommendation: {rec}**")
                st.caption(note)

            if st.button("❌ Stop Tracking", key=f"stop_{pid}"):
                del st.session_state["tracked"][pid]
                st.rerun()

# -------------------------------------------
# SAVE BOARD BUTTON
# -------------------------------------------
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save Board"):
    save_board(
        user,
        {"saved": list(st.session_state["saved"]), "tracked": st.session_state["tracked"]}
    )
    st.sidebar.success("Board saved!")
