#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define a function to set up Certbot and generate SSL certificates
setup_certbot_plex() {
    # Ensure $dir, $domain, and $CERTBOT_EMAIL are set in the environment or passed as arguments.
    # Example usage:
    # dir="/home/freyr/homeprojects/plex-azure" domain="your.domain.com" CERTBOT_EMAIL="your@email.com" setup_certbot_plex
    if [ -z "$dir" ]; then
        echo "Error: 'dir' variable is not set. Please set it to the base directory for Certbot configurations."
        exit 1
    fi
    if [ -z "$domain" ]; then
        echo "Error: 'domain' variable is not set. Please set it to your domain name."
        exit 1
    fi
    if [ -z "$CERTBOT_EMAIL" ]; then
        echo "Error: 'CERTBOT_EMAIL' variable is not set. Please set it to your email address for Certbot."
        exit 1
    fi

    echo "Starting Certbot setup for domain: $domain with email: $CERTBOT_EMAIL"
    echo "Using base directory: $dir"

    # Install python3-venv if not already installed
    echo "Installing python3-venv..."
    # Using 'sudo apt update' before install to ensure package lists are up-to-date
    sudo apt update && sudo apt install -y python3-venv

    # Create and activate a Python virtual environment for Certbot
    echo "Setting up Certbot virtual environment..."
    python3 -m venv "$HOME/certbot-venv"
    source "$HOME/certbot-venv/bin/activate"

    # Install Certbot and the Azure DNS plugin
    echo "Installing Certbot and certbot-dns-azure..."
    pip install certbot certbot-dns-azure

    # Ensure the secrets directory exists and set permissions for azure.ini
    echo "Setting up Certbot secrets directory and permissions..."
    mkdir -p "$dir/.secrets/certbot"
    # Check if azure.ini exists before setting permissions
    if [ ! -f "$dir/.secrets/certbot/azure.ini" ]; then
        echo "Error: Azure DNS credentials file '$dir/.secrets/certbot/azure.ini' not found."
        echo "Please create this file with your Azure DNS credentials before running the script."
        deactivate # Deactivate venv before exiting
        exit 1
    fi
    chmod 600 "$dir/.secrets/certbot/azure.ini"
    echo "Permissions set for $dir/.secrets/certbot/azure.ini"

    # Create Certbot configuration directories if they don't exist
    echo "Creating Certbot configuration directories..."
    mkdir -p "$dir/.config/letsencrypt"
    mkdir -p "$dir/.local/share/letsencrypt"
    mkdir -p "$dir/.local/log/letsencrypt"

    # Run Certbot to obtain the certificate
    echo "Running Certbot to obtain certificate for $domain..."
    certbot certonly \
        --authenticator dns-azure \
        --dns-azure-credentials "$dir/.secrets/certbot/azure.ini" \
        --dns-azure-propagation-seconds 30 \
        -d "$domain" \
        --non-interactive \
        --agree-tos \
        --email "$CERTBOT_EMAIL" \
        --config-dir "$dir/.config/letsencrypt" \
        --work-dir "$dir/.local/share/letsencrypt" \
        --logs-dir "$dir/.local/log/letsencrypt" \
        -v

    echo "Certbot certificate obtained successfully."

    # Deactivate the virtual environment
    deactivate

    # Convert the certificate to PFX format using openssl
    # Certificates are stored in the --config-dir/live/<domain>/
    CERT_LIVE_DIR="$dir/.config/letsencrypt/live/$domain"
    PFX_OUTPUT_PATH="$dir/$domain.pfx" # Output PFX to the base directory

    echo "Converting certificate to PFX format using OpenSSL..."
    echo "Looking for certificates in: $CERT_LIVE_DIR"

    if [ ! -d "$CERT_LIVE_DIR" ]; then
        echo "Error: Certbot live directory '$CERT_LIVE_DIR' not found."
        echo "This usually means Certbot failed to obtain the certificate or stored it elsewhere."
        exit 1
    fi

    # No sudo needed for openssl if certificates are in user-writable $dir
    openssl pkcs12 -export \
        -out "$PFX_OUTPUT_PATH" \
        -inkey "$CERT_LIVE_DIR/privkey.pem" \
        -in "$CERT_LIVE_DIR/fullchain.pem" \
        -certfile "$CERT_LIVE_DIR/fullchain.pem" \
        -name "$domain" # Add a friendly name to the certificate

    echo "PFX file created at: $PFX_OUTPUT_PATH"

    # Verify the PFX file (optional)
    echo "Verifying PFX file..."
    openssl pkcs12 -in "$PFX_OUTPUT_PATH" -info -nodes -noout

    echo "Script finished successfully."
}

# How to use this script:
#
# 1. Make it executable (if you want to run it directly):
#    chmod +x environment/plex/function.sh
#
# 2. Set the required environment variables and then call the function.
#    Example for direct execution:
#    dir="/home/freyr/homeprojects/plex-azure" \
#    domain="your.domain.com" \
#    CERTBOT_EMAIL="your@email.com" \
#    ./environment/plex/function.sh
#
#    Example for sourcing and then calling:
#    source environment/plex/function.sh
#    dir="/home/freyr/homeprojects/plex-azure" \
#    domain="your.domain.com" \
#    CERTBOT_EMAIL="your@email.com" \
#    setup_certbot_plex
#
#    Replace "your.domain.com" and "your@email.com" with your actual domain and email.
#    The 'dir' variable should point to the base directory where you want Certbot configurations
#    and the output PFX file to be stored.
