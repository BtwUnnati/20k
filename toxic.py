from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


EMAIL = "dilkhushghunawat86@gmail.com"
PASSWORD = "unnati@8690"

# 🧾 File jisme aapke codes hain (har line me ek code)
CODE_FILE = "word.txt"

# 📁 Output file jahan result save hoga
OUTPUT_FILE = "offer_status.txt"

# 🧰 Chrome setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def login_linkedin():
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    driver.find_element(By.ID, "username").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    time.sleep(5)
    print("✅ Logged in successfully!")

def read_codes():
    with open(CODE_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def check_offer(code):
    url = f"https://www.linkedin.com/premium/redeem/gift?_ed={code}"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    page_text = driver.page_source.lower()

    if "offer active" in page_text or "claim offer" in page_text:
        status = "ACTIVE"
    elif "already claimed" in page_text or "invalid" in page_text:
        status = "INVALID/CLAIMED"
    else:
        status = "UNKNOWN"

    print(f"{code} → {status}")

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{code}: {status}\n")

# 🚀 Main process
login_linkedin()
codes = read_codes()

print(f"🔍 {len(codes)} codes mil gaye, checking start ho rahi hai...\n")

for code in codes:
    check_offer(code)

driver.quit()
print(f"\n✅ Sab codes check ho gaye! Result '{OUTPUT_FILE}' me save ho gaya.")
