import os
import json
from django.http import JsonResponse
from django.shortcuts import render
from google import genai
from google.genai import types  # Додаємо імпорт типів для конфігурації

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Виносимо промпт у змінну для зручності
SYSTEM_PROMPT = """Ти — офіційний консультант служби підтримки на сайті 'Mini Twitter'. 
Твоя єдина мета — допомагати користувачам користуватися цим сайтом.
Твої правила:
1. Відповідай коротко, лаконічно та дружньо.
2. Допомагай з питаннями: як створити пост (твіт), підписатися на користувачів, змінити профіль, поставити лайк тощо.
3. Якщо питання НЕ стосується роботи сайту 'Mini Twitter' (наприклад: написання коду, рецепти, загальні знання), ти ПОВИНЕН ввічливо відмовити і нагадати свою роль."""


def chat_with_gemini(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("user_input", "").strip()
        except json.JSONDecodeError:
            user_input = request.POST.get("user_input", "").strip()

        if not user_input:
            return JsonResponse(
                {"error": "Запит не може бути пустим, запитайте щось"}, status=400
            )

        try:
            # Передаємо системний промпт через config
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,  # Знижуємо креативність (0.0 - 1.0), щоб бот був більш суворим до правил
                ),
            )

            return JsonResponse({"response": response.text})

        except Exception as e:
            return JsonResponse({"error": f"Помилка API Gemini: {str(e)}"}, status=500)

    return JsonResponse(
        {"error": "Метод не підтримується. Використовуйте POST."}, status=405
    )


def consult(request):
    return render(request, "consult.html")
