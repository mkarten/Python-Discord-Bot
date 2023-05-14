import openai
import logging

class message(object):
    def __init__(self, author, content):
        self.role = author
        self.content = content

class chat(object):
    def __init__(self):
        self.tokenCost = 0
        self.messages : list[message] =[]
        self.lastMessage : message = message("", "")
    
    def __str__(self):
        return str(self.messages)
    
    def askGpt(self, input : str):
        self.messages.append(message("user", input))
        self.lastMessage = self.messages[-1]
        messageData = []
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[x.__dict__ for x in self.messages]
        )
        tokenUsage = "promt token : " + str(response["usage"]["prompt_tokens"]) + " , completion token : " + str(response["usage"]["completion_tokens"]) + " , total token : " + str(response["usage"]["total_tokens"])
        msg = response["choices"][0]["message"]
        self.messages.append(message(msg["role"], msg["content"]))
        self.lastMessage = self.messages[-1]
        cost = round(int(response["usage"]["total_tokens"])*(0.002/1000),7)
        return self.lastMessage.content,cost

def registerApi(apiKey : str, organization : str):
    openai.api_key = apiKey
    openai.organization = organization
    print("Successfully registered OpenAI API key and organization")