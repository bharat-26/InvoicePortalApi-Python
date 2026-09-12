from fastapi import Request
from fastapi.responses import JSONResponse


async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request) # medium read

        # Every successful response should return 200
        if 200 <= response.status_code < 300:
            response.status_code = 200
        #200 only for all globally 
        elif 400 <= response.status_code < 500:
            response.status_code = 400


        return response

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Bad request error occurred."
            }
        )
#direct exception ke jagah bad request  error occured 
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Something went wrong while processing the request."
            }
        )