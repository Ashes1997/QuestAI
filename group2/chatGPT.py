
from openai import OpenAI






client = OpenAI()
def quest_create(prompt: str):
    print("Creating quest...")

    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a wizard who gives quests. You will be given a list of magical items and then state the quest required to obtain them. Keep the quest short, less than 200 words and add in where they will get each item in a single quest."}, #sets role of AI
        {"role": "user", "content": prompt} #gives list of items required for quest
        ]
    )

    prompt_return = completion.choices[0].message.content
    
    return prompt_return


def chatbot(quest, user_message, past_messages=[]):
    if not past_messages: #if first message in chat

        conversation = [
            {"role": "system", "content": "You are a helpful wizard answering questions about a specific quest you gave an adventurer."},
            {"role": "assistant", "content": quest} #just send quest if first message 
        ]
    else:
        conversation = past_messages
    format_message = "Quest is " + quest + " ...  My message is " + user_message #send quest plus first message 
    conversation.append({"role": "user", "content": format_message}) #add message to conversation
    
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation #send conversation to openai api so ai is aware of past messages
    )
    

    past_messages.append({"role": "user", "content": format_message})
    past_messages.append({"role": "assistant", "content": completion.choices[0].message.content}) #append response to conversation

    # print("Quest is" + quest)


    return completion.choices[0].message.content, past_messages






