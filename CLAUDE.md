# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of utility scripts and reference materials for various development and system administration tasks organized in subdirectories:

### `otherideas/` Directory
- **lsof_parser.py** / **lsof_parser_v2.py**: Python scripts for parsing `lsof` network output and converting it to JSON format
- **advanced_search_examples.md**: Comprehensive reference guide for advanced search syntax across Gmail, Google Drive, and GitHub
- **mcp.examples.json**: Configuration fragment for MCP (Model Context Protocol) server setup

### `plex-cert/` Directory
- **renew_cert.py**: Main Python script for automated SSL certificate generation and renewal using Certbot with Azure DNS
- **manual_renew.py**: Alternative Python script for manual certificate renewal
- **install_certbot.sh** / **install_alternate.sh**: Installation scripts for setting up Certbot environment
- **config/settings.json**: Configuration file for certificate renewal settings
- **secrets/azure.ini**: Azure DNS API credentials (with template available)
- **logs/**: Directory containing renewal operation logs
- **README.md**: Detailed documentation for the certificate renewal system

## Usage Instructions

### lsof Parser Scripts (in `otherideas/`)
```bash
# Run with root privileges for complete visibility
sudo python3 otherideas/lsof_parser.py
# or
sudo python3 otherideas/lsof_parser_v2.py

# Basic usage (limited visibility without sudo)
python3 otherideas/lsof_parser.py
```

### SSL Certificate Renewal Scripts (in `plex-cert/`)
```bash
# Main renewal script
python3 plex-cert/renew_cert.py

# Manual renewal alternative
python3 plex-cert/manual_renew.py

# Install Certbot environment
bash plex-cert/install_certbot.sh
# or alternative installation
bash plex-cert/install_alternate.sh

# Configure Azure credentials in plex-cert/secrets/azure.ini
# Configure settings in plex-cert/config/settings.json
```

## Key Dependencies

### Python Scripts
- Python 3.x standard library (json, re, subprocess, os, sys)
- Requires `lsof` system utility: `sudo apt install lsof`

### SSL Certificate Scripts (plex-cert/)
- Certbot and certbot-dns-azure (installed via pip in virtual environment)
- OpenSSL for certificate format conversion
- Azure DNS credentials file at `plex-cert/secrets/azure.ini`
- Python 3 with venv support: `sudo apt install python3-venv`
- Configuration managed through `plex-cert/config/settings.json`

## Architecture Notes

### lsof Parsers
- Executes system `lsof -i` command to capture network connections
- Parses structured output fields: command, PID, user, file descriptor, type, device, size/offset, node, and name
- Extracts network-specific information: protocol, local/remote addresses, connection state
- Outputs structured JSON with both parsed fields and raw data for debugging

### Certificate Management Scripts (plex-cert/)
- **renew_cert.py**: Main automated renewal script with JSON-based configuration
- **manual_renew.py**: Alternative manual process script
- Creates isolated Python virtual environment for Certbot installation
- Uses Azure DNS challenge for domain validation (suitable for servers behind firewalls)
- Generates both standard PEM certificates and PFX format for Windows/IIS compatibility
- Implements proper file permissions and directory structure for certificate storage
- Comprehensive logging system in `logs/` directory

### Reference Materials (otherideas/)
- **advanced_search_examples.md**: Provides comprehensive syntax references for platform-specific search capabilities
- **mcp.examples.json**: Contains MCP server configuration for integrating external tools like Semgrep

## Security Considerations

- lsof parser requires elevated privileges for complete system visibility
- SSL scripts handle sensitive Azure DNS credentials with restricted file permissions (600) in `plex-cert/secrets/azure.ini`
- Certificate files stored in user-controlled directories with appropriate access controls
- Configuration files contain sensitive domain and path information
- All scripts include error handling and validation for required parameters and dependencies
- Comprehensive logging for audit trail and troubleshooting