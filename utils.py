import yaml
import random
import os
import streamlit as st

def get_sample_prompts():
    """Return sample prompts for initialization"""
    return [
        {
            'id': 1,
            'title': 'Professional Email Template',
            'prompt_text': 'Write a professional email to a client explaining a project delay and proposing a new timeline.',
            'tone': 'formal',
            'category': 'email',
            'completion': ''
        },
        {
            'id': 2,
            'title': 'Blog Post Introduction',
            'prompt_text': 'Create an engaging introduction for a blog post about sustainable living practices.',
            'tone': 'informal',
            'category': 'blog',
            'completion': ''
        },
        {
            'id': 3,
            'title': 'Creative Story Opening',
            'prompt_text': 'Write the opening paragraph of a mystery story set in a small coastal town.',
            'tone': 'creative',
            'category': 'story',
            'completion': ''
        },
        {
            'id': 4,
            'title': 'Technical Documentation',
            'prompt_text': 'Explain how to implement error handling in Python for beginners.',
            'tone': 'factual',
            'category': 'instruction',
            'completion': ''
        },
        {
            'id': 5,
            'title': 'Customer Support Response',
            'prompt_text': 'Respond to a customer complaint about a delayed shipment with empathy and a solution.',
            'tone': 'empathetic',
            'category': 'email',
            'completion': ''
        }
    ]

def load_prompts():
    """Load prompts from YAML file or return sample data if file doesn't exist"""
    try:
        if os.path.exists('prompts.yaml'):
            with open('prompts.yaml', 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data and isinstance(data, list):
                    return data
                else:
                    return get_sample_prompts()
        else:
            # Create file with sample data
            sample_data = get_sample_prompts()
            save_prompts(sample_data)
            return sample_data
    except Exception as e:
        st.error(f"Error loading prompts: {str(e)}")
        return get_sample_prompts()

def save_prompts(prompts_data):
    """Save prompts to YAML file"""
    try:
        with open('prompts.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(prompts_data, file, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        st.error(f"Error saving prompts: {str(e)}")
        return False

def get_static_completions():
    """Return a list of static completion responses for different tones"""
    return {
        'formal': [
            "Thank you for your inquiry. I would be pleased to provide you with the requested information in a comprehensive and detailed manner.",
            "Please find below a structured response that addresses your requirements with appropriate professional consideration.",
            "I appreciate the opportunity to assist you with this matter and shall endeavor to provide a thorough response."
        ],
        'informal': [
            "Hey there! Thanks for reaching out. I'd be happy to help you with this - let me break it down for you.",
            "No problem at all! Here's what I think about this topic, and I hope it helps you out.",
            "Great question! I've got some thoughts on this that might be useful for what you're working on."
        ],
        'empathetic': [
            "I understand this situation can be challenging, and I want to help you navigate through it with care and consideration.",
            "Your concerns are completely valid, and I'm here to support you through this process with understanding and patience.",
            "I recognize how important this is to you, and I'm committed to providing thoughtful guidance that addresses your specific needs."
        ],
        'factual': [
            "Based on available data and research, the following information provides an objective analysis of the topic.",
            "The evidence indicates several key points that are supported by reliable sources and documented findings.",
            "Research shows that this approach has demonstrated measurable results across multiple studies and applications."
        ],
        'creative': [
            "Imagine a world where possibilities unfold like origami flowers, each fold revealing new dimensions of potential and wonder.",
            "Picture this scenario unfolding like a story where every detail contributes to a larger narrative of innovation and discovery.",
            "Let's explore this concept through the lens of imagination, where conventional boundaries become launching pads for extraordinary ideas."
        ],
        'professional': [
            "In accordance with industry best practices, I recommend implementing a strategic approach that aligns with organizational objectives.",
            "Our analysis suggests that the following methodology would optimize outcomes while maintaining operational efficiency.",
            "Based on professional standards and proven methodologies, the recommended approach ensures both quality and measurable results."
        ],
        'casual': [
            "So here's the deal - this is pretty straightforward stuff once you get the hang of it.",
            "Honestly, this isn't as complicated as it might seem at first glance. Let me walk you through it.",
            "You know what? I think the best way to tackle this is to keep things simple and practical."
        ],
        'persuasive': [
            "Consider the significant advantages this approach offers, and how it can transform your current situation for the better.",
            "The compelling evidence suggests that taking action now will yield substantial benefits that far outweigh any initial investment.",
            "This opportunity presents a unique chance to achieve remarkable results that align perfectly with your goals and aspirations."
        ]
    }

def generate_completion(prompt_text, tone='formal'):
    """Generate a completion for the given prompt"""
    
    # Try to use OpenAI API if available
    try:
        import openai
        
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        if api_key and api_key.strip():
            client = openai.OpenAI(api_key=api_key)
            
            # Adjust system message based on tone
            tone_instructions = {
                'formal': 'Respond in a formal, professional manner with proper structure and respectful language.',
                'informal': 'Respond in a casual, friendly tone as if talking to a friend.',
                'empathetic': 'Respond with warmth, understanding, and emotional consideration.',
                'factual': 'Respond with objective, data-driven information and clear facts.',
                'creative': 'Respond with imagination, artistic flair, and innovative thinking.',
                'professional': 'Respond in a business-appropriate manner with industry expertise.',
                'casual': 'Respond in a relaxed, everyday conversational style.',
                'persuasive': 'Respond in a compelling, convincing manner that motivates action.'
            }
            
            system_message = f"You are a helpful writing assistant. {tone_instructions.get(tone, 'Respond appropriately to the request.')} Keep your response concise but complete."
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt_text}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
    except ImportError:
        pass  # OpenAI not installed, fall back to static responses
    except Exception as e:
        st.warning(f"OpenAI API error: {str(e)}. Using static response instead.")
    
    # Fall back to static responses
    static_completions = get_static_completions()
    tone_responses = static_completions.get(tone, static_completions['formal'])
    
    # Add some variation based on prompt content
    base_response = random.choice(tone_responses)
    
    # Add a relevant continuation based on prompt keywords
    if any(word in prompt_text.lower() for word in ['email', 'message', 'letter']):
        if tone == 'formal':
            continuation = " Please let me know if you require any additional information or clarification."
        elif tone == 'informal':
            continuation = " Feel free to reach out if you need anything else!"
        else:
            continuation = " I hope this helps with your communication needs."
    elif any(word in prompt_text.lower() for word in ['story', 'narrative', 'tale']):
        if tone == 'creative':
            continuation = " The narrative possibilities are endless, limited only by imagination itself."
        else:
            continuation = " This sets the foundation for an engaging narrative journey."
    elif any(word in prompt_text.lower() for word in ['instruction', 'guide', 'tutorial']):
        if tone == 'factual':
            continuation = " Following these steps systematically will ensure optimal results."
        else:
            continuation = " These guidelines provide a clear path forward for implementation."
    else:
        continuation = " This approach should effectively address your specific requirements."
    
    return base_response + continuation
