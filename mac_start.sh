#!/usr/bin/env bash
python init_project.py
cd api
source venv_mac/bin/activate
uvicorn main:app --host 0.0.0.0 --port 5055 --reload
