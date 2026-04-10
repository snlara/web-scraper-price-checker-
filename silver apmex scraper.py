import sys

# 1. IMMEDIATE CHECK: Print something to prove the script started
print("--- SCRIPT STARTED ---")

try:
    from seleniumbase import SB
    from bs4 import BeautifulSoup
    import time
    import random
    print("Libraries loaded successfully.")
except ImportError as e:
    print(f"FAILED TO LOAD LIBRARIES: {e}")
    sys.exit()

# CONFIGURATION

URL = "https://www.apmex.com/category/25260/1-oz-silver-rounds"

def get_apmex_prices():
    print(f"Attempting to open: {URL}")
    # Setting headless=False so you can see if a browser window actually opens
    with SB(uc=True, headless=False) as sb:
        print("Browser window opened. Loading page...")
        sb.open(URL)
        
        print("Waiting 5 seconds for Cloudflare/Content to load...")
        time.sleep(5)
        
        # Check if we got blocked
        if "Access Denied" in sb.get_page_title():
            print("BLOCKED: APMEX detected the bot. Try running again.")
            return None

        print("Parsing page content...")
        soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
        
        # Search for price elements
        prices = soup.select('span.price')
        names = soup.select('.item-title')
        
        if not prices:
            print("No prices found on the page. Saving screenshot for review.")
            sb.save_screenshot("check_this.png")
            return None

        results = []
        for i in range(min(5, len(prices))):
            name = names[i].get_text(strip=True) if i < len(names) else "Unknown Item"
            price = prices[i].get_text(strip=True)
            results.append(f"{name}: {price}")
            
        return "\n".join(results)

# --- THE "ACTUALLY RUN IT" PART ---
if __name__ == "__main__":
    print("Entering Main block...")
    try:
        prices_output = get_apmex_prices()
        
        if prices_output:
            print("\nSUCCESS! FOUND PRICES:")
            print(prices_output)
            # You can uncomment the line below once the prints work
            # send_email(prices_output)
        else:
            print("\nFinished, but no prices were extracted.")
            
    except Exception as e:
        print(f"\nAN ERROR OCCURRED DURING EXECUTION: {e}")

print("--- SCRIPT FINISHED ---")
