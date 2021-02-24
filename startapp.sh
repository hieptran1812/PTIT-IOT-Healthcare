#!/bin/bash
eval "$(conda shell.bash hook)"
# active virtual environment
source venv/bin/activate
# run app.py
python app.py &
# /snap/bin/ngrok http -subdomain=ptit03 8000 &
/snap/bin/ngrok http -subdomain=ptit03 8000 
