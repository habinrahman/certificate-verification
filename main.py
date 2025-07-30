from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from supabase_config import get_certificate_by_id, get_all_certificates, supabase

app = FastAPI(title="Certificate Verification API", version="1.0.0")

# CORS for local, Vercel, and Render frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://certificate-verification-ecru.vercel.app",
        "https://certificate-three-wheat.vercel.app",
        "http://localhost:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files like CSS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading index page: {str(e)}")


@app.get("/home")
async def home_page():
    try:
        with open("home.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading home page: {str(e)}")


@app.get("/verify")
async def verify_page():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading verify page: {str(e)}")


@app.get("/test")
async def test_page():
    try:
        with open("test.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading test page: {str(e)}")


@app.get("/cert/{certificate_id}")
async def serve_certificate_page(certificate_id: str, request: Request):
    try:
        with open("certificate.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        base_url = str(request.base_url).rstrip("/")
        cert_data = get_certificate_by_id(certificate_id, base_url=base_url)

        if not cert_data:
            return HTMLResponse(
                content="<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Certificate Not Found</h2>",
                status_code=404,
            )

        html_content = (
            html_content.replace("{{student_name}}", cert_data["student_name"])
            .replace("{{course_name}}", cert_data["course"])
            .replace("{{completion_date}}", cert_data["completion_date"])
            .replace("{{certificate_id}}", cert_data["certificate_id"])
        )

        return HTMLResponse(content=html_content)

    except Exception as e:
        return HTMLResponse(
            content=f"<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Error: {str(e)}</h2>",
            status_code=500,
        )


@app.get("/certificates")
async def get_all_certificates_route():
    try:
        certificates = get_all_certificates()
        return {"success": True, "certificates": certificates}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.get("/debug")
async def debug_info():
    return {
        "supabase_url_set": bool(os.getenv("SUPABASE_URL")),
        "supabase_key_set": bool(os.getenv("SUPABASE_KEY")),
        "supabase_url": os.getenv("SUPABASE_URL", "Not set"),
        "environment": os.getenv("VERCEL_ENV", "local"),
    }


@app.get("/debug/certificates")
async def debug_all_certs():
    try:
        response = supabase.table("certificates").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}


@app.get("/{certificate_id}")
async def serve_verification_direct(certificate_id: str):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading verification page: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
