import os
import argparse
from uvicorn import run
from multiprocessing import freeze_support
from main import app
def main():
    parser = argparse.ArgumentParser(description='Start the FastAPI app with a specific environment.')
    parser.add_argument('--env', type=str, required=False)

    run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    freeze_support()
    main()