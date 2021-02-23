eval "$(conda shell.bash hook)"
conda activate breath-env
python app.py &
/snap/bin/ngrok http -subdomain=ptit03 8000 &
