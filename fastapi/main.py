import uvicorn
import os

async def app(scope, receive, send):
    assert scope['type'] == 'http'

    mode = 'DEBUG'
    if ('MODE' in os.environ.keys()):
        mode = os.environ['MODE']

    body = (f'Hello, world (mode:{mode})\n').encode()

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': body,
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")

