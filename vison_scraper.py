from openai import OpenAI
import subprocess
import base64
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenAI()
model.timeout = 30

def images_b64():
    images_b64 = []
    for image_path in os.listdir("."):
        if image_path.startswith("screenshot_") and image_path.endswith(".jpg"):
            with open(image_path, "rb") as image_file:
                images_b64.append(base64.b64encode(image_file.read()).decode())
            os.remove(image_path)  # Clean up after encoding
    return images_b64

def url2screenshot(url):
    print(f"Crawling {url}")

    # Remove existing screenshots
    for existing_image in os.listdir("."):
        if existing_image.startswith("screenshot_") and existing_image.endswith(".jpg"):
            os.remove(existing_image)

    result = subprocess.run(
        ["node", "screenshot.js", url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("ERROR in screenshot capture")
        return []

    return images_b64()


def visionExtract(b64_image, prompt):
    response = model.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction",
            }
        ] + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
            }
        ],
        max_tokens=1024,
    )

    message = response.choices[0].message
    message_text = message.content

    if "ANSWER_NOT_FOUND" in message_text:
        print("ERROR: Answer not found")
        return "I was unable to find the answer on that website. Please pick another one"
    else:
        print(f"GPT: {message_text}")
        return message_text

def visionCrawl(url, prompt):
    b64_image = url2screenshot(url)

    print("Image captured")
    
    if b64_image == "Failed to scrape the website":
        return "I was unable to crawl that site. Please pick a different one."
    else:
        return visionExtract(b64_image, prompt)

response = visionCrawl("https://docs.anthropic.com/claude/docs/tool-use", "teach me how to use the Tool Use")
print(response)