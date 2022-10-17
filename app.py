import os

import openai
import streamlit as st

# from textwrap import dedent


openai.api_key = os.getenv("OPENAI_API_KEY")


@st.cache
def is_my_idea_good_or_bad(idea):
    prompt = (f"Classify the following hackathon idea as good or bad:\n{idea}.\n",)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.8,
        max_tokens=32,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def main():
    st.header("💡 Is my hackathon idea good or bad?")
    # description_text = dedent("""
    # """)
    # st.write(description_text)

    idea = st.text_area("My hackathon idea is...")
    button = st.button("Is it good... or bad?")

    if button:
        good_or_bad = is_my_idea_good_or_bad(idea)
        st.write(good_or_bad)


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()
