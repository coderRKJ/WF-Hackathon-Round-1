import asyncio
import heapq
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
from ujson import dumps
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from send_emails import send_bulk_emails

app = FastAPI()

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response

class SendEmailGroup(BaseModel):
    group_name: str
    subject: str
    content: str
    priority: int | None = 3
    delay: int | None = 0

class EmailGroupList(BaseModel):
    group_name: str
    group_email_list: list[str]

email_groups = {"Test_group":["test_email_1@email.com", "test_email_2@email.com"]}

email_groups_pending = []

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@app.get('/groups')
def get_groups():
    global email_groups
    return list(email_groups.keys())

@app.get('/group/{group_name}')
def get_groups(group_name: str):
    global email_groups
    return email_groups[group_name]

@app.post('/group')
def get_groups(emailGroupList: EmailGroupList):
    global email_groups
    email_groups[emailGroupList.group_name] = emailGroupList.group_email_list
    return {"status": f"Added {emailGroupList.group_name}"}

@app.post('/send_email_group')
def add_email(sendEmailGroup: SendEmailGroup):
    global email_groups_pending
    group = sendEmailGroup.group_name
    email_data = {
        "subject": sendEmailGroup.subject,
        "content": sendEmailGroup.content
    }
    send_time = sendEmailGroup.delay + time.time()
    priorty = sendEmailGroup.priority # TODO: Check if between 1 and 3
    heapq.heappush(email_groups_pending, (send_time,priorty,group,email_data))
    return {"status": "Email Queued" if sendEmailGroup.delay>0 else "Email Sent"}

@app.get('/stream')
async def message_stream(request: Request):
    global email_groups_pending
    def check_if_schedule_passed():
        # Add logic here to check for new emails to be sent
        global email_groups_pending
        return len(email_groups_pending) and email_groups_pending[0][0] < time.time()

    async def event_generator():
        global email_groups_pending
        global email_groups
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if check_if_schedule_passed():
                _, _, group, email_data = heapq.heappop(email_groups_pending)
                email_list = email_groups[group]
                send_bulk_emails(email_list, email_data["subject"], email_data["content"])
                yield {
                        "event": "message",
                        "id": "message_id",
                        "retry": RETRY_TIMEOUT,
                        "data": dumps(email_data)
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

app.mount('/', SPAStaticFiles(directory='./', html=True), name='vue-spa')