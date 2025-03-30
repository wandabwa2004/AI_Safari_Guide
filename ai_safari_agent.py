# import streamlit as st
# import asyncio
# from safari_manager import SafariManager
# from agents import set_default_openai_key
# import json

# # def tts(text):
# #     from pathlib import Path
# #     from openai import OpenAI

# #     client = OpenAI()
# #     speech_file_path = Path(__file__).parent / f"safari_tour.mp3"
        
# #     response = client.audio.speech.create(
# #         model="gpt-4o-mini-tts",
# #         voice="nova",
# #         input=text,
# #         instructions="""You are a friendly, knowledgeable safari guide. Speak naturally and conversationally, as if walking alongside the visitor.
# #         Use a warm, inviting tone with natural transitions between topics. Avoid robotic or overly formal language."""
# #     )
# #     response.stream_to_file(speech_file_path)
# #     return speech_file_path
# def tts(text):
#     from pathlib import Path
#     from openai import OpenAI
#     # Retrieve the API key from Streamlit's session_state
#     api_key = st.session_state.get("OPENAI_API_KEY")
#     if not api_key:
#         raise ValueError("API key is not set.")
    
#     client = OpenAI(api_key=api_key)
#     speech_file_path = Path(__file__).parent / "safari_tour.mp3"
        
#     response = client.audio.speech.create(
#         model="gpt-4o-mini-tts",
#         voice="nova",
#         input=text,
#         instructions="""You are a friendly, knowledgeable safari guide. Speak naturally and conversationally, as if walking alongside the visitor.
#         Use a warm, inviting tone with natural transitions between topics. Avoid robotic or overly formal language."""
#     )
#     response.stream_to_file(speech_file_path)
#     return speech_file_path

# def run_async(func, *args, **kwargs):
#     try:
#         return asyncio.run(func(*args, **kwargs))
#     except RuntimeError:
#         loop = asyncio.get_event_loop()
#         return loop.run_until_complete(func(*args, **kwargs))

# st.set_page_config(
#     page_title="AI Safari Companion",
#     page_icon="🦁",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# with st.sidebar:
#     st.title("🔑 Settings")
#     api_key = st.text_input("OpenAI API Key:", type="password")
#     if api_key:
#         st.session_state["OPENAI_API_KEY"] = api_key
#         st.success("API key saved!")

# set_default_openai_key(api_key)

# st.title("🦁 AI Safari Companion")
# st.markdown("""
#     <div class='welcome-card'>
#         <h3>Welcome to your personalized safari tour guide!</h3>
#         <p>Explore Kenyan landscapes with engaging narratives on nature, environment, culture, and safety.</p>
#     </div>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns([2, 1])

# with col1:
#     st.markdown("### 📍 Where would you like to explore?")
#     location = st.text_input("", placeholder="Enter a national park or safari location...")
    
#     st.markdown("### 🎯 Which aspects interest you?")
#     interests = st.multiselect(
#         "",
#         options=["Biodiversity", "Environment", "Culture", "Safety"],
#         default=["Biodiversity", "Culture"],
#         help="Select topics for your safari experience"
#     )

# with col2:
#     st.markdown("### ⏱️ Tour Settings")
#     duration = st.slider(
#         "Tour Duration (minutes)",
#         min_value=5,
#         max_value=60,
#         value=10,
#         step=5,
#         help="Choose how long you'd like your safari tour to be"
#     )
    
#     st.markdown("### 🎙️ Voice Settings")
#     voice_style = st.selectbox(
#         "Guide's Voice Style",
#         options=["Friendly & Casual", "Professional & Detailed", "Enthusiastic & Energetic"],
#         help="Select the personality of your safari guide"
#     )

# if st.button("🦁 Generate Safari Tour", type="primary"):
#     if "OPENAI_API_KEY" not in st.session_state:
#         st.error("Please enter your OpenAI API key in the sidebar.")
#     elif not location:
#         st.error("Please enter a safari location.")
#     elif not interests:
#         st.error("Please select at least one interest.")
#     else:
#         with st.spinner(f"Creating your safari tour for {location}..."):
#             mgr = SafariManager()
#             final_tour = run_async(
#                 mgr.run, location, interests, duration
#             )

#             with st.expander("📝 Tour Content", expanded=True):
#                 st.markdown(final_tour)
            
#             with st.spinner("🎙️ Generating audio tour..."):
#                 progress_bar = st.progress(0)
#                 tour_audio = tts(final_tour)
#                 progress_bar.progress(100)
            
#             st.markdown("### 🎧 Listen to Your Safari Tour")
#             st.audio(tour_audio, format="audio/mp3")
            
#             with open(tour_audio, "rb") as file:
#                 st.download_button(
#                     label="📥 Download Audio Tour",
#                     data=file,
#                     file_name=f"{location.lower().replace(' ', '_')}_safari_tour.mp3",
#                     mime="audio/mp3"
#                 )

import streamlit as st
import asyncio
from safari_manager import SafariManager
from agents import set_default_openai_key
import json

def tts(text):
    from pathlib import Path
    from openai import OpenAI

    api_key = st.session_state.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set.")
    
    client = OpenAI(api_key=api_key)
    speech_file_path = Path(__file__).parent / "safari_tour.mp3"
        
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text,
        instructions="""You are a friendly, knowledgeable safari guide. Speak naturally and conversationally, as if walking alongside the visitor.
        Use a warm, inviting tone with natural transitions between topics. Avoid robotic or overly formal language."""
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

def run_async(func, *args, **kwargs):
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

st.set_page_config(
    page_title="AI Safari Companion",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.title("🔑 Settings")
    api_key = st.text_input("OpenAI API Key:", type="password")
    if api_key:
        st.session_state["OPENAI_API_KEY"] = api_key
        st.success("API key saved!")
    
    # Add language selection here
    language = st.selectbox(
        "Language",
        options=["English", "Swahili"],
        help="Choose your preferred language for the tour"
    )
    st.session_state["LANGUAGE"] = language

set_default_openai_key(api_key)

st.title("🦁 AI Safari Companion")
st.markdown("""
    <div class='welcome-card'>
        <h3>Welcome to your personalized safari tour guide!</h3>
        <p>Explore Kenyan landscapes with engaging narratives on nature, culture, and safety.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📍 Where would you like to explore?")
    location = st.text_input("", placeholder="Enter a national park or safari location...")
    
    st.markdown("### 🎯 Which aspects interest you?")
    interests = st.multiselect(
        "",
        options=["Biodiversity", "Environment", "Culture", "Safety"],
        default=["Biodiversity", "Culture"],
        help="Select topics for your safari experience"
    )

with col2:
    st.markdown("### ⏱️ Tour Settings")
    duration = st.slider(
        "Tour Duration (minutes)",
        min_value=5,
        max_value=60,
        value=10,
        step=5,
        help="Choose how long you'd like your safari tour to be"
    )
    
    st.markdown("### 🎙️ Voice Settings")
    voice_style = st.selectbox(
        "Guide's Voice Style",
        options=["Friendly & Casual", "Professional & Detailed", "Enthusiastic & Energetic"],
        help="Select the personality of your safari guide"
    )

if st.button("🦁 Generate Safari Tour", type="primary"):
    if "OPENAI_API_KEY" not in st.session_state:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not location:
        st.error("Please enter a safari location.")
    elif not interests:
        st.error("Please select at least one interest.")
    else:
        with st.spinner(f"Creating your safari tour for {location}..."):
            mgr = SafariManager()
            # Pass the language choice to the manager
            final_tour = run_async(
                mgr.run, location, interests, duration, st.session_state.get("LANGUAGE")
            )

            with st.expander("📝 Tour Content", expanded=True):
                st.markdown(final_tour)
            
            with st.spinner("🎙️ Generating audio tour..."):
                progress_bar = st.progress(0)
                tour_audio = tts(final_tour)
                progress_bar.progress(100)
            
            st.markdown("### 🎧 Listen to Your Safari Tour")
            st.audio(tour_audio, format="audio/mp3")
            
            with open(tour_audio, "rb") as file:
                st.download_button(
                    label="📥 Download Audio Tour",
                    data=file,
                    file_name=f"{location.lower().replace(' ', '_')}_safari_tour.mp3",
                    mime="audio/mp3"
                )