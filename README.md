# Emotion Analysis using the BRIGHTER dataset
- The project is split into the `backend` and `frontend` subdirectories
- Training files are located within the `training/notebooks` directory
- Models used by the backend (namely `api.py`) are loaded from Huggingface

## Running the backend

> 📘Note
>
> It is recommended that a virtual environment is created using `python -m venv <virtual_environment_name>`. 

**Instructions**
1. Navigate to the root of the project
2. Issue the command `python -m venv venv` to create the virtual environment named "venv", then activate the environment using the appropriate platform dependent script. E.g. For Powershell the command would be `venv/scripts/activate`
3. Load the required python dependencies (for the backend) using `pip install -r backend/requirements.txt`
4. After the required packages are installed, run the backend using `python backend/api.py`. The required models will be loaded from Huggingface and a server instance will be instantiated (on ` http://127.0.0.1:8000`).

## Running the Frontend 

> 📘Note
>
> NodeJS must be installed to run the frontend

1. Navigate to the `frontend` sub-directory with `cd frontend`
2. Install the necessary dependencies using `npm i`
3. Run the react application using `npm run dev`
4. A react instance will be instantiated (likely on `http://localhost:5173/`)
