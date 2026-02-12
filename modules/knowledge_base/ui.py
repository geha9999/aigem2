"""
Knowledge Base UI
Streamlit interface for note-taking
"""
import streamlit as st
from modules.knowledge_base.database import NotesDatabase
from i18n.loader import get_text

class KnowledgeBaseUI:
    """Knowledge Base user interface"""
    
    def __init__(self, config, license_tier: str):
        self.config = config
        self.license_tier = license_tier
        self.db = NotesDatabase()
        
        # Initialize session state
        if 'current_note_id' not in st.session_state:
            st.session_state.current_note_id = None
        if 'show_note_editor' not in st.session_state:
            st.session_state.show_note_editor = False
    
    def render_ui(self):
        """Render main UI"""
        st.title("📚 " + get_text("knowledge_base"))
        
        # Top action bar
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_query = st.text_input(
                get_text("search"),
                placeholder="Search notes...",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("🔍 " + get_text("search"), use_container_width=True):
                if search_query:
                    st.session_state.search_results = self.db.search_notes(search_query)
        
        with col3:
            if st.button("➕ " + get_text("new_note"), use_container_width=True):
                st.session_state.show_note_editor = True
                st.session_state.current_note_id = None
                st.rerun()
        
        st.divider()
        
        # Show note editor or note list
        if st.session_state.show_note_editor:
            self._render_note_editor()
        else:
            self._render_note_list()
    
    def _render_note_list(self):
        """Render list of notes""" 
        
        # Check if showing search results
        if hasattr(st.session_state, 'search_results'):
            notes = st.session_state.search_results
            st.info(f"Found {len(notes)} note(s)")
        else:
            notes = self.db.get_all_notes()
        
        if not notes:
            st.info(get_text("notes_empty"))
            return
        
        # Display notes as cards
        for note in notes:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {note['title']}")
                    
                    # Preview content (first 200 chars)
                    preview = note['content'][:200] + "..." if len(note['content']) > 200 else note['content']
                    st.markdown(preview)
                    
                    # Tags
                    if note['tags']:
                        tags_html = " ".join([f"<span style='background:#334155; padding:2px 8px; border-radius:4px; font-size:12px; margin-right:4px;'>#{tag}</span>" for tag in note['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                    
                    # Metadata
                    st.caption(f"Updated: {note['updated_at']}")
                
                with col2:
                    if st.button("✏️", key=f"edit_{note['id']}"):
                        st.session_state.current_note_id = note['id']
                        st.session_state.show_note_editor = True
                        st.rerun()
                    
                    if st.button("🗑️", key=f"delete_{note['id']}"):
                        self.db.delete_note(note['id'])
                        st.success("Note deleted!")
                        st.rerun()
                
                st.divider()
    
    def _render_note_editor(self):
        """Render note editor""" 
        
        # Load existing note if editing
        note_data = None
        if st.session_state.current_note_id:
            note_data = self.db.get_note(st.session_state.current_note_id)
        
        # Editor form
        with st.form("note_editor"):
            title = st.text_input(
                "Title",
                value=note_data['title'] if note_data else "",
                placeholder="Enter note title..."
            )
            
            content = st.text_area(
                "Content",
                value=note_data['content'] if note_data else "",
                height=400,
                placeholder="Write your note here... (Markdown supported)"
            )
            
            tags_input = st.text_input(
                "Tags",
                value=", ".join(note_data['tags']) if note_data else "",
                placeholder="tag1, tag2, tag3"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                submitted = st.form_submit_button(get_text("save"), type="primary", use_container_width=True)
            
            with col2:
                cancelled = st.form_submit_button(get_text("cancel"), use_container_width=True)
            
            if submitted:
                if title:
                    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                    
                    if st.session_state.current_note_id:
                        # Update existing note
                        self.db.update_note(
                            st.session_state.current_note_id,
                            title=title,
                            content=content,
                            tags=tags
                        )
                        st.success("Note updated!")
                    else:
                        # Create new note
                        note_id = self.db.create_note(title, content, tags=tags)
                        st.success(f"Note created! (ID: {note_id})")
                    
                    st.session_state.show_note_editor = False
                    st.session_state.current_note_id = None
                    st.rerun()
                else:
                    st.error("Title is required!")
            
            if cancelled:
                st.session_state.show_note_editor = False
                st.session_state.current_note_id = None
                st.rerun()
    
    def cleanup(self):
        """Cleanup resources"""
        pass
