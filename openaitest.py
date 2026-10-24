
from openai import OpenAI
from config import apikey

# Connect to the OpenAI API
client = OpenAI(api_key=apikey)

try:
    print("Testing OpenAI API connection...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Write a short professional resignation email to my boss."
            }
        ],
        temperature=0.7,
        max_tokens=256
    )

    # Display the generated response
    print("\nOpenAI API Response:\n")
    print(response.choices[0].message.content)

    print("\nAPI test completed successfully!")

except Exception as e:
    print("\nAPI test failed.")
    print("Error:", e)
