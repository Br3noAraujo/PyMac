#!/usr/bin/python3
#! coding: utf-8
"""
PyMac: Cross-platform, fast MAC address changer and restorer.
"I am PyMac. Become untraceable. Mask your identity at the edge of the network."
Coded By Br3noAraujo | github.com/Br3noAraujo
"""

import os
import sys
import re
import random
import subprocess
import platform
import argparse
import logging
from datetime import datetime
from colorama import Fore, Style, init
import pickle
from pathlib import Path

init(autoreset=True)

# ========== BANNER ==========
def print_banner():
    banner = f"""
{Fore.LIGHTCYAN_EX}
██████╗ ██╗   ██╗███╗   ███╗ █████╗  ██████╗
██╔══██╗╚██╗ ██╔╝████╗ ████║██╔══██╗██╔════╝
██████╔╝ ╚████╔╝ ██╔████╔██║███████║██║     
██╔═══╝   ╚██╔╝  ██║╚██╔╝██║██╔══██║██║     
██║        ██║   ██║ ╚═╝ ██║██║  ██║╚██████╗
╚═╝        ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝
{Fore.LIGHTGREEN_EX}🛡️ I am PyMac. Become untraceable. Mask your identity at the edge of the network.
{Fore.CYAN}By Br3noAraujo | github.com/Br3noAraujo{Style.RESET_ALL}
    """
    print(banner)

# ========== LOGGING ==========
LOG_FILE = "pymac.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_event(msg):
    logging.info(msg)

# ========== PERMISSION CHECK ==========
def check_root():
    if os.name != 'nt' and os.geteuid() != 0:
        print(f"{Fore.LIGHTRED_EX}❌ [!] This script requires root/sudo privileges!{Style.RESET_ALL}")
        sys.exit(1)
    elif os.name == 'nt':
        print(f"{Fore.LIGHTRED_EX}❌ [!] Limited functionality on Windows. Run as Administrator to try.{Style.RESET_ALL}")

# ========== INTERFACE DETECTION ==========
def list_interfaces():
    system = platform.system()
    interfaces = []
    if system == 'Linux':
        try:
            output = subprocess.check_output(['ip', 'link'], encoding='utf-8')
            interfaces = re.findall(r'\d+: ([^:]+):', output)
        except Exception:
            output = subprocess.check_output(['ifconfig', '-a'], encoding='utf-8')
            interfaces = re.findall(r'^(\w+):', output, re.MULTILINE)
    elif system == 'Darwin':
        output = subprocess.check_output(['networksetup', '-listallhardwareports'], encoding='utf-8')
        interfaces = re.findall(r'Device: (.+)', output)
    elif system == 'Windows':
        output = subprocess.check_output(['getmac'], encoding='utf-8')
        interfaces = re.findall(r'([A-Za-z0-9]+)\s', output)
    return interfaces

# ========== MAC GENERATION ==========
def generate_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# ========== MAC VALIDATION ==========
def is_valid_mac(mac):
    return re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac) is not None

# ========== GET CURRENT MAC ==========
def get_current_mac(interface):
    system = platform.system()
    try:
        if system == 'Linux':
            path = f'/sys/class/net/{interface}/address'
            if not Path(path).exists():
                print(f"{Fore.LIGHTYELLOW_EX}⚠️ [!] PyMac: Interface '{interface}' does not exist on this system.{Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX}💡 Tip: Use '-l' or '--list' to see available interfaces.{Style.RESET_ALL}")
                return None
            output = subprocess.check_output(['cat', path], encoding='utf-8')
            return output.strip()
        elif system == 'Darwin':
            try:
                output = subprocess.check_output(['ifconfig', interface], encoding='utf-8')
            except subprocess.CalledProcessError:
                print(f"{Fore.LIGHTYELLOW_EX}⚠️ [!] PyMac: Interface '{interface}' does not exist on this system.{Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX}💡 Tip: Use '-l' or '--list' to see available interfaces.{Style.RESET_ALL}")
                return None
            match = re.search(r'ether ([0-9a-f:]{17})', output)
            return match.group(1) if match else None
        elif system == 'Windows':
            print(f"{Fore.LIGHTYELLOW_EX}⚠️ [!] PyMac: Showing MAC on Windows is limited. Use getmac in the terminal.{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}❌ [!] PyMac: Error getting MAC for interface '{interface}': {e}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}💡 Tip: Use '-l' or '--list' to see available interfaces.{Style.RESET_ALL}")
        return None

# ========== MAC SPOOF / RESTORE ==========
def change_mac(interface, new_mac):
    system = platform.system()
    try:
        # Save the original MAC before changing
        orig_mac = get_current_mac(interface)
        if orig_mac and orig_mac != new_mac:
            save_original_mac(interface, orig_mac)
        if system == 'Linux':
            subprocess.call(['ip', 'link', 'set', 'dev', interface, 'down'])
            subprocess.call(['ip', 'link', 'set', 'dev', interface, 'address', new_mac])
            subprocess.call(['ip', 'link', 'set', 'dev', interface, 'up'])
        elif system == 'Darwin':
            subprocess.call(['sudo', 'ifconfig', interface, 'ether', new_mac])
        elif system == 'Windows':
            print(f"{Fore.LIGHTYELLOW_EX}⚠️ [!] PyMac: Changing MAC on Windows is not supported. Use specific tools.{Style.RESET_ALL}")
            return False
        print(f"{Fore.LIGHTGREEN_EX}✅ [+] PyMac: MAC of {interface} changed to {new_mac}{Style.RESET_ALL}")
        log_event(f"PyMac: MAC of {interface} changed to {new_mac}")
        return True
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}❌ [!] PyMac: Failed to change MAC: {e}{Style.RESET_ALL}")
        return False

def restore_mac(interface):
    orig_mac = load_original_mac(interface)
    if not orig_mac:
        print(f"{Fore.LIGHTRED_EX}❌ [!] PyMac: No original MAC saved for {interface}. I can't restore it automatically!{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}💡 Use the -R argument to set the original MAC manually.{Style.RESET_ALL}")
        return False
    print(f"{Fore.LIGHTCYAN_EX}🔄 [!] PyMac: Restoring original MAC for {interface}: {Fore.LIGHTGREEN_EX}{orig_mac}{Style.RESET_ALL}")
    return change_mac(interface, orig_mac)

# ========== STATE MANAGEMENT ==========
STATE_FILE = Path.home() / '.pymac_state.pkl'

def save_original_mac(interface, mac):
    state = {}
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open('rb') as f:
                state = pickle.load(f)
        except Exception:
            state = {}
    state[interface] = mac
    with STATE_FILE.open('wb') as f:
        pickle.dump(state, f)

def load_original_mac(interface):
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open('rb') as f:
                state = pickle.load(f)
            return state.get(interface)
        except Exception:
            return None
    return None

# ========== CLI / PARSER ==========
def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description=f"{Fore.LIGHTCYAN_EX}PyMac: Cross-platform tool to change/restore MAC addresses. I am PyMac, your MAC identity manipulator.{Style.RESET_ALL}\n\n{Fore.LIGHTCYAN_EX}Usage:{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py [options]{Style.RESET_ALL}\n\n{Fore.LIGHTCYAN_EX}Examples:{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -l{Style.RESET_ALL}                {Fore.LIGHTGREEN_EX}# List interfaces{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -s -i eth0{Style.RESET_ALL}         {Fore.LIGHTGREEN_EX}# Show current MAC{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -r -i eth0{Style.RESET_ALL}         {Fore.LIGHTGREEN_EX}# Generate and apply random MAC{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -c 00:11:22:33:44:55 -i eth0{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}# Set custom MAC{Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -R -i eth0{Style.RESET_ALL}         {Fore.LIGHTGREEN_EX}# Restore original MAC (PyMac auto){Style.RESET_ALL}\n  {Fore.LIGHTBLUE_EX}sudo ./pymac.py -f -i eth0{Style.RESET_ALL}         {Fore.LIGHTGREEN_EX}# Generate and apply funny MAC{Style.RESET_ALL}",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument('-l', '--list', action='store_true', help='List active network interfaces')
    parser.add_argument('-s', '--show', action='store_true', help='Show current MAC address of the interface')
    parser.add_argument('-r', '--random', action='store_true', help='Generate and apply a random MAC address')
    parser.add_argument('-c', '--set', type=str, help='Set custom MAC address (e.g. -c "XX:XX:XX:XX:XX:XX")')
    parser.add_argument('-R', '--restore', action='store_true', help='Restore original MAC address (if known by PyMac)')
    parser.add_argument('-i', '--iface', type=str, help='Target network interface')
    parser.add_argument('--log', action='store_true', help='Enable logging to pymac.log')
    parser.add_argument('-h', '--help', action='help', help='Show this custom help and usage examples')
    parser.add_argument('-f', '--funny', action='store_true', help='Generate and apply a funny MAC address')
    args = parser.parse_args()

    # Minimal usage if no arguments
    if len(sys.argv) == 1:
        print(f"{Fore.LIGHTCYAN_EX}Usage:{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}sudo ./pymac.py [options]{Style.RESET_ALL}")
        if os.name != 'nt' and os.geteuid() != 0:
            print(f"{Fore.LIGHTRED_EX}❌ [!] PyMac: This script requires root/sudo privileges for most operations!{Style.RESET_ALL}")
        sys.exit(0)

    system = platform.system()
    if system != 'Windows':
        check_root()
    else:
        print(f"{Fore.LIGHTBLUE_EX}[!] Limited functionality on Windows. Some operations may not work.{Style.RESET_ALL}")

    if args.list:
        print(f"{Fore.LIGHTCYAN_EX}🔍 Detected network interfaces:{Style.RESET_ALL}")
        for iface in list_interfaces():
            print(f"  {Fore.LIGHTGREEN_EX}• {iface}{Style.RESET_ALL}")
        sys.exit(0)

    if not args.iface:
        print(f"{Fore.LIGHTRED_EX}❌ [!] Please specify the network interface with --iface or -i{Style.RESET_ALL}")
        sys.exit(1)

    iface = args.iface
    current_mac = get_current_mac(iface)
    if not current_mac:
        print(f"{Fore.LIGHTRED_EX}❌ [!] PyMac: Could not get the current MAC address of interface '{iface}'.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}💡 Tip: Use '-l' or '--list' to see available interfaces and check your spelling.{Style.RESET_ALL}")
        sys.exit(1)

    if args.show:
        print(f"{Fore.LIGHTCYAN_EX}🔎 Current MAC of {iface}: {Fore.LIGHTGREEN_EX}{current_mac}{Style.RESET_ALL}")
        sys.exit(0)

    if args.random:
        new_mac = generate_mac()
        print(f"{Fore.LIGHTCYAN_EX}🎲 Generating new random MAC: {Fore.LIGHTGREEN_EX}{new_mac}{Style.RESET_ALL}")
        change_mac(iface, new_mac)
        sys.exit(0)

    if args.set:
        if not is_valid_mac(args.set):
            print(f"{Fore.LIGHTRED_EX}❌ [!] Invalid MAC: {args.set}{Style.RESET_ALL}")
            sys.exit(1)
        change_mac(iface, args.set)
        sys.exit(0)

    if args.restore:
        if restore_mac(iface):
            print(f"{Fore.LIGHTGREEN_EX}✅ [+] PyMac: Restoration complete!{Style.RESET_ALL}")
        sys.exit(0)

    if args.funny:
        funny_macs = [
            'DE:AD:BE:EF:00:01',
            'CA:FE:BA:BE:00:13',
            'BA:DB:EE:F0:0D:42',
            'FA:CE:B0:0C:12:34',
            'C0:FF:EE:00:BA:BE',
            'AB:BA:AB:BA:AB:BA',
            '12:34:56:78:9A:BC',
            'FE:ED:FA:CE:BE:EF',
            'BE:EF:DE:AD:FA:CE',
            '00:11:22:33:44:55',
            'AA:BB:CC:DD:EE:FF',
            '01:23:45:67:89:AB',
            'BA:DC:0F:FE:ED:00',
            'DE:CA:F1:ED:00:01',
            'AC:AB:AD:1D:EA:5E',
        ]
        funny_mac = random.choice(funny_macs)
        print(f"{Fore.LIGHTCYAN_EX}🦄 Generating funny MAC: {Fore.LIGHTGREEN_EX}{funny_mac}{Style.RESET_ALL}")
        change_mac(iface, funny_mac)
        sys.exit(0)

    if args.log:
        print(f"{Fore.LIGHTGREEN_EX}📝 [+] PyMac: Logging enabled at {LOG_FILE}{Style.RESET_ALL}")
        log_event(f"PyMac: Script executed with arguments: {sys.argv}")

if __name__ == "__main__":
    main()
