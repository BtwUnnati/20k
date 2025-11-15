import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===============================
# CONFIG
# ===============================
COOKIES_FILE = "cookies.txt"       # li_at cookie
WORDS_FILE = "word.txt"            # codes list
VALID_OUTPUT = "valid_codes.txt"   # valid results
THREADS = 4                        # safe parallel threads
TIMEOUT = 12                       # request timeout
# ===============================


def load_cookie():
    if not os.path.exists(COOKIES_FILE):
        raise SystemExit(f"❌ Cookie file not found: {COOKIES_FILE}")

    cookie = open(COOKIES_FILE, "r", encoding="utf-8").read().strip()
    if not cookie:
        raise SystemExit("❌ cookies.txt is empty!")
    return cookie


def create_session(li_at_cookie):
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    })
    s.cookies.set("li_at", li_at_cookie, domain=".linkedin.com")
    return s


def check_code(session, code):
    url = "https://www.linkedin.com/premium/redeem/gift"
    params = {"_ed": code}

    try:
        r = session.get(url, params=params, timeout=TIMEOUT)
        text = r.text.lower()
    except Exception as e:
        return code, "error"

    # ----- Detection Logic -----
    if "already been redeemed" in text:
        return code, "used"

    if "offer unavailable" in text:
        return code, "invalid"

    if "claim" in text or "activate" in text or "redeem" in text:
        return code, "valid"

    return code, "unknown"


def main():
    li_at_cookie = load_cookie()
    session = create_session(li_at_cookie)

    if not os.path.exists(WORDS_FILE):
        raise SystemExit(f"❌ Code file not found: {WORDS_FILE}")

    codes = [x.strip() for x in open(WORDS_FILE, "r", encoding="utf-8") if x.strip()]
    print(f"\n🔥 TOTAL CODES LOADED: {len(codes)}\n")

    valid_found = 0

    print("⚡ Checking codes fast with multi-threads...\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        tasks = {executor.submit(check_code, session, code): code for code in codes}

        for future in as_completed(tasks):
            code, result = future.result()

            if result == "valid":
                valid_found += 1
                print(f"🎉 OFFER ACTIVE → {code}")

                with open(VALID_OUTPUT, "a", encoding="utf-8") as f:
                    f.write(code + "\n")

            elif result == "invalid":
                print(f"❌ INVALID → {code}")

            elif result == "used":
                print(f"⚠ USED → {code}")

            else:
                print(f"❓ UNKNOWN → {code}")

    print("\n=============================")
    print(f"✔ TOTAL VALID OFFERS FOUND: {valid_found}")
    print(f"📁 SAVED IN: {VALID_OUTPUT}")
    print("=============================\n")


if __name__ == "__main__":
    main()
