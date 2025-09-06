#!/bin/bash

# Install script for certbot using snap
# Run this script to install certbot for manual certificate renewal

echo "Installing certbot via snap..."
echo "Note: This will require sudo privileges"

# Install snapd if not available
if ! command -v snap &> /dev/null; then
    echo "Installing snapd..."
    sudo apt update
    sudo apt install -y snapd
fi

# Install certbot via snap
echo "Installing certbot..."
sudo snap install --classic certbot

# Create symlink for easy access
echo "Creating symlink..."
sudo ln -sf /snap/bin/certbot /usr/bin/certbot

echo "Certbot installation complete!"
echo "You can now run: python3 manual_renew.py"