import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8017,
        reload=True,
        log_level="info",
        access_log=True
    ) 