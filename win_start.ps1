python init_project.py
cd api
.\venv_win\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 5055 --reload
# flask run --host=0.0.0.0 --port=5055
# cd ..
# python open_weburl.py