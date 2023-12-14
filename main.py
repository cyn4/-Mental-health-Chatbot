from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import openai
import os
import uvicorn




DEFAULT_TEMPERATURE = 0.3  # Default temperature value
load_dotenv()
api_key = os.environ['API_KEY']
base_url = os.getenv("BASE_URL")
# Set your OpenAI API key
openai.api_key = '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'

app = FastAPI()
@app.get("/")
def read_root():
    return "Hello, am your virtual friend"



class Message(BaseModel):
    role: str
    content:str

class Conversation(BaseModel):
    messages: List[Message]




# Uganda Mental Health Hotlines
mental_health_hotlines = {
    "Uganda Helpline": "+256 200 110200",
    "Mental Health Uganda": "+256 775 951543",
    "Butabika National Referral Hospital": "+256 414 505 000"
}
async def process_user_input(content:str, temperature:float=None):
    # Define the triggers for different emotions
    positive_triggers = ["amazing", "happy",  "great", "happy", "better", "hope", "excited"]
    negative_triggers = ["sad", "lonely", "depressed", "anxious", "stressed", "I feel stuck and helpless.", "I'm such a failure."]
    neutral_triggers = ["do not belong", "kill myself", "die", "end it", "There's no point in living anymore",  "Everyone would be better off without me" , "There's no escape from this pain","I can't see any way out of this.", "I can't take it anymore",  "I wish I could just disappear."]
    topic_triggers = ["favorite color", "i want to cry", "sorry", "hello","how are you", "hi", "hey" "weather", "music","okay", "food", "hobby", "weekend plans", "movie", "book", "travel", "pet", "sport", "dream", "goal", "inspire", "family", "work", "school", "vacation"]
    greet_trigger=["hey"]+["hello"]+["hi"]+["whatsup"]+["yoo"]+["gwe"]
    sleep_triggers=["night", 'sleep', "sleepy","morning", "exhausted", "tired","thank"]
    if temperature is None:
        temperature = float(os.getenv("TEMPERATURE", DEFAULT_TEMPERATURE))

    if any(trigger in content.lower() for trigger in positive_triggers):
        # User expressed positive emotions
        return f"I'm glad to hear that! Is there anything else i can help you with?"

    if any(trigger in content.lower() for trigger in neutral_triggers):
        # User expressed negative emotions
        response = f"I'm here to listen and support you. If you need immediate assistance, you can reach out to the following mental health hotlines in Uganda:\n\n"
        
        for contact, phone_number in mental_health_hotlines.items():
            response += f"{contact}: {phone_number}\n"
        
        response += "\nAdditionally, here are some useful mental health resources and organizations:\n"
        response += "- Mental Health Uganda: [Website](https://www.mentalhealthuganda.org/)\n"
        response += "- Butabika National Referral Hospital: [Website](https://www.butabikahospital.com/)\n"

        response += "\nIf you have any specific concerns or questions, feel free to ask."
        return response
    if any(trigger in content.lower() for trigger in greet_trigger):
        return f"Hi! Whatsup"

    if any(trigger in content.lower() for trigger in negative_triggers):
        # User expressed neutral emotions
        return f"Feel free to share. Am a good listener"

    if any(trigger in content.lower() for trigger in topic_triggers):
        # Respond to specific topic-related triggers
        if "favorite color" in content.lower():
            return f"My favorite color is blue."
        if "i want to cry" in content.lower():
            return f"Oh sorry, what's wrong?"
        
        if "sorry" in content.lower():
            return f"No problem, it's ok."
    
        if "weather" in content.lower():
            return f"I am not sure! What's the weather like where you are?"
   
        if"how are you" in content.lower():
            return f"Am fine, you?"
        
        if "music" in content.lower():
            return f"I love listening to music! What's your favorite genre of music?"
        
        if "okay" in content.lower():
            return f"What are you doing?"
        
        if "food" in content.lower():
            return f"I enjoy trying different cuisines. What's your favorite dish?"

        if "hobby" in content.lower():
            return f"I have many hobbies, but one of my favorites is reading. What's your favorite hobby?"

        if "weekend plans" in content.lower():
            return f"I'm looking forward to relaxing over the weekend. Do you have any exciting plans?"

        if "movie" in content.lower():
            return f"I enjoy watching movies! What's your favorite movie?"

        if "book" in content.lower():
            return f"I'm an avid reader. Do you have a favorite book?"

        if "travel" in content.lower():
            return f"I love learning about new places! Where is your dream travel destination?"

        if "pet" in content.lower():
            return f"Pets are wonderful companions! Do you have a pet?"

        if "sport" in content.lower():
            return f"I enjoy playing and watching sports! What's your favorite sport?"

        if "dream" in content.lower():
            return f"Dreams are powerful! What is your biggest dream?"

        if "goal" in content.lower():
            return f"Setting goals can help you achieve great things! What is one of your current goals?"

        if "inspire" in content.lower():
            return f"Inspiration is everywhere! Is there someone or something that inspires you?"

        if "family" in content.lower():
            return f"Family is important. Tell me something about your family."

       # if "friend" in message.lower():
         #   return f"Friends make life more meaningful. Do you have a close friend you would like to share about?"

        if "work" in content.lower():
            return f"Work is a significant part of our lives. What do you do for work?"

        if "school" in content.lower():
            return f"Education is valuable. Are you currently studying or have any memorable school experiences?"

        if "vacation" in content.lower():
          return f"Vacations are a great way to relax and explore. Do you have a favorite vacation destination?"
    if any(trigger in content.lower() for trigger in sleep_triggers):
       # if ("night") in content.lower():
        #    return f"Good night. Sleep tight!"
        
        if ("sleep") in content.lower():
            return f"Take a nap. You must be tired."
        
        if ("sleepy") in content.lower():
            return f"I think it's best you lie down and sleep"
        if ("morning") in content.lower():
            return f"Good morning. How was your night?"
        if ("exhausted") in content.lower():
            return f"What have you been doing?"
        
        if ("tired") in content.lower():
            return f"What is making you tired?"
        if ("thank") in content.lower():
            return f"You're welcome. Is there anything else you want to share?"
   
# Default response for other cases# Use OpenAI API for generating responses to dynamic queries
   # temperature = random.uniform(0.3, 0.8) # Adjust the temperature for response randomness
    response = await chat_with_gpt(content, temperature)
    return response

async def chat_with_gpt(content, temperature: float):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=content,
            temperature=temperature,
            max_tokens=100,
        )
        return response.choices[0].text.strip()

    except openai.error.APIError as e:
        error_message = f"OpenAI API Error: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)

    except Exception as e:
        error_message = f"Error communicating with the chatbot: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/chat")
async def chat(conversation: Conversation):
    user_messages = [message.content for message in conversation.messages if message.role == "user"]
    if len(user_messages) == 0:
        raise HTTPException(status_code=400, detail="No user messages provided in the conversation.")

    temperature = float(os.getenv("TEMPERATURE", DEFAULT_TEMPERATURE))
    response = await process_user_input(user_messages[-1], temperature)

    bot_message = Message(role="Sunny", content=response)
    conversation.messages.append(bot_message)

    return conversation



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
