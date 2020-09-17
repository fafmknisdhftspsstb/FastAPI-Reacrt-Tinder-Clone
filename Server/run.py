import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run("server:app", host=config.IP_ADDR, port=config.PORT, reload=True, debug=True, workers=1)