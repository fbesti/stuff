#!/usr/bin/env python3
"""
Manual Certificate Renewal Script

This script guides you through manual certificate renewal when Azure DNS automation fails.
It uses certbot with manual DNS challenge and helps convert to PFX format.
"""

import os
import sys
import json
import subprocess
import shutil
import logging
from pathlib import Path
from datetime import datetime


class ManualCertRenewer:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_file = self.script_dir / "config" / "settings.json"
        
        # Setup logging
        log_dir = self.script_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"manual_renewal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
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
        """Check if all required dependencies exist"""
        self.logger.info("Checking prerequisites...")
        
        # Check if certbot is available (try system first)
        if not shutil.which('certbot'):
            self.logger.error("Certbot not found. Please install certbot.")
            self.logger.info("On Ubuntu/Debian: sudo apt install certbot")
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
    
    def _create_directories(self):
        """Create necessary directories for certificates"""
        directories = [
            self.script_dir / "certs" / "manual" / "config",
            self.script_dir / "certs" / "manual" / "work", 
            self.script_dir / "certs" / "manual" / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
    
    def _run_manual_certbot(self):
        """Run Certbot with manual DNS challenge"""
        self.logger.info(f"Starting manual certificate process for domain: {self.config['domain']}")
        
        config_dir = self.script_dir / "certs" / "manual" / "config"
        work_dir = self.script_dir / "certs" / "manual" / "work"
        logs_dir = self.script_dir / "certs" / "manual" / "logs"
        
        cmd = [
            'certbot',
            'certonly',
            '--manual',
            '--preferred-challenges', 'dns',
            '-d', self.config['domain'],
            '--agree-tos',
            '--email', self.config['email'],
            '--config-dir', str(config_dir),
            '--work-dir', str(work_dir),
            '--logs-dir', str(logs_dir),
            '-v'
        ]
        
        self.logger.info("Running manual certbot process...")
        self.logger.info("IMPORTANT: You will be prompted to create DNS TXT records manually")
        self.logger.info("Follow the certbot instructions to create the DNS records in Azure DNS")
        
        try:
            subprocess.run(cmd, check=True)
            self.logger.info("Certificate obtained successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Certbot failed with exit code {e.returncode}")
            raise
    
    def _convert_to_pfx(self):
        """Convert certificate to PFX format"""
        domain = self.config['domain']
        cert_live_dir = self.script_dir / "certs" / "manual" / "config" / "live" / domain
        pfx_output = self.script_dir / "certs" / f"{domain}-manual.pfx"
        
        self.logger.info("Converting certificate to PFX format...")
        self.logger.info(f"Looking for certificates in: {cert_live_dir}")
        
        if not cert_live_dir.exists():
            self.logger.error(f"Certificate directory not found: {cert_live_dir}")
            raise FileNotFoundError("Certificate directory not found")
        
        # Get PFX password from config or use empty password
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
        """Main method to manually renew the certificate"""
        try:
            self.logger.info("Starting MANUAL certificate renewal process...")
            self.logger.info(f"Domain: {self.config['domain']}")
            self.logger.info(f"Email: {self.config['email']}")
            
            print("\n" + "="*60)
            print("MANUAL CERTIFICATE RENEWAL")
            print("="*60)
            print("This script will guide you through manual certificate renewal.")
            print("You will need to create DNS TXT records manually in Azure DNS.")
            print("Make sure you have access to your Azure DNS zone.")
            print("="*60 + "\n")
            
            input("Press Enter to continue...")
            
            self._check_prerequisites()
            self._create_directories()
            self._run_manual_certbot()
            pfx_file = self._convert_to_pfx()
            
            self.logger.info("Certificate renewal completed successfully!")
            self.logger.info(f"PFX file ready for Plex: {pfx_file}")
            
            print("\n" + "="*60)
            print("SUCCESS! Certificate renewal completed!")
            print("="*60)
            print(f"PFX file location: {pfx_file}")
            print("\nNext steps:")
            print("1. Copy the PFX file to your Plex server")
            print("2. Import it in Plex Settings > Network > Custom certificate location")
            print("3. Restart Plex Media Server")
            print("="*60)
            
        except Exception as e:
            self.logger.error(f"Manual certificate renewal failed: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    renewer = ManualCertRenewer()
    renewer.renew_certificate()


if __name__ == "__main__":
    main()