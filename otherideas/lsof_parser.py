#!/usr/bin/env python3
"""
Parse lsof network output and convert to JSON format
Usage: python3 lsof_parser.py
"""

import sys
import json
import re
import subprocess
import os

def get_lsof_output():
    """Run lsof command and return output lines"""
    try:
        # Check if we're running as root or with sudo
        if os.geteuid() != 0:
            print("Warning: Running without root privileges. Some processes may not be visible.", file=sys.stderr)
            print("For complete results, run with: sudo python3 lsof_parser.py", file=sys.stderr)
        
        # Run lsof command
        result = subprocess.run(['lsof', '-i'], capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    
    except subprocess.CalledProcessError as e:
        print(f"Error running lsof: {e}", file=sys.stderr)
        print("Make sure lsof is installed: sudo apt install lsof", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: lsof command not found", file=sys.stderr)
        print("Install lsof: sudo apt install lsof", file=sys.stderr)
        sys.exit(1)
    """Parse a single lsof output line into a dictionary"""
    # Split by whitespace, but be careful with the NAME field which can contain spaces
    parts = line.split()
    
    if len(parts) < 8:
        return None
    
    # Extract basic fields
    command = parts[0]
    pid = parts[1]
    user = parts[2]
    fd = parts[3]
    type_field = parts[4]
    device = parts[5]
    size_off = parts[6]
    node = parts[7]
    
    # The NAME field is everything after the 8th column
    name = ' '.join(parts[8:]) if len(parts) > 8 else ''
    
    # Parse the NAME field to extract network information
    protocol = None
    local_address = None
    remote_address = None
    state = None
    
    if name:
        # Check if it's a network connection
        if '->' in name:
            # TCP connection with remote endpoint
            local_part, remote_part = name.split('->', 1)
            local_address = local_part.strip()
            
            # Check if there's a state in parentheses
            if '(' in remote_part and ')' in remote_part:
                remote_address = remote_part.split('(')[0].strip()
                state = remote_part.split('(')[1].split(')')[0].strip()
            else:
                remote_address = remote_part.strip()
        else:
            # Listening socket or UDP
            local_address = name
            if '(LISTEN)' in name:
                local_address = name.replace('(LISTEN)', '').strip()
                state = 'LISTEN'
        
        # Determine protocol from the node field
        if node.upper() in ['TCP', 'UDP']:
            protocol = node.upper()
        elif 'TCP' in node.upper():
            protocol = 'TCP'
        elif 'UDP' in node.upper():
            protocol = 'UDP'
    
    return {
        'command': command,
        'pid': int(pid) if pid.isdigit() else pid,
        'user': user,
        'fd': fd,
        'type': type_field,
        'device': device,
        'size_off': size_off,
        'node': node,
        'protocol': protocol,
        'local_address': local_address,
        'remote_address': remote_address,
        'state': state,
        'raw_name': name
    }

def main():
    """Main function to run lsof, parse output and convert to JSON"""
    connections = []
    
    # Get lsof output
    lines = get_lsof_output()
    
    # Parse each line
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip header line
        if line.startswith('COMMAND') and 'PID' in line:
            continue
        
        # Parse the line
        parsed = parse_lsof_line(line)
        if parsed:
            connections.append(parsed)
        else:
            print(f"Warning: Could not parse line {line_num}: {line}", file=sys.stderr)
    
    # Output as JSON
    print(json.dumps(connections, indent=2))

if __name__ == "__main__":
    main()