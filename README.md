# WikiFit - Streamlit Version

**WikiFit** is a health and fitness guide app that provides evidence-based fitness information, nutrition facts, workout plans, and home remedies. This version is built with Streamlit, a Python-based web application framework, and integrates real data from Wikipedia and other reliable sources.

---

## Features

- **Home Page**: Overview of the app with featured content and navigation.
- **Search**: Look up health and fitness terms using real Wikipedia data.
- **Nutrition Information**: Get details about nutritional content of different foods.
- **Exercise Comparison**: Compare different types of exercises for your needs.
- **Quiz**: Test your knowledge with interactive health and fitness trivia.
- **Workout Plans**: Access API-generated exercise routines based on your fitness goals.
- **Remedies**: Discover evidence-based treatments for common fitness-related issues.
- **Clean UI**: Simple, focused interface with multi-tabbed sections for easy navigation.

---

## Tech Stack

- **Streamlit** for the web application framework
- **Python** for backend logic and data processing
- **Wikipedia API** for real fitness and health data extraction
- **Requests** library for API interactions
- **Markdown** for rich text content

---

## Live Application

https://huggingface.co/spaces/KarthikGarlapati/wikifit

## Data Sources

WikiFit uses real API calls to extract data from:

1. **Wikipedia API** - For fitness articles, exercise information, and health data
2. **Structured Data** - Fallback data when API results aren't optimal
3. **Custom Analysis** - Processes raw data into structured, user-friendly information

---

## Getting Started

### Prerequisites

- Python 3.7+

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/wikifit.git
cd wikifit
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Verify setup (optional)
```bash
python check_setup.py
```

4. Run the application
```bash
streamlit run ai.py
```

The application will open in your default web browser at `http://localhost:8501`.

---

## Application Structure

```
wikifit/
├── ai.py                # Main Streamlit application file with full features
├── wikifit_basic.py     # Simplified version without AI dependencies
├── wikimedia.py         # Core module containing all Wikimedia API integrations
├── wiki.py              # Backward-compatibility adapter
├── DOCUMENTATION.md     # Detailed technical documentation
├── CONTRIBUTING.md      # Guidelines for contributing to the project
├── CHANGELOG.md         # History of project changes
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Usage

### Home Page
Visit the home page to see featured fitness content, daily tips, and quick navigation options.

### Search
Use the search functionality to find information on specific fitness topics, with results pulled directly from Wikipedia.

### Nutrition Information
Look up nutritional data for various foods and ingredients.

### Exercise Comparison
Compare different types of exercises to find what works best for your fitness goals.

### Quiz
Test your fitness knowledge with an interactive quiz and learn new facts.

### Workout Plans
Generate personalized workout plans based on your fitness goals, experience level, and available equipment.

### Remedies
Find evidence-based remedies and exercises for common fitness-related issues and ailments.

### Knowledge Center
Explore a wealth of knowledge from various Wikimedia projects, including Wikipedia, Wiktionary, Wikiquote, Wikibooks, and more.

### AI Health Q&A
Ask health questions and receive AI-powered answers (requires transformers library).

## Project Structure

### Key Files

- `ai.py` - Main Streamlit application with full features including AI capabilities
- `wikifit_basic.py` - Simplified version without AI dependencies
- `wikimedia.py` - Core module containing all Wikimedia API integrations
- `wiki.py` - Backward-compatibility adapter for existing code
- `requirements.txt` - Package dependencies

### Module Architecture

The application uses a modular architecture:

1. **wikimedia.py** - Core module with all Wikimedia API functions:
   - Handles all direct API calls to various Wikimedia services
   - Provides error handling and consistent response formatting
   - Centralizes logging and request management
   - Offers a unified search function across all Wikimedia sources

2. **ai.py and wikifit_basic.py** - Application entry points:
   - Import functions from wikimedia module
   - Apply caching for performance optimization
   - Handle UI/UX and user interaction
   - Provide feature-specific functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the Streamlit community
- Thanks to Hugging Face for providing free model hosting
- Gratitude to Wikimedia Foundation for their open APIs and information resources
