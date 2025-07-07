"""
WikiFit - Wikimedia API Integration Module

This module provides functions to interact with various Wikimedia APIs
to retrieve health and fitness information.
"""

import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache durations (in seconds)
CACHE_TTL = 3600  # 1 hour


def get_wikipedia_summary(term):
    """
    Get a summary of a topic from Wikipedia.
    
    Args:
        term: The search term/topic
        
    Returns:
        str: Summary text or error message
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            if not extract:
                # Check if we have an alternative like disambiguation
                if data.get("type") == "disambiguation":
                    return f"'{term}' refers to multiple topics. Please try a more specific search term."
                return "No summary found. This topic might not have an article on Wikipedia yet."
            return extract
        elif response.status_code == 404:
            return f"The topic '{term}' was not found on Wikipedia. Please check spelling or try another term."
        else:
            logging.error(f"Wikipedia API error: {response.status_code} for term '{term}'")
            return f"Error retrieving information: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikipedia request error for '{term}': {str(e)}")
        return "Connection error. Please check your internet connection and try again later."


def get_wiktionary_definition(term):
    """Get word definitions from Wiktionary"""
    try:
        url = "https://en.wiktionary.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exsectionformat": "plain",
            "exsentences": 5,
            "explaintext": True
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            # Extract the first page content (there should only be one)
            for page_id in pages:
                if "extract" in pages[page_id]:
                    return pages[page_id]["extract"]
                
            return "No definition found."
        else:
            return f"Error retrieving definition: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wiktionary request error: {str(e)}")
        return "Connection error. Please try again later."


def get_wikiquote_quotes(term):
    """Get quotes related to a topic from Wikiquote"""
    try:
        url = "https://en.wikiquote.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exsentences": 5,
            "explaintext": True
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            # Extract the first page content (there should only be one)
            for page_id in pages:
                if int(page_id) > 0 and "extract" in pages[page_id]:  # Skip missing pages
                    content = pages[page_id]["extract"].strip()
                    if content:
                        return content
                
            return "No quotes found for this topic."
        else:
            return f"Error retrieving quotes: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikiquote request error: {str(e)}")
        return "Connection error. Please try again later."


def get_wikibooks_content(term):
    """Get educational content from Wikibooks"""
    try:
        url = "https://en.wikibooks.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exsentences": 10,
            "explaintext": True
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            # Extract the first page content
            for page_id in pages:
                if int(page_id) > 0 and "extract" in pages[page_id]:
                    return pages[page_id]["extract"]
                
            return "No Wikibooks content found for this topic."
        else:
            return f"Error retrieving content: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikibooks request error: {str(e)}")
        return "Connection error. Please try again later."


def get_wikimedia_commons_images(term, limit=5):
    """Get relevant images from Wikimedia Commons"""
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{term} haswbstatement:P180={term}",  # Search for images with the term as subject
            "srnamespace": 6,  # File namespace
            "srlimit": limit
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            
            image_titles = []
            for result in search_results:
                if "title" in result:
                    image_titles.append(result["title"])
                    
            # If we found images, get their URLs
            image_data = []
            if image_titles:
                file_titles = "|".join(image_titles)
                image_params = {
                    "action": "query",
                    "format": "json",
                    "titles": file_titles,
                    "prop": "imageinfo",
                    "iiprop": "url|extmetadata",
                    "iiurlwidth": 300  # Thumbnail width
                }
                img_response = requests.get(url, params=image_params, timeout=10)
                if img_response.status_code == 200:
                    img_data = img_response.json()
                    pages = img_data.get("query", {}).get("pages", {})
                    
                    for page_id in pages:
                        page = pages[page_id]
                        if "imageinfo" in page and page["imageinfo"]:
                            info = page["imageinfo"][0]
                            title = page.get("title", "").replace("File:", "")
                            thumb_url = info.get("thumburl", "")
                            description = info.get("extmetadata", {}).get("ImageDescription", {}).get("value", "")
                            
                            # Clean HTML from description
                            description = description.replace("<p>", "").replace("</p>", "")
                            
                            if thumb_url:
                                image_data.append({
                                    "title": title,
                                    "url": thumb_url,
                                    "description": description
                                })
                    
            return image_data
        else:
            logging.error(f"Wikimedia Commons API error: {response.status_code} for term '{term}'")
            return []
    except requests.RequestException as e:
        logging.error(f"Wikimedia Commons request error: {str(e)}")
        return []


def get_wikisource_texts(term):
    """Get health-related texts from Wikisource"""
    try:
        url = "https://en.wikisource.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": term,
            "srlimit": 3
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            
            text_data = []
            for result in search_results:
                title = result.get("title", "")
                snippet = result.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                text_data.append({
                    "title": title,
                    "snippet": snippet
                })
                    
            return text_data
        else:
            logging.error(f"Wikisource API error: {response.status_code} for term '{term}'")
            return []
    except requests.RequestException as e:
        logging.error(f"Wikisource request error: {str(e)}")
        return []


def get_wikiversity_resources(term):
    """Get educational resources from Wikiversity"""
    try:
        url = "https://en.wikiversity.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exsentences": 5,
            "explaintext": True
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            # Extract the first page content
            for page_id in pages:
                if int(page_id) > 0 and "extract" in pages[page_id]:
                    return pages[page_id]["extract"]
                
            return "No Wikiversity resources found for this topic."
        else:
            return f"Error retrieving resources: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikiversity request error: {str(e)}")
        return "Connection error. Please try again later."


def get_wikispecies_info(species_name):
    """Get species information from Wikispecies"""
    try:
        url = "https://species.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": species_name,
            "prop": "extracts",
            "explaintext": True
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            # Extract the first page content
            for page_id in pages:
                if int(page_id) > 0 and "extract" in pages[page_id]:
                    return pages[page_id]["extract"]
                
            return "No species information found."
        else:
            return f"Error retrieving species information: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikispecies request error: {str(e)}")
        return "Connection error. Please try again later."


def get_wikidata_health_info(term):
    """Get structured health data from Wikidata"""
    try:
        # First, find the Wikidata ID for the term
        url = "https://www.wikidata.org/w/api.php"
        params = {
            "action": "wbsearchentities",
            "format": "json",
            "search": term,
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("search", [])
            
            if not search_results:
                return "No Wikidata information found for this term."
                
            # Get the first result's ID
            entity_id = search_results[0].get("id")
            
            # Now get the entity data
            entity_params = {
                "action": "wbgetentities",
                "format": "json",
                "ids": entity_id,
                "languages": "en"
            }
            entity_response = requests.get(url, params=entity_params, timeout=10)
            
            if entity_response.status_code == 200:
                entity_data = entity_response.json()
                entities = entity_data.get("entities", {})
                
                if entity_id in entities:
                    entity = entities[entity_id]
                    
                    # Extract label and description
                    label = entity.get("labels", {}).get("en", {}).get("value", "No label")
                    description = entity.get("descriptions", {}).get("en", {}).get("value", "No description")
                    
                    # Extract some claims/properties
                    claims = entity.get("claims", {})
                    properties = {}
                    
                    # Common health-related properties
                    property_map = {
                        "P2175": "medical condition treated",
                        "P2176": "drug used for treatment",
                        "P780": "symptoms",
                        "P1050": "medical condition",
                        "P1995": "health specialty"
                    }
                    
                    for prop_id, prop_name in property_map.items():
                        if prop_id in claims:
                            values = []
                            for claim in claims[prop_id]:
                                mainsnak = claim.get("mainsnak", {})
                                if mainsnak.get("datatype") == "wikibase-item" and "datavalue" in mainsnak:
                                    value_id = mainsnak["datavalue"]["value"]["id"]
                                    values.append(value_id)
                            
                            if values:
                                properties[prop_name] = values
                    
                    return {
                        "label": label,
                        "description": description,
                        "properties": properties
                    }
            
            return "No detailed Wikidata information available."
        else:
            logging.error(f"Wikidata API error: {response.status_code} for term '{term}'")
            return f"Error retrieving Wikidata: HTTP {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Wikidata request error: {str(e)}")
        return "Connection error. Please try again later."


# Add a unified search function to search across all Wikimedia platforms
def search_all_wikimedia(term):
    """
    Search for a term across all Wikimedia platforms.
    
    Args:
        term: Search term
        
    Returns:
        dict: Results from all Wikimedia sources
    """
    # Normalize the term
    search_term = term.strip().replace(" ", "_")
    
    # Create a results dictionary
    results = {
        "wikipedia": None,
        "wiktionary": None,
        "wikiquote": None,
        "wikibooks": None,
        "commons": None,
        "wikisource": None,
        "wikiversity": None,
        "wikispecies": None,
        "wikidata": None
    }
    
    # Get results from each platform
    results["wikipedia"] = get_wikipedia_summary(search_term)
    results["wiktionary"] = get_wiktionary_definition(search_term)
    results["wikiquote"] = get_wikiquote_quotes(search_term)
    results["wikibooks"] = get_wikibooks_content(search_term)
    results["commons"] = get_wikimedia_commons_images(search_term)
    results["wikisource"] = get_wikisource_texts(search_term)
    results["wikiversity"] = get_wikiversity_resources(search_term)
    results["wikispecies"] = get_wikispecies_info(search_term)
    results["wikidata"] = get_wikidata_health_info(search_term)
    
    return results