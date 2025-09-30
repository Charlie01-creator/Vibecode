import os
from flask import Flask, render_template, request
from openai import OpenAI

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image_url = None

    if request.method == "POST":
        vibe = request.form["vibe"]
        topic = request.form["topic"]

        # --- Generate caption ---
        text_prompt = f"Write a {vibe} style social media post about: {topic}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            max_tokens=120
        )
        result = response.choices[0].message.content

        # --- Generate image ---
        image_prompt = f"{vibe} aesthetic illustration for: {topic}, digital art, vibrant, social media style"
        image = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="512x512"
        )
        image_url = image.data[0].url

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
