import streamlit as st
import pandas as pd
from utils.storage import save_board, get_board
from utils.price import simulate_price_history, buy_or_wait_signal

st.header("❤️ Boards & Alerts")

products = pd.read_csv("data/sample_products.csv")

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

# ---------------- Load board ----------------
user = st.sidebar.text_input("Profile name to load board", placeholder="e.g. raj")

if not user:
    st.info("Enter your profile name to load your saved board.")
    st.stop()

board = get_board(user)

if "saved" not in st.session_state:
    st.session_state["saved"] = set(board.get("saved", []))

if "tracked" not in st.session_state:
    st.session_state["tracked"] = dict(board.get("tracked", {}))

saved_ids = list(st.session_state["saved"])
tracked_items = dict(st.session_state["tracked"])

# ---------------- Saved Items ----------------
st.subheader("⭐ Saved Items")

if not saved_ids:
    st.info("No saved items yet. Use ❤️ Save in Discover.")
else:
    cols = st.columns(2)

    for i, pid in enumerate(saved_ids):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            img = item["image_url"].replace("800x1000", "500x650")
            st.image(img, use_container_width=True)

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

            if st.button(f"❌ Remove", key=f"rm_{pid}"):
                st.session_state["saved"].remove(pid)
                st.experimental_rerun()

# ---------------- Price Alerts ----------------
st.subheader("🔔 Price Alerts")

if not tracked_items:
    st.info("You are not tracking any items.")
else:
    cols = st.columns(2)

    for i, (pid, threshold) in enumerate(tracked_items.items()):
        item = products[products["id"] == pid].iloc[0]

        with cols[i % 2]:
            img = item["image_url"].replace("800x1000", "500x650")
            st.image(img, use_container_width=True)

            icon = STORE_ICONS.get(item["store"], "🛒")
            st.markdown(f"### {item['name']}")
            st.caption(f"{icon} {item['store']} • {item['brand']} • {item['category']}")

            st.write(f"Tracking item for **{threshold}% price drop**")

            with st.expander("📉 Price Trend"):
                series = simulate_price_history(item["price"], 60)
                st.line_chart(series)

                rec, note = buy_or_wait_signal(series, item["price"])
                st.markdown(f"**AI Recommendation: {rec}**")
                st.caption(note)

            if st.button(f"❌ Stop Tracking", key=f"stop_{pid}"):
                del st.session_state["tracked"][pid]
                st.experimental_rerun()

# ---------------- Save Button ----------------
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save Board"):
    save_board(
        user,
        {
            "saved": list(st.session_state["saved"]),
            "tracked": st.session_state["tracked"]
        }
    )
    st.sidebar.success("Board saved!")
