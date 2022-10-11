import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Placeholder")


def user_input():
    disable = True
    text_input = st.text_input("Enter something", "")

    cost_input = st.selectbox('Cost', list(("Pay", "Free", "Both")))
    if cost_input == "Pay" or cost_input == "Both":
        disable = False

    # TODO: replace max_value with correct value
    max_input = st.slider("Pick your cost range",
                   min_value=0.0, max_value=100.00, step=0.25, disabled=disable)

    subject_input = st.multiselect('Subjects', [
        'Business Finance', 'Graphic Design', 'Musical Instruments', 'Web Development'])

    level_input = st.multiselect(
        'Level', ['All Levels', 'Expert', 'Intermediate', 'Beginner'])

    if text_input != "" and len(subject_input) != 0 and len(level_input) != 0:
        return dict(user_input=text_input, cost=cost_input,
                      max_range=max_input, subjects=subject_input, level=level_input)


if __name__ == "__main__":
    user_info = user_input()

    if user_info:
        print (user_info)
