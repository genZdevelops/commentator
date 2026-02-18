import streamlit as st
import moviepy as mp  # Changed from moviepy.editor
import os
import tempfile

# --- UI Configuration ---
st.set_page_config(page_title="Video Audio Extractor", page_icon="🎬")
st.title("🎬 Video Silencer & Audio Extractor")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "input_video.mp4")
        audio_path = os.path.join(temp_dir, "extracted_audio.mp3")
        video_path = os.path.join(temp_dir, "silent_video.mp4")

        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("Processing with MoviePy v2.x...")

        try:
            # In MoviePy 2.x, we use VideoFileClip directly from moviepy
            video = mp.VideoFileClip(input_path)
            
            # 1. Extract Audio
            if video.audio is not None:
                # Note: .write_audiofile remains the same
                video.audio.write_audiofile(audio_path)
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="🎵 Download Extracted Audio",
                        data=f,
                        file_name="extracted_audio.mp3",
                        mime="audio/mpeg"
                    )
            
            # 2. Create Silent Video
            # .without_audio() is still supported in v2.x
            silent_video = video.without_audio()
            silent_video.write_videofile(video_path, codec="libx264")
            
            with open(video_path, "rb") as f:
                st.download_button(
                    label="### 🔇 Download Silent Video",
                    data=f,
                    file_name="silent_video.mp4",
                    mime="video/mp4"
                )

            video.close()
            silent_video.close()
            st.success("Processing complete!")

        except Exception as e:
            st.error(f"Error: {e}")
