# WikiFit Changelog

All notable changes to the WikiFit project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-04

### Added
- New `wikimedia.py` module that centralizes all Wikimedia API integrations
- Unified search function to query across all Wikimedia platforms at once
- New `wiki.py` adapter for backward compatibility with existing code
- Improved documentation in README about the modular architecture
- This CHANGELOG file to track project changes

### Changed
- Refactored `ai.py` to use the new `wikimedia.py` module instead of direct API calls
- Updated `wikifit_basic.py` to use the `wikimedia.py` module
- Enhanced error handling and logging for all Wikimedia API requests
- Improved code organization with proper modularization

### Fixed
- Better error reporting for failed API requests
- Consistent API response formatting across all Wikimedia services

## [1.0.0] - 2025-06-15

### Added
- Initial release of WikiFit application
- Full version with AI features (`ai.py`)
- Basic version without AI dependencies (`wikifit_basic.py`)
- Support for multiple Wikimedia sources:
  - Wikipedia
  - Wiktionary
  - Wikiquote
  - Wikibooks
  - Wikimedia Commons
  - Wikisource
  - Wikiversity
  - Wikispecies
  - Wikidata
- Health features:
  - Daily health tips with seasonal recommendations
  - BMI calculator
  - Workout plans
  - Health quiz
  - Progress tracker
- AI-powered health Q&A using Hugging Face transformers
- Comprehensive documentation in README