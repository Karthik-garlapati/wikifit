# WikiFit Documentation

## Overview

WikiFit is a comprehensive health and fitness application built with Streamlit that leverages Wikimedia APIs to provide rich health-related information. The application features both a standard version with AI capabilities (`ai.py`) and a lightweight version (`wikifit_basic.py`) for environments with limited resources.

## System Architecture

### Core Components

```
┌─────────────────┐     ┌───────────────┐     ┌────────────────┐
│  wikifit_basic  │     │      ai.py    │     │    wiki.py     │
│      .py        │     │ (Main App)    │     │  (Adapter)     │
└────────┬────────┘     └───────┬───────┘     └────────┬───────┘
         │                      │                      │
         └──────────────────────▼──────────────────────┘
                               │
                     ┌─────────▼──────────┐
                     │    wikimedia.py    │
                     │  (Core Module)     │
                     └─────────┬──────────┘
                               │
                     ┌─────────▼──────────┐
                     │  Wikimedia APIs    │
                     └────────────────────┘
```

### Module Breakdown

1. **wikimedia.py**: Core module that handles all API integrations.
   - Centralized error handling and logging
   - Consistent response formatting
   - API abstraction layer

2. **ai.py**: Main application file with full features.
   - Streamlit UI/UX implementation
   - AI-powered health Q&A capabilities
   - Performance optimization with caching
   - Complete feature set

3. **wikifit_basic.py**: Lightweight alternative.
   - Streamlit UI with reduced features
   - No AI dependencies
   - Simpler interface
   - Faster startup

4. **wiki.py**: Backward compatibility adapter.
   - Re-exports functions from wikimedia.py
   - Ensures compatibility with existing code

## API Integration

WikiFit integrates with the following Wikimedia APIs:

| API | Purpose | Function |
|-----|---------|----------|
| Wikipedia | General health information | `get_wikipedia_summary()` |
| Wiktionary | Health terminology definitions | `get_wiktionary_definition()` |
| Wikiquote | Health and wellness quotes | `get_wikiquote_quotes()` |
| Wikibooks | Educational health content | `get_wikibooks_content()` |
| Wikimedia Commons | Health-related images | `get_wikimedia_commons_images()` |
| Wikisource | Historical health texts | `get_wikisource_texts()` |
| Wikiversity | Educational resources | `get_wikiversity_resources()` |
| Wikispecies | Biological information | `get_wikispecies_info()` |
| Wikidata | Structured health data | `get_wikidata_health_info()` |

### Unified Search

The `search_all_wikimedia()` function provides a unified search experience across all Wikimedia platforms:

```python
results = wikimedia.search_all_wikimedia("vitamin d")
```

Returns a dictionary with results from all platforms.

## Features

### Health Information

- **Daily Tips**: Provides contextual health tips adjusted for the current season.
- **Health Search**: Searches Wikipedia for health-related information.
- **Knowledge Center**: Centralized search across all Wikimedia platforms.
- **Home Remedies**: Traditional health remedies from various sources.
- **Did You Know**: Interesting health facts.

### Fitness Tools

- **Workout Plans**: Pre-defined workout routines by type.
- **BMI Calculator**: Calculates BMI with support for multiple measurement units.
- **Progress Tracker**: Tracks workout completion and quiz scores.

### AI Features

- **Health Q&A**: Ask health questions with AI-powered answers.
- **Context-Aware**: Different contexts for general health, nutrition, and fitness.
- **Disclaimer**: Clearly marks responses as not replacing professional advice.

## Usage Examples

### Basic Search

```python
# Get health information about a topic
info = wikimedia.get_wikipedia_summary("exercise")
```

### Unified Search

```python
# Search across all Wikimedia platforms
all_results = wikimedia.search_all_wikimedia("protein")

# Access specific platform results
wikipedia_info = all_results["wikipedia"]
wikidata_info = all_results["wikidata"]
```

### Getting Images

```python
# Get health-related images (returns a list of image data)
images = wikimedia.get_wikimedia_commons_images("meditation", limit=3)

# Display the first image
st.image(images[0]["url"], caption=images[0]["title"])
```

## Caching

WikiFit uses Streamlit's caching to optimize performance:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_wikipedia_summary(term):
    return wikimedia.get_wikipedia_summary(term)
```

## Error Handling

All API calls include comprehensive error handling:

1. **HTTP Errors**: Proper handling of different status codes.
2. **Network Issues**: Catch and log connection problems.
3. **Response Formatting**: Consistent response formatting regardless of API.
4. **User Feedback**: Clear error messages for end-users.

## Performance Considerations

- **Caching**: All API responses are cached for 1 hour (configurable).
- **Parallel Requests**: Unified search sequentially queries APIs to prevent rate limiting.
- **Response Size**: Image queries are limited by default to prevent memory issues.

## Development Guidelines

### Adding New Wikimedia Sources

To add a new Wikimedia source:

1. Add the API integration function to `wikimedia.py`
2. Include proper error handling and logging
3. Update the `search_all_wikimedia()` function to include the new source
4. Add wrapper functions with caching in `ai.py` and `wikifit_basic.py`

### Testing

Testing should include:

1. API response validation
2. Error handling verification
3. Performance testing with cached vs. non-cached responses
4. UI rendering tests with various response types

## Future Enhancements

Potential areas for improvement include:

- Adding more Wikimedia sources as they become available
- Implementing more sophisticated AI models for health advice
- Creating a more advanced progress tracking system
- Adding export functionality for health data
- Developing personalized recommendation algorithms

---

For more information, refer to the [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md) files.
