
from openai import OpenAI






client = OpenAI()
def quest_create(prompt: str):
    print("Creating quest...")

    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a wizard who gives quests. You will be given a list of magical items and then state the quest required to obtain them. Keep the quest short, less than 200 words and add in where they will get each item in a single quest."},
        {"role": "user", "content": prompt}
        ]
    )

    prompt_return = completion.choices[0].message.content
    
    return prompt_return






