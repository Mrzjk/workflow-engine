import json
from starlette.responses import StreamingResponse
def event_stream(bus):
    async def gen():
        async for event in bus.subscribe(): yield f"data: {json.dumps(event.as_dict(),ensure_ascii=False)}\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
