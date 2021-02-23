eval "$(conda shell.bash hook)"
source venv/bin/active
python app.py &
/snap/bin/ngrok http -subdomain=ptit03 8000 &
