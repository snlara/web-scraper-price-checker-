
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Scraping the Data
def get_apmex_prices():
    url = "https://www.apmex.com/category/25260/1-oz-silver-rounds"
    # User-Agent header is necessary to avoid being blocked as a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate product items (based on current APMEX structure)
    products = soup.find_all('div', class_='product-container', limit=5)
    
    price_list = []
    for product in products:
        name = product.find('div', class_='item-title').text.strip()
        price = product.find('span', class_='price').text.strip()
        price_list.append(f"{name}: {price}")
        
    return "\n".join(price_list)

# 2. Sending the Email
def send_email(content):
    sender_email = "your_email@gmail.com"  # Your email
    receiver_email = "snlara@gmail.com"
    password = "your_app_password"         # Use a Google App Password, NOT your regular password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "APMEX 1 oz Silver Prices - Top 5"
    
    message.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Run the process
if __name__ == "__main__":
    prices = get_apmex_prices()
    if prices:
        print("Prices found:\n", prices)
        send_email(prices)
    else:
        print("No prices found. Check the website's HTML structure.")