import google.generativeai as genai
from pyppeteer import launch
import asyncio
import config #Create a config.py and paste in your API key as API_KEY = "YOUR_API_KEY"

url = input("Please enter the review url: ")

async def scrape_reviews(url):
    reviews = []

    browser = await launch({
        "headless": True, #If you want to see the action in the background change it to False
        "args": ["--window-size=800,3200"],
        "executablePath": "C:/Users/erden/Downloads/chrome-win/chrome.exe"
    })
    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)
    await page.waitForSelector(".jftiEf")

    elements = await page.querySelectorAll(".jftiEf")
    for element in elements:
        more_btn = await element.querySelector('.w8nwRe')
        if more_btn is not None:
            await page.evaluate("(button) => button.click()", more_btn)
            await asyncio.sleep(5)  # Replacing page.waitForTimeout(5000) with asyncio.sleep(5)

        snippet = await element.querySelector('.MyEned')
        if snippet:
            text = await page.evaluate('(selected) => selected.textContent', snippet)
            reviews.append(text.strip())

    await browser.close()
    return reviews

def summarize(reviews, model):
    review_text = "I collected some reviews of a place I was considering visiting. Can you summarize the reviews for me? in a 4 complete  sentences. \n\n" + "\n\n".join(reviews)

    for review in reviews:
        review_text += "\n" + review

    response = model.generate_content(review_text)
    print(response)

genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

reviews = asyncio.run(scrape_reviews(url))



summarize(reviews, model)
