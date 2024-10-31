import re
import requests
from collections import defaultdict

# Path to the log file
log_path = 'C:/Users/Acer/Documents/MSIB/Code/auth.txt'

# Fungsi untuk mengekstrak alamat IP dari file log
def extract_ips(log_path):
    with open(log_path, 'r') as file:
        log_data = file.read()
    # Ekstrak IP menggunakan regex
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ip_list = re.findall(ip_pattern, log_data)
    return list(set(ip_list))  # Menghapus IP duplikat

# Fungsi untuk mendapatkan lokasi negara dari alamat IP menggunakan API
def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data.get("country", "Unknown")
    except Exception as e:
        return "Error"

# Fungsi untuk mengelompokkan IP berdasarkan negara
def group_ips_by_country(ip_list):
    country_ips = defaultdict(list)
    for ip in ip_list:
        country = get_ip_location(ip)
        country_ips[country].append(ip)
    return country_ips

# Jalankan program
ip_list = extract_ips(log_path)
grouped_ip_locations = group_ips_by_country(ip_list)

# Menampilkan hasil IP dan negara secara terurut
for country, ips in sorted(grouped_ip_locations.items()):
    print(f"{country}:")
    for ip in ips:
        print(f"  - {ip}")
