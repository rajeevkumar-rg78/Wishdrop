
import streamlit as st
import pandas as pd
from utils.storage import save_board, get_board
from utils.price import simulate_price_history

st.header("❤️ Boards & Alerts")

products = pd.read_csv("data/sample_products.csv")

user = st.sidebar.text_input("Profile name to save board under", placeholder="Use your profile name")
if user:
    current = get_board(user)
    if "saved" not in st.session_state:
        st.session_state["saved"] = set(current.get("saved", []))
    else:
        st.session_state["saved"].update(current.get("saved", []))
    if "tracked" not in st.session_state:
        st.session_state["tracked"] = dict(current.get("tracked", {}))
    else:
        st.session_state["tracked"].update(current.get("tracked", {}))

st.subheader("Saved Items")
saved_ids = list(st.session_state.get("saved", set()))
saved_df = products[products["id"].isin(saved_ids)]
if saved_df.empty:
    st.info("No saved items yet. Go to **🖼️ Discover** and click ❤️ Save.")
else:
    st.caption("Export your board or adjust alert thresholds.")
    c1, c2 = st.columns([1,1])
    with c1:
        st.download_button("Download Board (CSV)", saved_df.to_csv(index=False), file_name="my_board.csv", mime="text/csv")
    with c2:
        if st.button("Clear Board"):
            st.session_state["saved"] = set()
            st.experimental_rerun()

    cols = st.columns(3, gap="large")
    for i, row in saved_df.reset_index(drop=True).iterrows():
        with cols[i % 3]:
            st.image(row["image_url"], use_container_width=True)
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['brand']} • {row['category']} • {row['store']}")
            st.markdown(f"${row['price']:,.2f}  ~  ~~${row['msrp']:,.2f}~~  •  **-{int(row['discount_pct'])}%**")
            thr = st.number_input("Alert threshold %", min_value=1, max_value=50, value=st.session_state.get("tracked", {}).get(row["id"], 10), key=f"thr_{row['id']}")
            if st.button("Enable Alert", key=f"enable_{row['id']}"):
                tracked = st.session_state.get("tracked", {})
                tracked[row["id"]] = thr
                st.session_state["tracked"] = tracked
                st.success(f"Alerts enabled for {row['name']} @ {thr}%")

st.subheader("Alerts & Trends")
tracked = st.session_state.get("tracked", {})
if not tracked:
    st.info("No tracked items yet.")
else:
    alerts = []
    if "price_cache" not in st.session_state:
        st.session_state.price_cache = {}
    for tid, thr in tracked.items():
        row = products[products["id"] == tid].iloc[0]
        if tid not in st.session_state.price_cache:
            st.session_state.price_cache[tid] = simulate_price_history(row["price"], days=60)
        series = st.session_state.price_cache[tid]
        min30 = series[-30:].min()
        drop = (row["price"] - min30) / row["price"] * 100.0
        if drop <= thr:
            alerts.append((row, drop))

    if alerts:
        for row, drop in alerts:
            with st.container(border=True):
                st.markdown(f"### 🔔 {row['name']}")
                st.caption(f"{row['brand']} • {row['store']} • {row['category']}")
                st.write(f"**Now:** ${row['price']:,.2f} • **30‑day low proximity:** {drop:.1f}%")
                st.link_button("Open product", row["product_url"])
    else:
        st.success("No alerts met your thresholds today.")

st.markdown("---")
if user:
    if st.button("💾 Save Board to Profile"):
        payload = {
            "saved": list(st.session_state.get("saved", set())),
            "tracked": st.session_state.get("tracked", {})
        }
        save_board(user, payload)
        st.success("Board saved to your profile.")
