import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter



class Banner:
    def __init__(self):
        self.pity_5 = 0
        self.pity_4 = 0
        self.guaranteed = False

        self.history = []              # all pulls
        self.five_star_history = []    # (type, pity)

        self.counts = Counter()

    def pull(self):
        self.pity_5 += 1
        self.pity_4 += 1

        # 5* logic
        if self.pity_5 >= 90:
            return self._five_star()

        # base 0.6%
        import random
        if random.random() < 0.006:
            return self._five_star()

        # 4* logic
        if self.pity_4 >= 10:
            return self._four_star()

        if random.random() < 0.051:
            return self._four_star()

        # 3*
        self.counts["3★"] += 1
        self.history.append("3★")
        return "3★"

    def _five_star(self):
        self.pity_5 = 0
        self.pity_4 = 0

        if self.guaranteed:
            result = "5★ LIMITED"
            self.guaranteed = False
        else:
            import random
            if random.random() < 0.5:
                result = "5★ LIMITED"
            else:
                result = "5★ STANDARD"
                self.guaranteed = True

        self.counts["5★"] += 1
        self.history.append(result)
        self.five_star_history.append((result, len(self.history)))
        return result

    def _four_star(self):
        self.pity_4 = 0
        self.counts["4★"] += 1
        self.history.append("4★")
        return "4★"



# session setup
if "banner" not in st.session_state:
    st.session_state.banner = Banner()

if "page" not in st.session_state:
    st.session_state.page = "banner"

if "history_page" not in st.session_state:
    st.session_state.history_page = 0


banner = st.session_state.banner



# ui functions
def banner_page():
    st.title("🎮 Character Event Wish")

    c1, c2, c3 = st.columns(3)
    c1.metric("5★ Pity", banner.pity_5)
    c2.metric("4★ Pity", banner.pity_4)
    c3.metric("Guaranteed", banner.guaranteed)

    st.divider()

    a, b, c = st.columns(3)

    if a.button("Wish x1"):
        banner.pull()

    if b.button("Wish x10"):
        for _ in range(10):
            banner.pull()

    if c.button("View History"):
        st.session_state.page = "history"

    st.subheader("Recent Pulls")
    for pull in banner.history[-5:][::-1]:
        st.write(pull)


def history_page():
    st.title("📜 Wish History")

    PAGE_SIZE = 10
    total = len(banner.history)

    start = max(0, total - (st.session_state.history_page + 1) * PAGE_SIZE)
    end = total - st.session_state.history_page * PAGE_SIZE

    page_items = banner.history[start:end]

    for item in reversed(page_items):
        st.write(item)

    c1, c2, c3 = st.columns(3)

    if c1.button("⬅ Newer"):
        st.session_state.history_page = max(0, st.session_state.history_page - 1)

    if c2.button("Back to Banner"):
        st.session_state.page = "banner"

    if c3.button("Older ➡"):
        if start > 0:
            st.session_state.history_page += 1

    render_stats()
    render_pie()
    render_recent_fives()


def render_stats():
    st.subheader("📊 Player Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pulls", len(banner.history))
    col2.metric("5★ Pulls", banner.counts["5★"])
    col3.metric("4★ Pulls", banner.counts["4★"])


def render_pie():
    st.subheader("🎯 Rarity Distribution")

    labels = ["3★", "4★", "5★"]
    values = [
        banner.counts["3★"],
        banner.counts["4★"],
        banner.counts["5★"],
    ]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)


def render_recent_fives():
    st.subheader("🌟 Recent 5★ Pulls")

    for char, pull_num in banner.five_star_history[-5:]:
        pity = pull_num
        if pity < 75:
            color = "green"
        elif pity < 85:
            color = "orange"
        else:
            color = "red"

        st.markdown(
            f"<div style='color:{color}'>⭐ {char} (pull {pity})</div>",
            unsafe_allow_html=True
        )



# router
if st.session_state.page == "banner":
    banner_page()
else:
    history_page()