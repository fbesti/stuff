# Plex Certificate Renewal Guide

## 1. Debug the Current Failure

Run Certbot manually to see detailed error output:

```bash
/home/freyr/certbot-venv/bin/certbot certonly \
  --authenticator dns-azure \
  --dns-azure-credentials /home/freyr/homeprojects/stuff/plex-cert/secrets/azure.ini \
  --dns-azure-propagation-seconds 30 \
  -d plex.bigpapa.work \
  --non-interactive \
  --agree-tos \
  --email freyr.finnbogason@gmail.com \
  --config-dir /home/freyr/homeprojects/stuff/plex-cert/certs/letsencrypt/config \
  --work-dir /home/freyr/homeprojects/stuff/plex-cert/certs/letsencrypt/work \
  --logs-dir /home/freyr/homeprojects/stuff/plex-cert/certs/letsencrypt/logs \
  -v
```

## 2. Alternative Approaches

### Option A: Use the existing Python script with debugging
```bash
cd /home/freyr/homeprojects/stuff/plex-cert
python3 renew_cert.py
```

### Option B: Try the manual renewal script
```bash
cd /home/freyr/homeprojects/stuff/plex-cert
python3 manual_renew.py
```

### Option C: Reinstall Certbot environment
```bash
cd /home/freyr/homeprojects/stuff/plex-cert
bash install_alternate.sh
```

## 3. Likely Issues to Check

1. **Azure credentials expiration** - Verify your Azure service principal credentials are still valid
2. **DNS zone permissions** - Ensure the service principal has DNS Zone Contributor role
3. **Certbot-dns-azure plugin version** - May need update or downgrade
4. **Network connectivity** - Check if the server can reach Azure DNS APIs

## 4. Quick Validation Steps

Test Azure credentials:
```bash
az login --service-principal \
  -u 4a79e796-cfbd-4d5b-a4c1-f3358c825553 \
  -p <password> \
  --tenant 0d7c675e-2aec-4a6b-b02d-d089194b2ea9
```

Check DNS zone access:
```bash
az network dns zone show --resource-group rg-ot-dns-001 --name bigpapa.work
```

Start with the manual Certbot command to see the actual error details, then proceed based on what specific error you encounter.

## 5. Deploy Certificate to Plex Server

Once the certificate is created (for now using manual method Option B):

### 1. Copy to Plex server
```bash
scp $HOME/homeprojects/stuff/plex-cert/certs/plex.bigpapa.work-manual.pfx freyr@192.168.1.11:/home/freyr/plexcert/plex.bigpapa.work-manual.pfx
```

### 2. SSH into the Plex media server
```bash
ssh freyr@192.168.1.11
```

### 3. Set proper ownership
```bash
sudo chown plex:plex /etc/ssl/plex/plex.bigpapa.work-manual.pfx
```

### 4. Configure Plex
- Set the pfx password in **Network > Settings > Advanced > Custom certificate encryption key**
- Set **Custom certificate location** to point to the correct certificate

### 5. Restart Plex Media Server
```bash
sudo systemctl restart plexmediaserver
```