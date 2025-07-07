"""
WikiFit - Wiki API Helper Functions

This file serves as a backward-compatible adapter between the old direct API calls
and the new wikimedia module structure. It imports and re-exports all the relevant
functions from the wikimedia module.
"""

from wikimedia import (
    get_wikipedia_summary,
    get_wiktionary_definition,
    get_wikiquote_quotes,
    get_wikibooks_content,
    get_wikimedia_commons_images,
    get_wikisource_texts,
    get_wikiversity_resources,
    get_wikispecies_info,
    get_wikidata_health_info,
    search_all_wikimedia
)
# Re-export all functions (for backward compatibility)
__all__ = [
    'get_wikipedia_summary',
    'get_wiktionary_definition',
    'get_wikiquote_quotes',
    'get_wikibooks_content',
    'get_wikimedia_commons_images',
    'get_wikisource_texts',
    'get_wikiversity_resources',
    'get_wikispecies_info',
    'get_wikidata_health_info',
    'search_all_wikimedia'
]
