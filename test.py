import streamlit as st
# if 'count' not in st.session_state:
#     st.session_state.count = 2
# cur_day = st.sidebar.slider("请选择您想查看的天", 1, 31, st.session_state.count)
cur_day = st.sidebar.slider("请选择您想查看的天", 1, 31, 23, key="count")
if st.button('Say hello'):
    # cur_day += 1
    # st.session_state.count += 1
    st.session_state.slider_value += 1
    st.write(cur_day)
else:
    st.write('Goodbye')


# Define a function to update the slider value based on the stored value

def update_slider():
    # Get the stored value from the SessionState object
    stored_value = st.session_state.slider_value

    # Update the slider widget's value
    slider_value = st.slider('Select a value:', 0, 100,
                             value=stored_value, key='slider')

    # Store the updated slider value back in the SessionState object
    st.session_state.slider_value = slider_value


# Initialize the SessionState object with a default slider value of 50
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = 50

# Call the update_slider function to display the slider widget and update its value
update_slider()
