import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.banner import Banner
from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize



#streamlit page config
st.set_page_config(
    page_title = "Gacha Simulator",
    layout = "wide"
)

st.title("Gacha Simulator")
st.caption("COMP6049001 || Algorithm Design & Analysis Project")



#sidebar controls
st.sidebar.header("System Configuration")

system = st.sidebar.selectbox(
    "Select Gacha System:",
    ["No Pity", "Soft Pity", "Soft Pity + 50/50"]
)

if system == "No Pity":
    use_pity = False
    use_5050 = False
elif system == "Soft Pity":
    use_pity = True
    use_5050 = False
else:
    use_pity = True
    use_5050 = True

st.sidebar.markdown("---")

#reset banner when system changes
if "last_system" not in st.session_state:
    st.session_state.last_system = system

if system != st.session_state.last_system:
    st.session_state.banner = Banner(use_pity, use_5050)
    st.session_state.history = []
    st.session_state.last_system = system



#tabs
tab1, tab2, tab3 = st.tabs(["🎰 Pull Demo", "📊 Simulation Stats", "📜 History"])

#tab 1: pull demo
with tab1:
    st.subheader("Interactive Pull Demo")

    # Initialize banner state
    if "banner" not in st.session_state:
        st.session_state.banner = Banner(use_pity, use_5050)
        st.session_state.history = []

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Pity", st.session_state.banner.pity)
    col2.metric("Guaranteed", st.session_state.banner.guaranteed)
    col3.metric("System", system)

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        if st.button("1 Pull"):
            result = st.session_state.banner.pull()
            st.session_state.history.append(result)

    with colB:
        if st.button("10 Pull"):
            for _ in range(10):
                result = st.session_state.banner.pull()
                st.session_state.history.append(result)

    if st.button("🔄 Reset Banner"):
        st.session_state.banner = Banner(use_pity, use_5050)
        st.session_state.history = []

    st.markdown("### Pull History (Last 10)")
    if st.session_state.history:
        st.write(st.session_state.history[-10:])
    else:
        st.write("No pulls yet.")

#tab 2: monte carlo simul
with tab2:
    st.subheader("Monte Carlo Simulation")

    n_players = st.slider(
        "Number of simulated players",
        min_value=1000,
        max_value=20000,
        value=10000,
        step=1000
    )

    if st.button("▶ Run Simulation"):
        with st.spinner("Running simulation..."):
            results = simulate_players(
                n=n_players,
                use_pity=use_pity,
                use_5050=use_5050
            )

            stats = summarize(results)

        st.markdown("### Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Mean", f"{stats['mean']:.2f}")
        col2.metric("Median", f"{stats['median']:.2f}")
        col3.metric("Std Dev", f"{stats['std']:.2f}")
        col4.metric("p90", f"{stats['p90']:.2f}")

        st.markdown("### Cumulative Distribution (CDF)")
        st.line_chart(sorted(results))

        st.markdown(
            """
            **Interpretation:**  
            The curve shows the probability that a player obtains the featured
            character by a given number of pulls.  
            Steeper curves indicate lower variance and fairer outcomes.
            """
        )

#tab 3: history
with tab3:
    st.subheader("User Pull History & Stats")
    history = st.session_state.get("history", [])
    total_pulls = len(history)
    five_star_count = history.count("LIMITED") + history.count("STANDARD")
    five_star_percent = (five_star_count / total_pulls * 100) if total_pulls > 0 else 0


    if five_star_count > 0:
        win_5050 = history.count("LIMITED")
        win_rate_5050 = win_5050 / five_star_count * 100
    else:
        win_5050 = 0
        win_rate_5050 = 0

    st.metric("Total Pulls", total_pulls)
    st.metric("5★ Pulled", five_star_count)
    st.metric("5★ Rate (%)", f"{five_star_percent:.2f}")
    st.metric("50/50 Win Rate (%)", f"{win_rate_5050:.2f}")

    st.markdown("### Full Pull History")
    if history:
        st.write(history)
    else:
        st.write("No pulls yet.")
