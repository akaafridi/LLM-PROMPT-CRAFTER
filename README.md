# ⚡ LLM-PROMPT-CRAFTER

A powerful Streamlit web application for crafting, managing, and experimenting with AI writing prompts across different categories and tones. Perfect for writers, content creators, and anyone looking to enhance their AI-assisted writing workflow.

## 🌟 Features

### 📁 Prompt Management
- **Browse & Filter**: Organize prompts by categories (email, blog, story, instruction)
- **Live Editing**: Real-time prompt editing with instant preview
- **Easy Navigation**: Sidebar-based prompt selection and filtering
- **Add/Delete**: Create new prompts or remove existing ones

### 🎨 Tone Customization
Choose from 8 different writing tones:
- **Formal**: Professional and structured communication
- **Informal**: Casual and friendly conversation
- **Empathetic**: Warm and understanding responses
- **Factual**: Data-driven and objective information
- **Creative**: Imaginative and artistic expression
- **Professional**: Business-appropriate expertise
- **Casual**: Relaxed everyday language
- **Persuasive**: Compelling and motivating content

### 🤖 AI-Powered Completions
- **OpenAI Integration**: Generate intelligent responses using GPT-4o
- **Tone-Aware**: Completions adapt to your selected tone
- **Fallback Responses**: Static responses when API is unavailable
- **Copy Function**: Easy copying of generated content

### 💾 Data Persistence
- **YAML Storage**: Clean, human-readable data format
- **Auto-Save**: Automatic data persistence
- **Import/Export**: Easy backup and sharing of prompt collections

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Streamlit
- OpenAI API key (optional but recommended)

### Installation
1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install streamlit openai pyyaml
   ```

### Running the Application
```bash
streamlit run main.py --server.port 5000
```

The app will be available at `http://localhost:5000`

## 🔧 Configuration

### OpenAI API Setup (Optional)
To enable AI-powered completions:

1. Get an API key from [OpenAI Platform](https://platform.openai.com/)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Restart the application

**Note**: Without an API key, the app will use static response templates that still provide valuable writing examples.

## 📖 How to Use

### 1. Browse Prompts
- Use the sidebar to filter prompts by category
- Select any prompt to view and edit it
- Current settings are displayed in the right panel

### 2. Edit Prompts
- Modify the title, category, tone, and prompt text
- Changes are saved automatically to your session
- Click "Save Changes" to persist to file

### 3. Generate Completions
- Select your desired tone
- Click "Generate Completion" to create AI responses
- View the generated content in the completion area
- Copy the result for use in your projects

### 4. Manage Your Collection
- Add new prompts with the "Add New Prompt" button
- Delete unwanted prompts with the delete button
- All changes are automatically saved to `prompts.yaml`

## 📁 File Structure

```
llm-prompt-crafter/
├── main.py              # Main Streamlit application
├── utils.py             # Helper functions for data management
├── prompts.yaml         # Prompt data storage
├── .streamlit/
│   └── config.toml     # Streamlit configuration
└── README.md           # This file
```

## 🎯 Use Cases

### Content Creators
- Generate blog post introductions
- Create social media content templates
- Develop email marketing campaigns

### Writers
- Explore different narrative styles
- Practice various writing tones
- Generate story prompts and openings

### Professionals
- Craft business communications
- Develop training materials
- Create customer service templates

### Educators
- Teaching writing techniques
- Demonstrating tone and style variations
- Creating writing exercises

## 🛠️ Customization

### Adding New Categories
Edit the categories list in `main.py`:
```python
categories = ['email', 'blog', 'story', 'instruction', 'your_new_category']
```

### Adding New Tones
Extend the tones list and add corresponding static responses in `utils.py`:
```python
tones = ['formal', 'informal', 'empathetic', 'factual', 'creative', 'professional', 'casual', 'persuasive', 'your_new_tone']
```

### Custom Static Responses
Modify the `get_static_completions()` function in `utils.py` to add your own response templates.

## 💡 Tips for Best Results

1. **Be Specific**: Detailed prompts generate better completions
2. **Match Tone**: Choose the tone that fits your intended audience
3. **Iterate**: Try different tones for the same prompt to see variations
4. **Save Favorites**: Keep successful prompts for future reference
5. **Experiment**: Use the app to explore new writing styles and approaches

## 🔒 Data Privacy

- All data is stored locally in `prompts.yaml`
- OpenAI API calls follow OpenAI's privacy policy
- No data is shared with third parties beyond OpenAI (when API is used)

## 🆘 Troubleshooting

### Common Issues

**App won't start**
- Check Python version (3.11+ required)
- Verify all dependencies are installed
- Ensure port 5000 is available

**OpenAI API errors**
- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure stable internet connection

**Prompts not saving**
- Check file permissions in the project directory
- Ensure `prompts.yaml` is not locked by another application

### Getting Help
If you encounter issues:
1. Check the console output for error messages
2. Verify your environment setup
3. Try restarting the application

## 🚀 Future Enhancements

Potential features for future versions:
- Multiple AI provider support (Anthropic, Google, etc.)
- Prompt templates marketplace
- Advanced filtering and search
- Export to various formats (PDF, Word, etc.)
- Collaborative editing features
- Version history for prompts

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Writing!** 🎉

Create engaging content with the power of AI-assisted prompt engineering. Whether you're crafting professional emails, creative stories, or educational content, this tool helps you explore the full spectrum of writing possibilities.