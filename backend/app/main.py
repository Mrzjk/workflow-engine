from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.core.logging import configure_logging
from app.api import workflows,runs,tools,models,health,auth
configure_logging(); app=FastAPI(title="Workflow Studio")
for r in [auth.router,workflows.router,runs.router,tools.router,models.router,health.router]: app.include_router(r)
@app.exception_handler(ValueError)
async def value_error(_:Request,e:ValueError): return JSONResponse(status_code=422,content={"code":"WORKFLOW_VALIDATION_ERROR","message":str(e),"details":[]})
