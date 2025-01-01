from groq import Groq

client = Groq(
    api_key="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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)