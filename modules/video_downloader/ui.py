"""
Video Downloader UI
Streamlit interface for downloading videos
"""
import streamlit as st
from modules.video_downloader.downloader import VideoDownloader
from i18n.loader import get_text


class VideoDownloaderUI:
    """Video Downloader user interface"""
    
    def __init__(self, config, license_tier: str):
        self.config = config
        self.license_tier = license_tier
        self.downloader = VideoDownloader()
    
    def render_ui(self):
        """Render main UI"""
        st.title("🎥 " + get_text("video_downloader"))
        
        if self.license_tier == "FREE":
            st.warning("This feature requires STARTER tier or higher")
            if st.button("⬆️ Upgrade Now"):
                st.session_state.current_page = "tier_management"
                st.rerun()
            return
        
        video_url = st.text_input(
            get_text("paste_url"),
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬇️ Download Video", type="primary"):
                if video_url:
                    with st.spinner("Downloading..."):
                        result = self.downloader.download_video(video_url)
                        if result:
                            st.success("Download complete!")
                        else:
                            st.error("Download failed")
        
        with col2:
            if st.button("🎵 Download Audio Only"):
                if video_url:
                    with st.spinner("Downloading audio..."):
                        result = self.downloader.download_audio_only(video_url)
                        if result:
                            st.success("Audio download complete!")
                        else:
                            st.error("Download failed")
    
    def cleanup(self):
        pass
