# bcv_scraper/scraper.py
import requests
from bs4 import BeautifulSoup
import locale
from decimal import Decimal

def get_rate():
    """
    Scrapes the official USD exchange rate from the BCV website.

    Returns:
        A dictionary containing the rate as a Decimal and the source URL,
        or None if an error occurs.
    """
    # Set locale to handle comma as decimal separator
    try:
        locale.setlocale(locale.LC_ALL, 'es_VE.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except locale.Error:
            # Fallback if specific locales are not available
            locale.setlocale(locale.LC_ALL, '')

    url_bcv = "https://www.bcv.org.ve/"
    
    try:
        response = requests.get(url_bcv, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to BCV: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # This selector is based on the current structure of the BCV website.
        # It might need to be updated if the website's HTML changes.
        rate_tag = soup.select_one('#dolar strong')

        if rate_tag:
            rate_str = rate_tag.get_text(strip=True)
            
            # Convert string to Decimal for precision
            rate_decimal = Decimal(locale.atof(rate_str))
            
            return {
                "usd_rate": rate_decimal,
                "source": url_bcv
            }
        else:
            print("Could not find the dollar rate element. The CSS selector may need to be revised.")
            return None
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None

