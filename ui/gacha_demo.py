import streamlit as st
import random
import matplotlib.pyplot as plt
from collections import Counter


# banner logic
class Banner:
    def __init__(self, soft_pity=False, use_5050=False):
        self.soft_pity = soft_pity
        self.use_5050 = use_5050

        self.pity_5 = 0
        self.pity_4 = 0
        self.guaranteed = False

        self.history = []
        self.five_star_pities = []
        self.four_star_pities = []
        self.counts = Counter()

    def five_star_rate(self):
        if not self.soft_pity:
            return 0.006
        if self.pity_5 < 75:
            return 0.006
        return min(1.0, 0.006 + (self.pity_5 - 75) * 0.06)

    def pull(self):
        self.pity_5 += 1
        self.pity_4 += 1

        # 5* check
        if random.random() < self.five_star_rate() or self.pity_5 >= 90:
            return self._five_star()

        # 4* check
        if self.pity_4 >= 10 or random.random() < 0.051:
            return self._four_star()

        # 3*
        self.counts["3★"] += 1
        self.history.append("3★")
        return "3★"

    def _five_star(self):
        self.counts["5★"] += 1
        self.five_star_pities.append(self.pity_5)

        self.pity_5 = 0
        self.pity_4 = 0

        if self.use_5050:
            if self.guaranteed:
                result = "5★ LIMITED"
                self.guaranteed = False
            else:
                if random.random() < 0.5:
                    result = "5★ LIMITED"
                else:
                    result = "5★ STANDARD"
                    self.guaranteed = True
        else:
            result = "5★"

        self.history.append(result)
        return result

    def _four_star(self):
        self.counts["4★"] += 1
        self.four_star_pities.append(self.pity_4)

        self.pity_4 = 0
        self.history.append("4★")
        return "4★"

    # stats stuff
    def avg_5_pity(self):
        return sum(self.five_star_pities) / len(self.five_star_pities) if self.five_star_pities else 0

    def avg_4_pity(self):
        return sum(self.four_star_pities) / len(self.four_star_pities) if self.four_star_pities else 0

    def winrate_5050(self):
        if not self.use_5050:
            return None
        wins = sum(1 for x in self.history if x == "5★ LIMITED")
        total = sum(1 for x in self.history if x.startswith("5★"))
        return wins / total if total else 0



# session setup
def create_banner(mode):
    if mode == "No pity":
        return Banner(False, False)
    if mode == "Soft pity":
        return Banner(True, False)
    return Banner(True, True)

if "mode" not in st.session_state:
    st.session_state.mode = "Soft pity + 50/50"

if "banner" not in st.session_state:
    st.session_state.banner = create_banner(st.session_state.mode)

if "history_page" not in st.session_state:
    st.session_state.history_page = 0



# UI stuff
st.title("🎰 Gacha Simulator – Player Demo")

mode = st.selectbox(
    "Banner Mode",
    ["No pity", "Soft pity", "Soft pity + 50/50"],
    index=["No pity", "Soft pity", "Soft pity + 50/50"].index(st.session_state.mode)
)

# Reset banner on mode change
if mode != st.session_state.mode:
    st.session_state.mode = mode
    st.session_state.banner = create_banner(mode)
    st.session_state.history_page = 0

banner = st.session_state.banner

tabs = st.tabs(["🎮 Main", "📜 History", "📊 Stats"])

# main tab
with tabs[0]:
    st.subheader("Current Banner State")

    c1, c2, c3 = st.columns(3)
    c1.metric("5★ Pity", banner.pity_5)
    c2.metric("4★ Pity", banner.pity_4)
    c3.metric("Guaranteed", banner.guaranteed)

    if st.button("Wish x1"):
        banner.pull()

    if st.button("Wish x10"):
        for _ in range(10):
            banner.pull()

    st.subheader("Recent Pulls")
    for pull in banner.history[-5:][::-1]:
        st.write(pull)


# history tab
with tabs[1]:
    st.subheader("Wish History")

    PAGE_SIZE = 10
    total = len(banner.history)

    current_page = st.session_state.history_page + 1
    st.markdown(f"### Page {current_page}")

    start = max(0, total - (st.session_state.history_page + 1) * PAGE_SIZE)
    end = total - st.session_state.history_page * PAGE_SIZE

    if total == 0:
        st.info("No pulls yet.")
    else:
        for item in reversed(banner.history[start:end]):
            st.write(item)

    c1, _, c3 = st.columns([1, 2, 1])

    if c1.button("⬅ Newer", disabled=st.session_state.history_page == 0):
        st.session_state.history_page -= 1

    if c3.button("Older ➡", disabled=start == 0):
        st.session_state.history_page += 1


# stats tab
with tabs[2]:
    st.subheader("Player Statistics")

    total_pulls = len(banner.history)

    if total_pulls == 0:
        st.info("No pulls yet. Make some wishes to see statistics.")
        st.stop()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pulls", total_pulls)
    c2.metric("5★ Pulls", banner.counts["5★"])
    c3.metric("4★ Pulls", banner.counts["4★"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Avg 5★ Pity", round(banner.avg_5_pity(), 2))
    c5.metric("Avg 4★ Pity", round(banner.avg_4_pity(), 2))

    winrate = banner.winrate_5050()
    if winrate is not None:
        c6.metric("50/50 Win Rate", f"{winrate * 100:.2f}%")

    st.subheader("Rarity Distribution")

    labels = ["3★", "4★", "5★"]
    values = [banner.counts[x] for x in labels]

    if sum(values) > 0:
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)