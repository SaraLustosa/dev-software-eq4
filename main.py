from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import List
import model as m
import uvicorn
import os
import sys

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")


class Settings(BaseSettings):
    OPENAI_KEY: str = ''

settings=Settings()

app = FastAPI()

origins = [
    "http://localhost:5173", 
    os.getenv("FRONTEND_URL", "https://production.com") 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = m.user_list
openai = m.OpenaiInteface(useDummy=not settings.OPENAI_KEY,openai_key=settings.OPENAI_KEY)
print(settings.OPENAI_KEY)

@app.get("/")
async def root():
    return {"message": "Hello World"}

messagesyet=[]

@app.post("/addMessage")
@app.post("/addData")
async def addData(msg: m.Message):
    """Recebe uma mensagem nova, determina o usuario, pega a resposta 
    de uma IA e adiciona no historico de mensagens
    e retorna o historico de mensagens"""
    #preencher aqui
    if (msg.username not in m.user_list):
        user = m.User(msg.username)
        m.user_list[msg.username] = user
    else:
        user = m.user_list[msg.username]
    user.addMessage(msg)
    reply = await openai.reply(user)
    user.addMessage(m.Message(username="assistant", content=reply ))
    messages =user.getMessageHistory()
    return messages

@app.post("/getMessages", response_model=List[m.GptMessage])
async def getMessages(username:str) -> List[m.GptMessage]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""

    if username not in m.user_list.keys():
        m.user_list[username] = m.User(username=username)

    return m.user_list[username].message_history

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
