import os
import argparse
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
import additions.saves as saves
from additions.auth import BasicAuthMiddleware
from additions.cache import proxy_and_cache, get_local_file

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--custom_saves", action="store_true")
parser.add_argument("--login", type=str)
parser.add_argument("--password", type=str)
parser.add_argument("--vcsky_local", action="store_true", help="Serve vcsky from local directory instead of proxy")
parser.add_argument("--vcbr_local", action="store_true", help="Serve vcbr from local directory instead of proxy")
parser.add_argument("--vcsky_url", type=str, default="https://cdn.dos.zone/vcsky/", help="Custom vcsky proxy URL")
parser.add_argument("--vcbr_url", type=str, default="https://br.cdn.dos.zone/vcsky/", help="Custom vcbr proxy URL")
parser.add_argument("--vcsky_cache", action="store_true", help="Cache vcsky files locally. If files are not found in the local directory, they will be downloaded from the specified URL and saved to the local directory.")
parser.add_argument("--vcbr_cache", action="store_true", help="Cache vcbr files locally. If files are not found in the local directory, they will be downloaded from the specified URL and saved to the local directory.")
args = parser.parse_args()

app = FastAPI()

if args.login and args.password:
    app.add_middleware(BasicAuthMiddleware, username=args.login, password=args.password)

if args.custom_saves:
    app.include_router(saves.router)

VCSKY_BASE_URL = args.vcsky_url
VCBR_BASE_URL = args.vcbr_url

def request_to_url(request: Request, path: str, base_url: str):
    query_string = str(request.url.query) if request.url.query else ""
    url = f"{base_url}{path}"
    if query_string:
        url = f"{url}?{query_string}"
    return url

# vcsky routes - either local or proxy
@app.api_route("/vcsky/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def vc_sky_proxy(request: Request, path: str):
    local_path = os.path.join("vcsky", path)
    if args.vcsky_local:
        if response := get_local_file(local_path, request):
            return response
        raise HTTPException(status_code=404, detail="File not found")
    url = request_to_url(request, path, VCSKY_BASE_URL)
    if args.vcsky_cache:
        return await proxy_and_cache(request, url, local_path)
    return await proxy_and_cache(request, url, disable_cache=True)

# vcbr routes - either local or proxy
@app.api_route("/vcbr/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def vc_br_proxy(request: Request, path: str):
    local_path = os.path.join("vcbr", path)
    if args.vcbr_local:
        if response := get_local_file(local_path, request):
            return response
        raise HTTPException(status_code=404, detail="File not found")
    url = request_to_url(request, path, VCBR_BASE_URL)
    if args.vcbr_cache:
        return await proxy_and_cache(request, url, local_path)
    return await proxy_and_cache(request, url, disable_cache=True)

@app.get("/")
async def read_index():
    if os.path.exists("dist/index.html"):
        with open("dist/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Inject custom_saves status
        custom_saves_val = "1" if args.custom_saves else "0"
        content = content.replace(
            'new URLSearchParams(window.location.search).get("custom_saves") === "1"',
            f'"{custom_saves_val}" === "1"'
        )
        
        return Response(content, media_type="text/html", headers={
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Embedder-Policy": "require-corp"
        })
    return Response("index.html not found", status_code=404)

app.mount("/", StaticFiles(directory="dist"), name="root")

def start_server(app=app, host="0.0.0.0", port=args.port):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    print(f"Starting server on http://localhost:{args.port}")
    print(f"vcsky: {'local' if args.vcsky_local else 'proxy'} ({VCSKY_BASE_URL if not args.vcsky_local else 'vcsky/'})")
    print(f"vcbr: {'local' if args.vcbr_local else 'proxy'} ({VCBR_BASE_URL if not args.vcbr_local else 'vcbr/'})")
    start_server()