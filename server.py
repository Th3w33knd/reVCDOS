from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

VCSKY_BASE_URL = "https://cdn.dos.zone/vcsky/"
BR_BASE_URL = "https://br.cdn.dos.zone/vcsky/"

def request_to_url(request: Request, path: str, base_url = VCSKY_BASE_URL):
    query_string = str(request.url.query) if request.url.query else ""
    url = f"{base_url}{path}"
    if query_string:
        url = f"{url}?{query_string}"
    return url

async def _proxy_request(request: Request, url: str):
    client = httpx.AsyncClient()
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    req = client.build_request(request.method, url, headers=headers, content=request.stream())
    r = await client.send(req, stream=True)
    return StreamingResponse(r.aiter_raw(), status_code=r.status_code, headers=r.headers, background=client.aclose)

@app.api_route("/vcsky/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def vc_sky_proxy(request: Request, path: str):
    return await _proxy_request(request, request_to_url(request, path))

@app.api_route("/vcbr/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def vc_br_proxy(request: Request, path: str):
    return await _proxy_request(request, request_to_url(request, path, BR_BASE_URL))

# local use
# app.mount("/vcsky", StaticFiles(directory="vcsky"), name="vcsky") # audio/, data/, models/, anim/
# app.mount("/vcbr", StaticFiles(directory="vcbr"), name="vcbr") # vc-sky-en-v6.data.br, vc-sky-en-v6.wasm.br, vc-sky-ru-v6.data.br, vc-sky-ru-v6.wasm.br

@app.get("/")
async def read_index():
    return FileResponse("dist/index.html")

app.mount("/", StaticFiles(directory="dist"), name="root")

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
