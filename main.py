import streamlit as st
import yaml
import random
import os
from utils import load_prompts, save_prompts, generate_completion, get_sample_prompts

# Configure page
st.set_page_config(
    page_title="LLM-PROMPT-CRAFTER",
    page_icon="⚡",
    layout="wide"
)

# Initialize session state
if 'prompts_data' not in st.session_state:
    st.session_state.prompts_data = load_prompts()

if 'current_prompt_id' not in st.session_state:
    st.session_state.current_prompt_id = None

if 'edited_prompt' not in st.session_state:
    st.session_state.edited_prompt = ""

if 'last_completion' not in st.session_state:
    st.session_state.last_completion = ""

# Main title
st.title("⚡ LLM-PROMPT-CRAFTER")
st.markdown("Craft, manage, and experiment with AI writing prompts across different categories and tones.")

# Sidebar for filters and navigation
st.sidebar.header("📁 Navigation & Filters")

# Get unique categories and tones from data
categories = sorted(list(set([prompt.get('category', 'general') for prompt in st.session_state.prompts_data])))
tones = ['formal', 'informal', 'empathetic', 'factual', 'creative', 'professional', 'casual', 'persuasive']

# Category filter
selected_category = st.sidebar.selectbox(
    "Select Category:",
    options=['All'] + categories,
    index=0
)

# Tone selector
selected_tone = st.sidebar.selectbox(
    "Select Tone:",
    options=tones,
    index=0
)

# Filter prompts based on selection
filtered_prompts = st.session_state.prompts_data
if selected_category != 'All':
    filtered_prompts = [p for p in filtered_prompts if p.get('category', 'general') == selected_category]

# Display filtered prompts list
st.sidebar.subheader("Available Prompts")
if filtered_prompts:
    prompt_options = {}
    for i, prompt in enumerate(filtered_prompts):
        title = prompt.get('title', f"Prompt {prompt.get('id', i+1)}")
        category = prompt.get('category', 'general')
        display_name = f"{title} ({category})"
        prompt_options[display_name] = prompt
    
    selected_prompt_name = st.sidebar.selectbox(
        "Choose a prompt:",
        options=list(prompt_options.keys()),
        index=0 if prompt_options else None
    )
    
    if selected_prompt_name and selected_prompt_name in prompt_options:
        selected_prompt = prompt_options[selected_prompt_name]
        st.session_state.current_prompt_id = selected_prompt.get('id')
        if st.session_state.edited_prompt == "" or st.session_state.current_prompt_id != selected_prompt.get('id'):
            st.session_state.edited_prompt = selected_prompt.get('prompt_text', '')
else:
    st.sidebar.info("No prompts found for the selected category.")
    selected_prompt = None

# Add new prompt button
if st.sidebar.button("➕ Add New Prompt"):
    new_id = max([p.get('id', 0) for p in st.session_state.prompts_data], default=0) + 1
    new_prompt = {
        'id': new_id,
        'title': f'New Prompt {new_id}',
        'prompt_text': 'Enter your prompt here...',
        'tone': selected_tone,
        'category': selected_category if selected_category != 'All' else 'general',
        'completion': ''
    }
    st.session_state.prompts_data.append(new_prompt)
    st.session_state.current_prompt_id = new_id
    st.session_state.edited_prompt = new_prompt['prompt_text']
    st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Prompt Editor")
    
    if selected_prompt or st.session_state.current_prompt_id:
        # Find current prompt
        current_prompt = None
        if st.session_state.current_prompt_id:
            current_prompt = next((p for p in st.session_state.prompts_data if p.get('id') == st.session_state.current_prompt_id), None)
        
        if not current_prompt and selected_prompt:
            current_prompt = selected_prompt
        
        if current_prompt:
            # Title editor
            new_title = st.text_input(
                "Prompt Title:",
                value=current_prompt.get('title', ''),
                key="title_input"
            )
            
            # Category and tone selectors
            col_cat, col_tone = st.columns(2)
            with col_cat:
                new_category = st.selectbox(
                    "Category:",
                    options=categories,
                    index=categories.index(current_prompt.get('category', 'general')) if current_prompt.get('category', 'general') in categories else 0,
                    key="category_input"
                )
            
            with col_tone:
                new_tone = st.selectbox(
                    "Tone:",
                    options=tones,
                    index=tones.index(current_prompt.get('tone', 'formal')) if current_prompt.get('tone', 'formal') in tones else 0,
                    key="tone_input"
                )
            
            # Prompt text editor
            edited_text = st.text_area(
                "Prompt Text:",
                value=st.session_state.edited_prompt,
                height=200,
                key="prompt_editor"
            )
            st.session_state.edited_prompt = edited_text
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🤖 Generate Completion", type="primary"):
                    with st.spinner("Generating completion..."):
                        completion = generate_completion(st.session_state.edited_prompt, new_tone)
                        st.session_state.last_completion = completion
                        # Update the prompt in session state
                        for i, p in enumerate(st.session_state.prompts_data):
                            if p.get('id') == st.session_state.current_prompt_id:
                                st.session_state.prompts_data[i]['completion'] = completion
                                break
            
            with col_btn2:
                if st.button("💾 Save Changes"):
                    # Update the prompt data
                    for i, p in enumerate(st.session_state.prompts_data):
                        if p.get('id') == st.session_state.current_prompt_id:
                            st.session_state.prompts_data[i].update({
                                'title': new_title,
                                'prompt_text': st.session_state.edited_prompt,
                                'category': new_category,
                                'tone': new_tone
                            })
                            break
                    
                    # Save to file
                    if save_prompts(st.session_state.prompts_data):
                        st.success("✅ Prompt saved successfully!")
                    else:
                        st.error("❌ Failed to save prompt.")
            
            with col_btn3:
                if st.button("🗑️ Delete Prompt"):
                    st.session_state.prompts_data = [p for p in st.session_state.prompts_data if p.get('id') != st.session_state.current_prompt_id]
                    st.session_state.current_prompt_id = None
                    st.session_state.edited_prompt = ""
                    save_prompts(st.session_state.prompts_data)
                    st.success("🗑️ Prompt deleted successfully!")
                    st.rerun()
    else:
        st.info("👈 Select a prompt from the sidebar or add a new one to get started.")

with col2:
    st.subheader("🎯 Generated Completion")
    
    if st.session_state.last_completion or (selected_prompt and selected_prompt.get('completion')):
        completion_text = st.session_state.last_completion or selected_prompt.get('completion', '')
        
        st.markdown("**Generated Response:**")
        st.text_area(
            "Completion:",
            value=completion_text,
            height=200,
            disabled=True,
            key="completion_display"
        )
        
        # Copy button
        if st.button("📋 Copy to Clipboard"):
            st.code(completion_text, language="text")
            st.info("💡 Select and copy the text above.")
    else:
        st.info("🤖 Click 'Generate Completion' to see AI-generated content here.")
    
    # Display current settings
    st.markdown("---")
    st.subheader("⚙️ Current Settings")
    if selected_prompt or st.session_state.current_prompt_id:
        current_prompt = None
        if st.session_state.current_prompt_id:
            current_prompt = next((p for p in st.session_state.prompts_data if p.get('id') == st.session_state.current_prompt_id), None)
        if not current_prompt and selected_prompt:
            current_prompt = selected_prompt
            
        if current_prompt:
            st.write(f"**Category:** {current_prompt.get('category', 'general')}")
            st.write(f"**Tone:** {current_prompt.get('tone', 'formal')}")
            st.write(f"**ID:** {current_prompt.get('id', 'N/A')}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>💡 <strong>Tip:</strong> Use different tones to generate varied writing styles for your prompts!</p>
    </div>
    """,
    unsafe_allow_html=True
)
