#!/bin/bash

echo "Installing Google Chrome..."

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update || true
apt-get install -y ./google-chrome-stable_current_amd64.deb || true

echo "Installing ChromeDriver..."

CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
