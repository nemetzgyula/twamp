#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Creating base directory: /opt/twampy"
mkdir -p /opt/twampy
cd /opt/twampy

echo "Cleaning /opt/twampy (except existing virtualenv)"
find . -mindepth 1 -not -path "./python3*" -exec rm -rf {} +

echo "Cloning nemetzgyula/twamp into /opt/twampy"
temp_twamp=$(mktemp -d)
git clone https://github.com/nemetzgyula/twamp.git "$temp_twamp"
cp -rT "$temp_twamp" /opt/twampy
rm -rf "$temp_twamp"

echo "📥 Cloning nokia/twampy into /opt/twampy"
temp_twampy=$(mktemp -d)
git clone https://github.com/nokia/twampy.git "$temp_twampy"
cp -rT "$temp_twampy" /opt/twampy
rm -rf "$temp_twampy"

echo "Updating system and installing Python3"
apt-get update -y
apt-get install -y python3 python3-venv python3-pip

echo "Creating Python virtual environment at /opt/twampy/python3"
python3 -m venv /opt/twampy/python3

echo "Installing required Python packages"
source /opt/twampy/python3/bin/activate
pip install --upgrade pip
pip install python-dotenv pymysql

chmod 755 run.sh

echo "Modifying run.sh to use virtual environment's Python"
if [[ -f "/opt/twampy/run.sh" ]]; then
    sed -i 's|python3 /opt/twampy/process.py|/opt/twampy/python3/bin/python3 /opt/twampy/process.py|' /opt/twampy/run.sh
    echo "run.sh updated successfully."
else
    echo "run.sh not found, skipping modification."
fi

echo "Setting up cron job to run every minute"
cron_entry="* * * * * /opt/twampy/run.sh"
(crontab -l 2>/dev/null | grep -Fv "/opt/twampy/run.sh"; echo "$cron_entry") | crontab -
echo "Cron job added."

/etc/init.d/cron restart

echo "Verifying directory structure:"
[[ -d "/opt/twampy" ]] && echo "/opt/twampy exists"
[[ -d "/opt/twampy/twampy" ]] && echo "nokia/twampy repository cloned"
[[ -d "/opt/twampy/twamp" ]] && echo "nemetzgyula/twamp repository cloned"
[[ -d "/opt/twampy/python3" ]] && echo "Python virtual environment created"

echo "Setup completed successfully!"
