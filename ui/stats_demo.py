import streamlit as st
import sys
import os
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize

st.set_page_config(page_title="Monte Carlo Gacha Simulation", layout="wide")

st.title("📊 Monte Carlo Gacha Simulation")
st.caption("Expected number of pulls until a 5★ appears")

#controls
mode = st.selectbox(
    "Simulation Mode",
    ["No pity", "Soft pity", "Soft pity + 50/50"]
)

if mode == "No pity":
    use_pity, use_5050 = False, False
elif mode == "Soft pity":
    use_pity, use_5050 = True, False
else:
    use_pity, use_5050 = True, True

n = st.slider(
    "Number of simulated players",
    min_value=1000,
    max_value=20000,
    value=10000,
    step=1000
)

run = st.button("▶ Run Simulation")

#simulation
if run:
    with st.spinner("Running Monte Carlo simulation..."):
        results = simulate_players(n, use_pity, use_5050)
        stats = summarize(results)

    st.markdown("---")

    #results
    st.subheader("Results Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean", f"{stats['mean']:.2f}")
    col2.metric("Median", f"{stats['median']:.2f}")
    col3.metric("Std Dev", f"{stats['std']:.2f}")
    col4.metric("90th Percentile", f"{stats['p90']:.2f}")

    st.markdown("---")

    #histogram / count
    st.subheader("Pull Distribution (Histogram)")

    df = pd.DataFrame({"Pulls until 5★": results})
    st.bar_chart(
        df["Pulls until 5★"].value_counts().sort_index(),
        height=300
    )

    #cdf (cumulative distribution function)
    st.subheader("Cumulative Distribution Function (CDF)")

    sorted_vals = np.sort(results)
    cdf = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)

    cdf_df = pd.DataFrame({
        "Pulls": sorted_vals,
        "Probability": cdf
    })

    st.line_chart(cdf_df.set_index("Pulls"), height=300)

    #interpretation (this is optional but i put it here cause why not)
    st.markdown("### Interpretation")
    st.write(
        f"- **50%** of players obtain a 5★ by **~{stats['median']:.0f} pulls**.\n"
        f"- **90%** of players obtain a 5★ by **~{stats['p90']:.0f} pulls**.\n"
        f"- The distribution shows how pity mechanics affect player experience."
    )