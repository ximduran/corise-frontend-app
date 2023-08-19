import streamlit as st
import modal
import json
import os

def main():
    st.title("Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]
        display_newsletter_content(podcast_info)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take upto 5 mins, please be patient.")

    if process_button:
        podcast_info = process_podcast_info(url)
        display_newsletter_content(podcast_info)

def display_newsletter_content(podcast_info):
    # Right section - Newsletter content
    st.header("Newsletter Content")

    # Display the podcast title
    st.subheader("Episode Title")
    st.write(podcast_info['podcast_details']['episode_title'])

    # Display the podcast summary and the cover image in a side-by-side layout
    col1, col2 = st.columns([7, 3])

    with col1:
        # Display the podcast episode summary
        st.subheader("Podcast Episode Summary")
        st.write(podcast_info['podcast_summary'])

    with col2:
        st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

    # Display the podcast guest and their details in a side-by-side layout
    col3, col4 = st.columns([3, 7])

    with col3:
        st.subheader("Podcast Guest")
        st.write(podcast_info['podcast_guest']['name'])

    with col4:
        write_guest_summary(st, podcast_info)

    # Display the five key moments
    st.subheader("Key Moments")
    key_moments = podcast_info['podcast_highlights']
    for moment in key_moments:
        st.markdown(
            f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def write_guest_summary(st, podcast_info):
    st.subheader("Podcast Guest Details")
    if podcast_info['podcast_guest']['summary']:
        st.write(podcast_info["podcast_guest"]['summary'])
    else:
        podcast_guest_title = podcast_info["podcast_guest"]['title']
        podcast_guest_org = podcast_info["podcast_guest"]['organization']
        short_description = f"{podcast_guest_title} at {podcast_guest_org}"
        st.write(short_description)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
