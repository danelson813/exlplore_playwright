from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/")
        heading = page.query_selector("//h1/a")
        # print(heading.inner_text())

        login = page.query_selector('[href = "/login"]')
        login.click()
        username = page.query_selector('[id="username"]')
        username.type('user')

        password = page.query_selector('[id="password"]')
        password.type("text")

        submit_btn = page.query_selector('//input[@class="btn btn-primary"]')
        submit_btn.click()

        quotes = page.query_selector_all("[class='quote']")
        data = []
        for quote in quotes:
            result = {}
            content = quote.query_selector('.text').inner_text()
            author = quote.query_selector('.author').inner_text()
            result = {
                'Quote': content,
                "Author": author,
            }
            data.append(result)
        # page.wait_for_timeout(5000)

        browser.close()

        return data


if __name__ == "__main__":
    main()
    df = pd.DataFrame(main())
    df.to_csv('Data.csv', index=False)
