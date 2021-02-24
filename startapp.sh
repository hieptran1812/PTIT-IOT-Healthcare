eval "$(conda shell.bash hook)"
# active virtual environment
source /home/namvh/PTIT-IOT-Healthcare/venv/bin/active
# run app.py
python app.py &
# /snap/bin/ngrok http -subdomain=ptit03 8000 &
/snap/bin/ngrok http -subdomain=ptit03 8000 > /dev/null &
