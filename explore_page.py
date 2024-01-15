import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Data Cleaning
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

#Load the data and apply all the transformation
@st.cache_data#Now we have executed this one time, then it will cache it and it is available the next time again
def load_data():
    df = pd.read_csv("C:\Absar\Important\ML Project\stack-overflow-developer-survey-2023\survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2023
    """
    )
    
    #PIE CHART
    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)
    
    #BAR CHART
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)#average salary for each country
    st.bar_chart(data)

    #LINE CHART
    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)#average salary as per the experience
    st.line_chart(data)
