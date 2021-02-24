eval "$(conda shell.bash hook)"
source /home/namvh/PTIT-IOT-Healthcare/venv/bin/active
python app.py &
# /snap/bin/ngrok http -subdomain=ptit03 8000 &
/snap/bin/ngrok http -subdomain=ptit03 8000 > /dev/null &
