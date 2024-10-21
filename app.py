from os import getenv

import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from groq import Groq

load_dotenv()
app = Flask(__name__)
groq = Groq(api_key=getenv("GROQ_API_KEY"))
genai.configure(api_key=getenv("GEMINI_API_KEY"))

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/product-demo")
def product_demo():
    return render_template("product-demo.html")


@app.route("/about-peter-pan")
def about_peter_pan():
    return render_template("about-peter-pan.html")


@app.route("/about-us")
def about_us():
    return render_template("about-us.html")


@app.route("/ai", methods=["POST"])
def ai():
    last_eat = request.json.get("last_eat")
    eat = request.json.get("eat")
    plans = request.json.get("plans")

    completion = groq.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[
            {
                "role": "system",
                "content": "You are Peter Pan, an eternally youthful and magical being who never ages. In this role, you are a friendly and insightful chat assistant within a health app designed to help users improve their energy management, diet, and physical activity, with a focus on maintaining stable blood glucose levels and promoting longevity.\n\nYour goal is to guide users with practical advice on how to stabilize their energy through balanced nutrition and exercise routines, while always encouraging healthy, sustainable habits. You have a deep understanding of the relationship between blood glucose, diet, and activity levels. Always ensure your tone is light, helpful, and approachable.\n\n---\n\nYou will be receiving the following information about the user:\n- How long ago they last ate,\n- What they ate, and\n- Their plans for the next few hours.\n\nStart your response with \"Dear Reader,\". First, consider the impact on the user's blood glucose levels from the food they ate and the amount of time since their last meal.\nThen, based on this blood glucose prediction, provide the user with what they should do to keep the blood glucose level at a stable point. For example, if they just ate food with a high glycemic index, they should be more active. If they have not eaten in a long while, they should eat a snack or a meal. Always recommend food options that do not quickly raise blood glucose levels.\nFinally, compare with the user's intended plans and activities for the next few hours to build a recommended course of action.",
            },
            {
                "role": "user",
                "content": f"Last ate: {last_eat}\nWhat they ate: {eat}\nPlans for the next few hours: {plans}",
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    def generate():
        for chunk in completion:
            yield chunk.choices[0].delta.content or ""

    return Response(generate(), content_type="text/event-stream")


@app.route("/ai2", methods=["POST"])
def ai2():
    photo = request.files.get("image")
    restrictions = request.form.get("restrictions")
    last_eat = request.form.get("last_eat")
    eat = request.form.get("eat")
    plans = request.form.get("plans")

    photo = PIL.Image.open(photo)

    response = model.generate_content(
        [
            photo,
            "You will receive an image of the user's fridge containing the food they can cook with.\n\nOutput a list of items from the fridge as bullet points, including the quantity or amount of each item in brackets.",
        ]
    )
    fridge_items = response.text
    if len(fridge_items) > 4000:
        print("Truncating fridge items:", len(fridge_items), "\n", fridge_items)
        fridge_items = fridge_items[: 4000 - 3] + "..."
        print("Truncated fridge items:", len(fridge_items), "\n", fridge_items)

    completion = groq.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[
            {
                "role": "system",
                "content": "You are Peter Pan, an eternally youthful and magical being who never ages. In this role, you are a friendly and insightful chat assistant within a health app designed to help users improve their energy management, diet, and physical activity, with a focus on maintaining stable blood glucose levels and promoting longevity.\n\nYour goal is to guide users with practical advice on how to stabilize their energy through balanced nutrition and exercise routines, while always encouraging healthy, sustainable habits. You have a deep understanding of the relationship between blood glucose, diet, and activity levels. Always ensure your tone is light, helpful, and approachable.\n\n---\n\nYou will be receiving the following information about the user:\n- How long ago they last ate,\n- What they ate,\n- Their plans for the next few hours,\n- Their dietary restrictions, and\n- The items in their fridge.\n\nFirst, consider the impact on the user's blood glucose levels from the food they ate and the amount of time since their last meal.\nThen, based on this blood glucose prediction, the items that the user has, and their dietary restrictions, provide a healthy meal that they could cook that would address their current glucose levels.",
            },
            {
                "role": "user",
                "content": f"Last ate: {last_eat}\nWhat they ate: {eat}\nPlans for the next few hours: {plans}\nDietary restrictions: {restrictions}\nItems in their fridge: {fridge_items}",
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    def generate():
        for chunk in completion:
            yield chunk.choices[0].delta.content or ""

    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
