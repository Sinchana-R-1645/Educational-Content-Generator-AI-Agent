elif menu == "Analytics":
    show_analysis()

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
