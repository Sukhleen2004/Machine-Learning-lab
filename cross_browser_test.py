import asyncio
import os
from playwright.async_api import async_playwright

async def test_cross_browser():
    os.makedirs("screenshots", exist_ok=True)

    async with async_playwright() as p:

        browsers = [
            ("Chromium", p.chromium),
            ("Firefox", p.firefox),
            ("WebKit", p.webkit)
        ]

        for name, browser_type in browsers:
            browser = None
            page = None

            try:
                print(f"\nTesting on {name} browser...")

                browser = await browser_type.launch(
                    headless=False,
                    slow_mo=1000
                )

                page = await browser.new_page(
                    viewport={"width": 1366, "height": 768}
                )

                # Open login page
                await page.goto(
                    "https://www.saucedemo.com/",
                    wait_until="domcontentloaded",
                    timeout=60000
                )
                await page.wait_for_timeout(3000)

                await page.screenshot(
                    path=f"screenshots/{name}_01_login_page.png"
                )

                # Enter username
                await page.locator("#user-name").fill("standard_user")
                await page.wait_for_timeout(2000)

                # Enter password
                await page.locator("#password").fill("secret_sauce")
                await page.wait_for_timeout(2000)

                await page.screenshot(
                    path=f"screenshots/{name}_02_credentials.png"
                )

                # Click login
                await page.locator("#login-button").click()
                await page.wait_for_timeout(5000)

                # Verify login
                heading = page.locator(".title")

                if (
                    await heading.count() > 0
                    and await heading.inner_text() == "Products"
                ):
                    print(f"{name}: Login test - PASS")
                else:
                    print(f"{name}: Login test - FAIL")
                    print("Current URL:", page.url)

                await page.screenshot(
                    path=f"screenshots/{name}_03_login_result.png"
                )

                # Keep browser open to view the result
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"{name}: Test error - {e}")

                if page:
                    try:
                        await page.screenshot(
                            path=f"screenshots/{name}_error.png"
                        )
                    except Exception:
                        pass

            finally:
                if browser:
                    await browser.close()

    print("\nTesting completed. Check the screenshots folder.")

asyncio.run(test_cross_browser())