import streamlit as st
import moviepy.editor as mp
import os
import tempfile

# --- UI Configuration ---
st.set_page_config(page_title="Video Audio Extractor", page_icon="🎬")
st.title("🎬 Video Silencer & Audio Extractor")
st.markdown("Upload a video to extract its audio and create a muted version.")

# --- File Upload ---
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Use a temporary directory to store files during processing
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "input_video.mp4")
        audio_path = os.path.join(temp_dir, "extracted_audio.mp3")
        video_path = os.path.join(temp_dir, "silent_video.mp4")

        # Save uploaded file to the temp directory
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("Processing... please wait.")

        try:
            # --- Processing Logic ---
            video = mp.VideoFileClip(input_path)
            
            # Extract Audio
            if video.audio:
                video.audio.write_audiofile(audio_path, logger=None)
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="🎵 Download Extracted Audio",
                        data=f,
                        file_name="extracted_audio.mp3",
                        mime="audio/mpeg"
                    )
            
            # Create Silent Video
            silent_video = video.without_audio()
            silent_video.write_videofile(video_path, codec="libx264", logger=None)
            
            with open(video_path, "rb") as f:
                st.download_button(
                    label="🔇 Download Silent Video",
                    data=f,
                    file_name="silent_video.mp4",
                    mime="video/mp4"
                )

            # Cleanup
            video.close()
            silent_video.close()
            st.success("Done!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.write("Please upload a video file to begin.")
