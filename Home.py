
import streamlit as st
from annual import Talk_To_Annual_Report
from Analaysis import Analysis
from webiste import website
from Visulizationn import visulizationn

def main():
    st.set_page_config(page_title="FinalyzeChat", layout="wide")

    st.markdown("<span class='center'>", unsafe_allow_html=True)
    st.image("images.png", width=200)
    st.markdown("</span>", unsafe_allow_html=True)

    st.title("FinalyzeChat \n\n **Easy Access to Financial Insights**")

    st.success("""
    Imagine an investor who wants to quickly understand a company's financial health or an employee curious about future growth prospects. 
    Our chatbot, can answer these questions in a clear, concise, and informative way. 
    This not only empowers users but also streamlines information access, ultimately fostering better financial decision-making
    """)

    with open("docs/news.md", "r") as f:
        st.success(f.read())

    with open("docs/main.md", "r") as f:
        st.info(f.read())

    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6; /* Set the background color */
                color: #333; /* Set the text color */
                font-family: Arial, sans-serif; /* Set font */
            }

            .sidebar .sidebar-content {
                background-color: #ffffff; /* Set sidebar background color */
                color: #333; /* Set sidebar text color */
            }

            .stButton>button {
                background-color: #5bc0de; /* Set button background color to light blue */
                color: white; /* Set button text color */
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #31b0d5; /* Change button background color on hover */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Features")

    if st.sidebar.button("Talk to Annual report"):
        st.experimental_set_query_params(page="Talk_To_Annual_Report")

    if st.sidebar.button("Data Visualization"):
        st.experimental_set_query_params(page="visulizationn")

    if st.sidebar.button("Company profile"):
        st.experimental_set_query_params(page="website")

    if st.sidebar.button("Analysis"):
        st.experimental_set_query_params(page="Analysis")


if __name__ == "__main__":
    page = st.experimental_get_query_params().get("page", ["main"])[0]
    if page == "Talk_To_Annual_Report":
        Talk_To_Annual_Report()
    elif page == "visulizationn":
        visulizationn()
    elif page=="website":
        website()
    elif page=="Analysis":
        Analysis()
    else:
        main()