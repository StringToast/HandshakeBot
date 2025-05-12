from auth import get_driver, login
import time

def main():
    # 1) launch Chrome (visible so you can watch it)
    driver = get_driver(headless=False)

    try:
        # 2) go through your auth.py login flow
        login(driver)
        print("🎉 Logged in successfully!")

        # 3) keep it open so you can confirm
        time.sleep(5)

    finally:
        # 4) clean up
        driver.quit()
        print("✅ Browser closed, done.")

if __name__ == "__main__":
    main()