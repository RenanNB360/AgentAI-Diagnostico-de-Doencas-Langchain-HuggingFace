from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import pandas as pd
from add_ons.agent import app_prompt, result_disease, set_disease

router = APIRouter()

class Connection:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = Connection()

async def init_chatbot():
    return await app_prompt()

async def diagnosis_chatbot(columns, responses, df):
    return await result_disease(columns, responses, df)

async def disease_result():
    return await set_disease()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    chain_initial, chain = await init_chatbot()

    df = pd.read_csv('data/archive/Disease_symptom_and_patient_profile_dataset.csv')
    columns = [column for column in df.columns[1:len(df.columns)-1]]
    responses = []

    await manager.connect(websocket)

    try:

        result_initial = chain_initial.invoke(input="")
        question_initial = result_initial.split('\n')[7]
        await websocket.send_text(question_initial)

        for symptom in columns:

            result = chain.invoke({'context': symptom})
            question = result.split('\n')[7]
            await websocket.send_text(question)

            user_message = await websocket.receive_text()
            responses.append(user_message)
        
        result_explain, disease = await diagnosis_chatbot(columns= columns, responses= responses, df= df)
        await set_disease(disease)
        await websocket.send_text(f"{result_explain}")

        await websocket.close()
    
    except WebSocketDisconnect:
        await manager.disconnect(websocket)