import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.database import get

def show_analysis():

    st.header("📊 Performance Analytics")

    data = get()

    if data:
        df = pd.DataFrame(data, columns=["Subject","Score","Total"])
        df["Percentage"] = (df["Score"] / df["Total"]) * 100

        st.dataframe(df)

        plt.figure()
        plt.plot(df["Percentage"], marker="o")
        plt.title("Performance")
        plt.ylabel("Percentage")
        st.pyplot(plt)

    else:
        st.info("No data yet")
