import socket
import threading
import datetime
import csv
import os

# Network Setup Configuration
HOST = '0.0.0.0'
PORT = 5000 

client_lock = threading.Lock()
stats_lock = threading.Lock()

# Task 1: Complete Client Profiles State Store
# Structure: {username: {"socket": sock, "ip": ip, "port": port, "login_time": time, "status": "ONLINE"}}
clients = {}  

# Task 1: Required Server Metrics Tracker
server_stats = {
    "messages_processed": 0,
    "broadcast_messages": 0,
    "private_messages": 0
}

HISTORY_FILE = "chat_history.csv" 

def init_csv_stores():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "sender", "receiver", "message_type", "message"])

def log_chat_event(sender, receiver, msg_type, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, sender, receiver, msg_type, message])
    except Exception as e:
        print(f"[-] CSV Logging Error: {e}")

def fetch_historical_catchup(username):
    records = []
    if not os.path.exists(HISTORY_FILE):
        return records
    try:
        with open(HISTORY_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == "timestamp":
                    continue
                if len(row)>=5 and row[1]==username:
                    records.append(f"[{row[0]}] To {row[2]}: {row[4]}")
    except Exception as e:
        print(f"[-]Error reading history  for {username}: {e}")
        
    return records[-5:]

def update_and_display_dashboard():
    """Task 1: Renders the mandatory server live statistics dashboard"""
    with client_lock:
        active_count = sum(1 for c in clients.values() if c["status"] == "ONLINE")
    with stats_lock:
        print("\n========== SERVER STATISTICS ==========")
        print(f"Connected Users    : {active_count}")
        print(f"Messages Processed : {server_stats['messages_processed']}")
        print(f"Broadcast Messages : {server_stats['broadcast_messages']}")
        print(f"Private Messages   : {server_stats['private_messages']}")
        print("=======================================\n")

def broadcast_system_message(text_content, exclude_user=None):
    with client_lock:
        for user, metadata in clients.items():
            if metadata["status"] == "ONLINE" and user != exclude_user:
                try:
                    metadata["socket"].sendall(text_content.encode('utf-8'))
                except Exception:
                    pass

def handle_client_worker(client_socket, client_address):
    ip, port = client_address
    username = None
    
    try:
        username_payload = client_socket.recv(1024).decode('utf-8').strip()
        if not username_payload:
            client_socket.close()
            return
        
        username = username_payload
        login_time = datetime.datetime.now().strftime("%H:%M:%S")


        # Phase 2: Historical Catchup Data Fetching (Task 4)
        historical_payload = fetch_historical_catchup(username)
        
        # ADD THIS LINE TO DEBUG:
        print(f"DEBUG: Found {len(historical_payload)} past messages for {username}")
        
        # Task 1: Complete state registration
        with client_lock:
            clients[username] = {
                "socket": client_socket,
                "ip": ip,
                "port": port,
                "login_time": login_time,
                "status": "ONLINE"
            }
            
        welcome_banner = f"\n[SERVER] Connected successfully as '{username}' from {ip}:{port}\n"
        if historical_payload:
            welcome_banner += "--- Your Last 5 Sent Messages (State Recovered) ---\n" + "\n".join(historical_payload) + "\n-------------------------------------------------\n"
        client_socket.sendall(welcome_banner.encode('utf-8'))
        
        # Task 1: Broadcast Join Notification
        print(f"CONNECTED : {username}")
        broadcast_system_message(f"[SERVER] {username} joined the chat.", exclude_user=username)
        update_and_display_dashboard()
        
        while True:
            raw_data = client_socket.recv(4096)
            if not raw_data:
                break
                
            incoming_text = raw_data.decode('utf-8').strip()
            if not incoming_text:
                continue
                
            with stats_lock:
                server_stats["messages_processed"] += 1
                
            if incoming_text == '/list':
                with client_lock:
                    active_list = [u for u, m in clients.items() if m["status"] == "ONLINE"]
                response = f"[Online System Users]: " + ", ".join(active_list)
                client_socket.sendall(response.encode('utf-8'))
                
            elif incoming_text.startswith('/msg '):
                parts = incoming_text.split(' ', 2)
                if len(parts) < 3:
                    client_socket.sendall("[System Error] Syntax: /msg <username> <message>".encode('utf-8'))
                    continue
                target, secret_msg = parts[1], parts[2]
                
                with client_lock:
                    is_online = target in clients and clients[target]["status"] == "ONLINE"
                    
                if is_online:
                    with client_lock:
                        clients[target]["socket"].sendall(f"[Private from {username}]: {secret_msg}".encode('utf-8'))
                    log_chat_event(username, target, "private", secret_msg)
                    with stats_lock:
                        server_stats["private_messages"] += 1
                else:
                    client_socket.sendall(f"[System Error] User '{target}' does not exist or is offline.".encode('utf-8'))
            
            else:
                broadcast_system_message(f"[{username}]: {incoming_text}", exclude_user=username)
                log_chat_event(username, "ALL", "broadcast", incoming_text)
                with stats_lock:
                    server_stats["broadcast_messages"] += 1
                    
            update_and_display_dashboard()
            
    except Exception as e:
        print(f"[-] Processing exception on user '{username if username else ip}': {e}")
    finally:
        # Task 1 Graceful State Disconnection & Leave Handlers
        if username:
            with client_lock:
                if username in clients:
                    clients[username]["status"] = "OFFLINE"
            
            print(f"DISCONNECTED : {username}")
            broadcast_system_message(f"[SERVER] {username} left the chat.")
            log_chat_event(username, "Server", "system_leave", f"{username} disconnected.")
            update_and_display_dashboard()
            
        client_socket.close()

def main():
    init_csv_stores()
    engine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    engine.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        engine.bind((HOST, PORT))
        engine.listen(15)
        print(f"Server listening on {PORT}")
        
        while True:
            sock, addr = engine.accept()
            worker = threading.Thread(target=handle_client_worker, args=(sock, addr), daemon=True)
            worker.start()
            
    except KeyboardInterrupt:
        print("\n[*] Server terminating safely.")
    finally:
        engine.close()

if __name__ == "__main__":
    main()