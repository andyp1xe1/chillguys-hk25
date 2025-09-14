import streamlit as st
import api

# Configure page
st.set_page_config(
    page_title="Chat App",
    page_icon="💬",
    layout="centered"
)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for confirmation workflow
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False

if "anonymized_response" not in st.session_state:
    st.session_state.anonymized_response = ""

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("display_type") == "dual":
            # Extract both versions from stored content
            content = message["content"]
            if "**Deanonymized Version:**" in content:
                parts = content.split("**Deanonymized Version:**")
                anon_part = parts[0].replace("**Anonymized Version:**", "").strip()
                deanon_part = parts[1].strip()
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**Anonymized Version**")
                    st.write(anon_part)
                with col2:
                    st.markdown("**Deanonymized Version**")
                    st.write(deanon_part)
            else:
                st.write(content)
        else:
            st.write(message["content"])

# Show confirm button if awaiting confirmation
if st.session_state.awaiting_confirmation:
    if st.button("Confirm"):
        st.session_state.awaiting_confirmation = False
        
        # Show gemini status
        with st.chat_message("assistant"):
            gemini_status = st.empty()
            gemini_status.write("Sending to gemini...")
            
            try:
                gemini_response = api.gemini(st.session_state.anonymized_response)
                
                # Create deanonymized version
                deanonymized_response = api.deanonymize(gemini_response)
                
                # Display both versions side-by-side
                gemini_status.empty()
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**Anonymized Version**")
                    st.write(gemini_response)
                
                with col2:
                    st.markdown("**Deanonymized Version**")
                    st.write(deanonymized_response)
                
                # Add both versions to messages
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"**Anonymized Version:**\n{gemini_response}\n\n**Deanonymized Version:**\n{deanonymized_response}",
                    "display_type": "dual"
                })
                
            except Exception as e:
                gemini_status.write(f"Error: {str(e)}")
        
        st.rerun()  # Rerun after processing

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Show anonymizing status
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.write("Anonymizing...")
        
        # Call anonymize API
        try:
            anonymized = api.anonymize(prompt)
            status_placeholder.write(anonymized)
            
            # Store for confirmation
            st.session_state.anonymized_response = anonymized
            st.session_state.awaiting_confirmation = True
            
            # Add to messages
            st.session_state.messages.append({"role": "assistant", "content": anonymized})
            
            # Trigger rerun to show confirm button
            st.rerun()
            
        except Exception as e:
            status_placeholder.write(f"Error: {str(e)}")

