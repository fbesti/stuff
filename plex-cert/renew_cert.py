#!/usr/bin/env python3
"""
Plex Certificate Renewal Script

Automates SSL certificate renewal for Plex servers using Certbot with Azure DNS challenge.
Converts certificates to PFX format for easy import into Plex.

Usage: python3 renew_cert.py
"""

import os
import sys
import json
import subprocess
import shutil
import logging
from pathlib import Path
from datetime import datetime


class PlexCertRenewer:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_file = self.script_dir / "config" / "settings.json"
        self.azure_credentials = self.script_dir / "secrets" / "azure.ini"
        self.venv_path = Path.home() / "certbot-venv"
        
        # Setup logging
        log_dir = self.script_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"renewal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from settings.json"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {self.config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _check_prerequisites(self):
        """Check if all required files and dependencies exist"""
        self.logger.info("Checking prerequisites...")
        
        # Check if Azure credentials exist
        if not self.azure_credentials.exists():
            self.logger.error(f"Azure credentials file not found: {self.azure_credentials}")
            self.logger.error("Please create the azure.ini file with your Azure DNS credentials")
            sys.exit(1)
        
        # Check if OpenSSL is available
        if not shutil.which('openssl'):
            self.logger.error("OpenSSL not found. Please install OpenSSL.")
            sys.exit(1)
        
        # Check required config fields
        required_fields = ['domain', 'email']
        for field in required_fields:
            if not self.config.get(field):
                self.logger.error(f"Required configuration field '{field}' is missing or empty")
                sys.exit(1)
        
        self.logger.info("Prerequisites check passed")
    
    def _setup_venv(self):
        """Create and setup Python virtual environment for Certbot"""
        self.logger.info("Setting up Certbot virtual environment...")
        
        if self.venv_path.exists():
            self.logger.info("Virtual environment already exists")
        else:
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], check=True)
            self.logger.info(f"Virtual environment created at {self.venv_path}")
        
        # Install/upgrade certbot packages
        pip_path = self.venv_path / "bin" / "pip"
        packages = ['certbot>=2.0,<3.0', 'certbot-dns-azure']
        
        self.logger.info("Installing/upgrading Certbot packages...")
        subprocess.run([
            str(pip_path), 'install', '--upgrade'
        ] + packages, check=True)
        
        self.logger.info("Certbot environment setup complete")
    
    def _create_directories(self):
        """Create necessary directories for Certbot"""
        directories = [
            self.script_dir / "certs" / "letsencrypt" / "config",
            self.script_dir / "certs" / "letsencrypt" / "work", 
            self.script_dir / "certs" / "letsencrypt" / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
    
    def _run_certbot(self):
        """Run Certbot to obtain the certificate"""
        self.logger.info(f"Running Certbot for domain: {self.config['domain']}")
        
        certbot_path = self.venv_path / "bin" / "certbot"
        config_dir = self.script_dir / "certs" / "letsencrypt" / "config"
        work_dir = self.script_dir / "certs" / "letsencrypt" / "work"
        logs_dir = self.script_dir / "certs" / "letsencrypt" / "logs"
        
        cmd = [
            str(certbot_path),
            'certonly',
            '--authenticator', 'dns-azure',
            '--dns-azure-credentials', str(self.azure_credentials),
            '--dns-azure-propagation-seconds', '30',
            '-d', self.config['domain'],
            '--non-interactive',
            '--agree-tos',
            '--email', self.config['email'],
            '--config-dir', str(config_dir),
            '--work-dir', str(work_dir),
            '--logs-dir', str(logs_dir),
            '-v'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            self.logger.info("Certificate obtained successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Certbot failed with exit code {e.returncode}")
            raise
    
    def _convert_to_pfx(self):
        """Convert certificate to PFX format"""
        domain = self.config['domain']
        cert_live_dir = self.script_dir / "certs" / "letsencrypt" / "config" / "live" / domain
        pfx_output = self.script_dir / "certs" / f"{domain}.pfx"
        
        self.logger.info("Converting certificate to PFX format...")
        self.logger.info(f"Looking for certificates in: {cert_live_dir}")
        
        if not cert_live_dir.exists():
            self.logger.error(f"Certificate directory not found: {cert_live_dir}")
            raise FileNotFoundError("Certificate directory not found")
        
        # Get PFX password from config or prompt
        pfx_password = self.config.get('pfx_password', '')
        if not pfx_password:
            self.logger.info("No PFX password configured - using empty password")
        
        cmd = [
            'openssl', 'pkcs12', '-export',
            '-out', str(pfx_output),
            '-inkey', str(cert_live_dir / 'privkey.pem'),
            '-in', str(cert_live_dir / 'fullchain.pem'),
            '-certfile', str(cert_live_dir / 'fullchain.pem'),
            '-name', domain,
            '-passout', f'pass:{pfx_password}'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"PFX file created: {pfx_output}")
            
            # Verify the PFX file
            verify_cmd = [
                'openssl', 'pkcs12',
                '-in', str(pfx_output),
                '-info', '-nodes', '-noout',
                '-passin', f'pass:{pfx_password}'
            ]
            subprocess.run(verify_cmd, check=True, capture_output=True)
            self.logger.info("PFX file verified successfully")
            
            return pfx_output
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"PFX conversion failed with exit code {e.returncode}")
            raise
    
    def renew_certificate(self):
        """Main method to renew the certificate"""
        try:
            self.logger.info("Starting certificate renewal process...")
            self.logger.info(f"Domain: {self.config['domain']}")
            self.logger.info(f"Email: {self.config['email']}")
            
            self._check_prerequisites()
            self._setup_venv()
            self._create_directories()
            self._run_certbot()
            pfx_file = self._convert_to_pfx()
            
            self.logger.info("Certificate renewal completed successfully!")
            self.logger.info(f"PFX file ready for Plex: {pfx_file}")
            self.logger.info("\nNext steps:")
            self.logger.info("1. Copy the PFX file to your Plex server")
            self.logger.info("2. Import it in Plex Settings > Network > Custom certificate location")
            
        except Exception as e:
            self.logger.error(f"Certificate renewal failed: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    renewer = PlexCertRenewer()
    renewer.renew_certificate()


if __name__ == "__main__":
    main()