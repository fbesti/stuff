# Plex Certificate Renewal

SSL certificate renewal for Plex servers. Two options available:

1. **Automated** (renew_cert.py) - Uses Certbot with Azure DNS plugin (currently has compatibility issues)
2. **Manual** (manual_renew.py) - Uses manual DNS challenge (recommended for urgent renewals)

## Quick Start (Manual Renewal - RECOMMENDED)

Since your certificate expires tomorrow, use the manual approach:

1. Install certbot: `./install_certbot.sh` (requires sudo)
2. Run manual renewal: `python3 manual_renew.py`

## Setup

### 1. Configure Your Email
Edit `config/settings.json` and replace `YOUR_EMAIL_HERE` with your actual email address:

```json
{
    "domain": "plex.bigpapa.work",
    "email": "your.email@example.com",
    "pfx_password": ""
}
```

### 2. Setup Azure DNS Credentials
Copy the template and fill in your Azure credentials:

```bash
cp secrets/azure.ini.template secrets/azure.ini
```

Edit `secrets/azure.ini` with your Azure service principal credentials:

```ini
dns_azure_sp_client_id = your-client-id
dns_azure_sp_client_secret = your-client-secret
dns_azure_tenant_id = your-tenant-id
dns_azure_subscription_id = your-subscription-id
dns_azure_zone1 = bigpapa.work
```

### 3. Make Script Executable
```bash
chmod +x renew_cert.py
```

## Usage

When your certificate is about to expire, simply run:

```bash
python3 renew_cert.py
```

The script will:
1. Setup a Python virtual environment for Certbot
2. Install required packages
3. Run Certbot with Azure DNS challenge
4. Convert the certificate to PFX format
5. Store everything in the `certs/` directory

## Output

- **Certificate files**: `certs/letsencrypt/config/live/plex.bigpapa.work/`
- **PFX file**: `certs/plex.bigpapa.work.pfx`
- **Logs**: `logs/renewal_YYYYMMDD_HHMMSS.log`

## Import to Plex

1. Copy the PFX file (`certs/plex.bigpapa.work.pfx`) to your Plex server
2. In Plex Settings → Network → Custom certificate location
3. Browse to the PFX file and import it
4. Restart Plex Media Server

## Requirements

- Python 3.6+
- OpenSSL
- Azure DNS zone configured for your domain
- Azure service principal with DNS Zone Contributor permissions

## Troubleshooting

Check the log files in the `logs/` directory for detailed error information. The script provides clear error messages and logging throughout the process.