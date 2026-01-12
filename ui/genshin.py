import streamlit as st
import random
import base64
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

# =========================
# PATH + PAGE CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

st.set_page_config(page_title="Gacha Simulation", layout="wide")

# =========================
# BACKGROUND CSS
# =========================
def img_to_base64(path: Path):
    return base64.b64encode(path.read_bytes()).decode()

bg64 = img_to_base64(ASSETS / "sky_bg.jpeg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1, h2, h3 {{
        color: white;
        text-align: center;
    }}

    .block-container {{
        padding-top: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# GACHA LOGIC
# =========================
class Banner:
    def __init__(self):
        self.pity_5 = 0
        self.pity_4 = 0
        self.guaranteed = False

        self.history = []
        self.counts = Counter()
        self.five_star_pities = []
        self.four_star_pities = []
        self.five_star_results = []  # "limited" or "standard"

    def five_star_rate(self):
        if self.pity_5 < 75:
            return 0.006
        return min(1.0, 0.006 + (self.pity_5 - 75) * 0.06)

    def pull(self):
        self.pity_5 += 1
        self.pity_4 += 1

        # 5★
        if random.random() < self.five_star_rate() or self.pity_5 >= 90:
            return self._five_star()

        # 4★
        if self.pity_4 >= 10 or random.random() < 0.051:
            return self._four_star()

        # 3★
        self.counts["3★"] += 1
        self.history.append("3★ Weapon")
        return "3★ Weapon"

    def _five_star(self):
        self.counts["5★"] += 1
        self.five_star_pities.append(self.pity_5)
        self.pity_5 = 0
        self.pity_4 = 0

        if self.guaranteed:
            result = "5★ Venti"
            self.guaranteed = False
            self.five_star_results.append("limited")
        else:
            if random.random() < 0.5:
                result = "5★ Venti"
                self.five_star_results.append("limited")
            else:
                result = "5★ Qiqi"
                self.guaranteed = True
                self.five_star_results.append("standard")

        self.history.append(result)
        return result

    def _four_star(self):
        self.counts["4★"] += 1
        self.four_star_pities.append(self.pity_4)
        self.pity_4 = 0
        self.history.append("4★ Fischl")
        return "4★ Fischl"

    # ===== STATS =====
    def avg_5_pity(self):
        return sum(self.five_star_pities) / len(self.five_star_pities) if self.five_star_pities else 0

    def avg_4_pity(self):
        return sum(self.four_star_pities) / len(self.four_star_pities) if self.four_star_pities else 0

    def winrate_5050(self):
        total = len(self.five_star_results)
        if total == 0:
            return 0
        return self.five_star_results.count("limited") / total

# =========================
# SESSION STATE
# =========================
if "screen" not in st.session_state:
    st.session_state.screen = "banner"

if "banner" not in st.session_state:
    st.session_state.banner = Banner()

if "last_results" not in st.session_state:
    st.session_state.last_results = []

if "history_page" not in st.session_state:
    st.session_state.history_page = 0

banner = st.session_state.banner

# =========================
# ACTION HANDLER
# =========================
def handle_wish(n):
    st.session_state.last_results = [banner.pull() for _ in range(n)]
    st.session_state.screen = "results"
    st.rerun()

# =========================
# SCREENS
# =========================
def banner_screen():
    _, center, _ = st.columns([1, 6, 1])
    with center:
        st.image(ASSETS / "banner.jpeg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, _, right = st.columns([3, 4, 3])

    with left:
        if st.button("📊 Details", use_container_width=True):
            st.session_state.screen = "details"
            st.rerun()
        if st.button("📜 History", use_container_width=True):
            st.session_state.screen = "history"
            st.rerun()

    with right:
        if st.button("✨ Wish x1", use_container_width=True):
            handle_wish(1)
        if st.button("🌟 Wish x10", use_container_width=True):
            handle_wish(10)

def results_screen():
    st.markdown("<h2>Wish Results</h2>", unsafe_allow_html=True)

    img_map = {
        "3★ Weapon": "weapon.jpeg",
        "4★ Fischl": "fischl.jpeg",
        "5★ Venti": "venti.jpeg",
        "5★ Qiqi": "qiqi.jpeg",
    }

    cols = st.columns(5)
    for i, res in enumerate(st.session_state.last_results):
        with cols[i % 5]:
            st.image(ASSETS / img_map[res], use_container_width=True)
            st.caption(res)

    if st.button("Return"):
        st.session_state.screen = "banner"
        st.rerun()

def history_screen():
    st.markdown("<h2>Wish History</h2>", unsafe_allow_html=True)

    PAGE = 10
    total = len(banner.history)
    page = st.session_state.history_page
    total_pages = max(1, (total + PAGE - 1) // PAGE)

    start = max(0, total - (page + 1) * PAGE)
    end = total - page * PAGE

    if total == 0:
        st.info("No pulls yet.")
    else:
        for item in reversed(banner.history[start:end]):
            st.write(item)

    c1, c2, c3 = st.columns([1, 2, 1])

    with c1:
        if st.button("⬅ Newer", disabled=page == 0):
            st.session_state.history_page -= 1
            st.rerun()

    with c2:
        st.markdown(f"<p style='text-align:center'>Page {page+1} / {total_pages}</p>", unsafe_allow_html=True)

    with c3:
        if st.button("Older ➡", disabled=start == 0):
            st.session_state.history_page += 1
            st.rerun()

    if st.button("Return"):
        st.session_state.screen = "banner"
        st.rerun()

def details_screen():
    st.markdown("<h2>Player Statistics</h2>", unsafe_allow_html=True)

    total_pulls = len(banner.history)
    if total_pulls == 0:
        st.info("No pulls yet.")
        if st.button("Return"):
            st.session_state.screen = "banner"
            st.rerun()
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pulls", total_pulls)
    c2.metric("5★ Pulls", banner.counts["5★"])
    c3.metric("4★ Pulls", banner.counts["4★"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Avg 5★ Pity", round(banner.avg_5_pity(), 2))
    c5.metric("Avg 4★ Pity", round(banner.avg_4_pity(), 2))
    c6.metric("50/50 Win Rate", f"{banner.winrate_5050() * 100:.2f}%")

    st.subheader("Rarity Distribution")

    labels = ["3★", "4★", "5★"]
    values = [banner.counts[x] for x in labels]

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)

    if st.button("Return"):
        st.session_state.screen = "banner"
        st.rerun()

# =========================
# ROUTER
# =========================
if st.session_state.screen == "banner":
    banner_screen()
elif st.session_state.screen == "results":
    results_screen()
elif st.session_state.screen == "history":
    history_screen()
elif st.session_state.screen == "details":
    details_screen()