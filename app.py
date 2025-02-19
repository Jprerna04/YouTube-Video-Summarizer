import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##loads all the env variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube video summariser. You will be taking 
the transcript text and summarising the entrire video and 
providing the important summary, key points and highlights in points within 300 words.
Please provide the summary of the text given here: """

##for video id
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)

    # Case 1: Standard YouTube URL (youtube.com/watch?v=...)
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]

    # Case 2: Shortened YouTube URL (youtu.be/...)
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    return None  # If the URL is invalid


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_link)
        print(video_id)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript+=" " + i["text"]

        return transcript

    except Exception as e:
        raise e

##here we are summarising the transcript we are getting from google gemini pro
def generate_gemini_content(transcript_text, prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link=st.text_input("Enter YouTube Video Link: ")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)