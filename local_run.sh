#! /bin/bash
echo "======================================================================"
echo "Welcome to the application. It will run the application in development mode."
echo "----------------------------------------------------------------------"
if [ -d "venv" ];
then
    echo "Enabling python 3.11 virtual env"
    # Activate virtual env
    . venv/bin/activate
else
    echo "No Virtual env detected. Please run setup.sh first"
    exit 1
fi

# Start SMTP Server
python3 -m smtpd -c DebuggingServer -n localhost:1025 &

# Stop SMTP Server on EXIT
trap 'pkill -9 python3; exit' ERR EXIT

# run the application through uvicorn in debug mode
uvicorn main:app --reload

# Deactivate virtual env 
deactivate
