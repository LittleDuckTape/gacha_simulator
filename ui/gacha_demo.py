import streamlit as st
import sys
import os
import time

#to fix imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from core.banner import Banner

st.set_page_config(page_title="Player Gacha Demo", layout="wide")
st.title("🎮 Character Event Wish")

#sidebar: mode select
mode = st.sidebar.selectbox(
    "Banner Mode",
    ["No pity", "Soft pity", "Soft pity + 50/50"]
)

if mode == "No pity":
    use_pity, use_5050 = False, False
elif mode == "Soft pity":
    use_pity, use_5050 = True, False
else:
    use_pity, use_5050 = True, True

#reset banner if mode changes
if "banner" not in st.session_state or st.session_state.get("mode") != mode:
    st.session_state.banner = Banner(use_pity, use_5050)
    st.session_state.history = []
    st.session_state.mode = mode

#banner info
col1, col2, col3 = st.columns(3)
col1.metric("5★ Pity", st.session_state.banner.pity)
col2.metric("4★ Pity", st.session_state.banner.four_star_pity)
col3.metric("Guaranteed", st.session_state.banner.guaranteed)

st.markdown("---")

#pulling buttons
def do_pull():
    with st.spinner("✨ Shooting star..."):
        time.sleep(0.4)
    result = st.session_state.banner.pull()
    st.session_state.history.append(result)

colA, colB, colC = st.columns(3)

with colA:
    if st.button("Wish x1"):
        do_pull()

with colB:
    if st.button("Wish x10"):
        for _ in range(10):
            do_pull()

with colC:
    if st.button("Reset Banner"):
        st.session_state.banner = Banner(use_pity, use_5050)
        st.session_state.history = []

#recent results
st.subheader("Recent Pulls")

if st.session_state.history:
    for pull in st.session_state.history[-10:][::-1]:
        if pull["rarity"] == "5★":
            st.success(f"5★ {pull['type']} (pity {pull['pity']})")
        elif pull["rarity"] == "4★":
            st.warning(f"4★ (pity {pull['pity']})")
        else:
            st.write("3★")
else:
    st.write("No pulls yet.")