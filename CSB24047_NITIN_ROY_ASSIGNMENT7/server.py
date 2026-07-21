import socket
import threading
import datetime
import csv
import os
import hashlib
import re
import time

# Network Setup Configuration
HOST = '0.0.0.0'
PORT = 5000 

client_lock = threading.Lock()
stats_lock = threading.Lock()

# Task 1: Complete Client Profiles State Store
# Structure: {username: {"socket": sock, "ip": ip, "port": port, "login_time": time, "status": "ONLINE", "last_activity": datetime}}
clients = {}  

# Task 1: Required Server Metrics Tracker
server_stats = {
    "messages_processed": 0,
    "broadcast_messages": 0,
    "private_messages": 0
}

HISTORY_FILE = "chat_history.csv" 
CREDENTIALS_FILE = "users.csv"
SECURITY_LOG = "security_log.txt"

# Task 5 & 6 Configuration Rules
LOCKOUT_LIMIT = 5
LOCKOUT_DURATION = datetime.timedelta(minutes=5)
INACTIVITY_TIMEOUT = datetime.timedelta(minutes=5)

# Lockout state databases (in-memory)
failed_attempts = {}  # {username: count}
lockouts = {}         # {username: lockout_expiry_datetime}

def init_csv_stores():
    """Initializes chat histories and user accounts storage safely."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "sender", "receiver", "message_type", "message"])
            
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])

def log_chat_event(sender, receiver, msg_type, message):
    """Logs ordinary chat events to the chat history database."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, sender, receiver, msg_type, message])
    except Exception as e:
        print(f"[-] CSV Logging Error: {e}")

def log_security_event(event_type, username, ip, port, details):
    """Task 6: Write to security_log.txt securely without storing plaintext passwords."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {event_type.upper()} | User: {username} | Host: {ip}:{port} | Info: {details}\n"
    try:
        with open(SECURITY_LOG, mode='a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception as e:
        print(f"[-] Security Log Error: {e}")

def hash_password(password):
    """Task 2: Secure password storage using SHA-256 hashing."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_valid_username(username):
    """Task 4: Alphanumeric constraint on usernames (3-15 characters)."""
    return bool(re.match(r"^[a-zA-Z0-9_]{3,15}$", username))

def authenticate_user(username, password):
    """Handles secure user verification and auto-registration."""
    pwd_hash = hash_password(password)
    users = {}
    
    try:
        with open(CREDENTIALS_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) == 2:
                    users[row[0]] = row[1]
    except Exception as e:
        print(f"[-] Credentials Reading Error: {e}")

    if username in users:
        if users[username] == pwd_hash:
            return "AUTH_SUCCESS"
        else:
            return "AUTH_FAIL"
    else:
        # Register user on the fly if profile doesn't exist
        try:
            with open(CREDENTIALS_FILE, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([username, pwd_hash])
            return "REGISTERED"
        except Exception as e:
            print(f"[-] Registration Error: {e}")
            return "AUTH_ERROR"

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
                if len(row) >= 5 and row[1] == username:
                    records.append(f"[{row[0]}] To {row[2]}: {row[4]}")
    except Exception as e:
        print(f"[-] History Fetch Error: {e}")
        
    return records[-5:]

def update_and_display_dashboard():
    with client_lock:
        active_count = sum(1 for c in clients.values() if c["status"] == "ONLINE")
    with stats_lock:
        print("\n========== SERVER SECURITY DASHBOARD ==========")
        print(f"Active Secure Connections: {active_count}")
        print(f"System Message Load      : {server_stats['messages_processed']}")
        print(f"Global Broadcasts        : {server_stats['broadcast_messages']}")
        print(f"Private Secret Messages  : {server_stats['private_messages']}")
        print("===============================================\n")

def broadcast_system_message(text_content, exclude_user=None):
    with client_lock:
        for user, metadata in list(clients.items()):
            if metadata["status"] == "ONLINE" and user != exclude_user:
                try:
                    metadata["socket"].sendall(text_content.encode('utf-8'))
                except Exception:
                    pass

def inactivity_monitor_thread():
    """Task 6: Periodically scans for inactive TCP clients and times them out."""
    while True:
        time.sleep(10)
        now = datetime.datetime.now()
        timed_out_clients = []
        
        with client_lock:
            for user, metadata in list(clients.items()):
                if metadata["status"] == "ONLINE":
                    if now - metadata["last_activity"] > INACTIVITY_TIMEOUT:
                        timed_out_clients.append((user, metadata["socket"], metadata["ip"], metadata["port"]))
                        
        for user, sock, ip, port in timed_out_clients:
            try:
                sock.sendall("SYSTEM:TIMEOUT:Your session expired due to inactivity.".encode('utf-8'))
                sock.close()
            except Exception:
                pass
            log_security_event("session_timeout", user, ip, port, "Disconnected due to inactivity.")

def handle_client_worker(client_socket, client_address):
    ip, port = client_address
    username = None
    
    #Task 1: enable Tcp keepalive to detect ded connections automatically
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
    try:
        # Handshake Data Check
        auth_payload = client_socket.recv(1024).decode('utf-8').strip()
        if not auth_payload or "||" not in auth_payload:
            client_socket.sendall("AUTH_FAIL:Invalid authentication protocol.".encode('utf-8'))
            client_socket.close()
            return
        
        username_payload, password_payload = auth_payload.split("||", 1)
        
        # Task 4 Input Validation: Username alphanumeric evaluation
        if not is_valid_username(username_payload):
            client_socket.sendall("AUTH_FAIL:Username must be 3-15 characters (alphanumeric only).".encode('utf-8'))
            log_security_event("validation_failed", username_payload, ip, port, "Rejected invalid username format.")
            client_socket.close()
            return
            
        # Task 4 Input Validation: Blank Password evaluation
        if not password_payload.strip():
            client_socket.sendall("AUTH_FAIL:Empty password submitted.".encode('utf-8'))
            log_security_event("validation_failed", username_payload, ip, port, "Rejected empty password attempt.")
            client_socket.close()
            return

        now = datetime.datetime.now()
        
        # Task 5: Failed Login Protection - Check Account Lockouts
        if username_payload in lockouts:
            if now < lockouts[username_payload]:
                remaining_sec = int((lockouts[username_payload] - now).total_seconds())
                client_socket.sendall(f"AUTH_FAIL:Account locked. Please try again in {remaining_sec}s.".encode('utf-8'))
                log_security_event("lockout_blocked", username_payload, ip, port, "Attempt during an active lockout.")
                client_socket.close()
                return
            else:
                # Lockout expired, purge cache
                del lockouts[username_payload]
                failed_attempts[username_payload] = 0

        # Run Verification
        auth_status = authenticate_user(username_payload, password_payload)
        
        if auth_status == "AUTH_FAIL":
            failed_attempts[username_payload] = failed_attempts.get(username_payload, 0) + 1
            attempts_left = LOCKOUT_LIMIT - failed_attempts[username_payload]
            
            log_security_event("failed_login", username_payload, ip, port, f"Incorrect password (Attempt {failed_attempts[username_payload]}/5).")
            
            if failed_attempts[username_payload] >= LOCKOUT_LIMIT:
                lockouts[username_payload] = now + LOCKOUT_DURATION
                log_security_event("account_locked", username_payload, ip, port, "Lockout state activated for 5 minutes.")
                client_socket.sendall("AUTH_FAIL:Too many incorrect attempts. Locked out for 5 minutes.".encode('utf-8'))
            else:
                client_socket.sendall(f"AUTH_FAIL:Incorrect credentials. {attempts_left} attempts remaining.".encode('utf-8'))
                
            client_socket.close()
            return
        
        elif auth_status == "AUTH_ERROR":
            client_socket.sendall("AUTH_FAIL:Server processing credentials error.".encode('utf-8'))
            client_socket.close()
            return
            
        # Task 3: Duplicate Login Prevention
        with client_lock:
            if username_payload in clients and clients[username_payload]["status"] == "ONLINE":
                client_socket.sendall("AUTH_FAIL:User already logged in from another location.".encode('utf-8'))
                log_security_event("duplicate_login_blocked", username_payload, ip, port, "Prevented concurrent active session.")
                client_socket.close()
                return

        # Login Approved - Purge failures and map profile
        username = username_payload
        failed_attempts[username] = 0 
        login_time = datetime.datetime.now().strftime("%H:%M:%S")
        log_security_event("successful_login", username, ip, port, f"Session established successfully ({auth_status}).")

        historical_payload = fetch_historical_catchup(username)
        
        with client_lock:
            clients[username] = {
                "socket": client_socket,
                "ip": ip,
                "port": port,
                "login_time": login_time,
                "status": "ONLINE",
                "last_activity": datetime.datetime.now()
            }
            
        welcome_banner = f"\n[SERVER] Secure connection established as '{username}' from {ip}:{port}\n"
        if historical_payload:
            welcome_banner += "--- Your Last 5 Sent Messages (State Recovered) ---\n" + "\n".join(historical_payload) + "\n-------------------------------------------------\n"
        client_socket.sendall(welcome_banner.encode('utf-8'))
        
        # Broadcast Join Notification
        print(f"CONNECTED : {username}")
        broadcast_system_message(f"JOIN:{username}", exclude_user=username)
        
        # Sync online users listbox right after joining
        with client_lock:
            online_users = [u for u, m in clients.items() if m["status"] == "ONLINE"]
        client_socket.sendall(f"USERLIST:{','.join(online_users)}".encode('utf-8'))
        
        update_and_display_dashboard()
        
        # Keepalive communications thread
        while True:
            raw_data = client_socket.recv(4096)
            if not raw_data:
                break
                
            incoming_text = raw_data.decode('utf-8').strip()
            if not incoming_text:
                continue
                
            # Update user session state for active monitoring
            with client_lock:
                if username in clients:
                    clients[username]["last_activity"] = datetime.datetime.now()
                    
            # Task 4 Input Validation: Oversized Message Block
            if len(incoming_text) > 1000:
                client_socket.sendall("SYSTEM:ERROR Message rejected. Must not exceed 1000 characters.".encode('utf-8'))
                log_security_event("oversized_message_rejected", username, ip, port, f"Rejected oversized message ({len(incoming_text)} characters).")
                continue
                
            # Task 4 Input Validation: Command Validation
            if incoming_text.startswith('/'):
                parts = incoming_text.split()
                command = parts[0]
                if command not in ['/list', '/msg', '/logout']:
                    client_socket.sendall(f"SYSTEM:ERROR Unsupported command '{command}'.".encode('utf-8'))
                    log_security_event("unsupported_command", username, ip, port, f"Attempted execution of unsupported command: {command}")
                    continue

            with stats_lock:
                server_stats["messages_processed"] += 1
                
            if incoming_text == '/list':
                with client_lock:
                    active_list = [u for u, m in clients.items() if m["status"] == "ONLINE"]
                response = f"[Online System Users]: " + ", ".join(active_list)
                client_socket.sendall(response.encode('utf-8'))
                
            # Task 6: Session Management - Client requested logout
            elif incoming_text == '/logout':
                client_socket.sendall("SYSTEM:LOGOUT:Logged out successfully.".encode('utf-8'))
                log_security_event("user_logout", username, ip, port, "User requested regular session termination.")
                break
                
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
    
    except ConnectionResetError:
        print(f"[-] Client {username if username else ip}forcefully disconneted.")
    except Exception as e:
        print(f"[-] Processing exception on user '{username if username else ip}': {e}")
    finally:
        # task 1 : Graceful Disconnection cleanup
        if username:
            with client_lock:
                if username in clients:
                    del clients[username]#fully remove client from state store to release memory
            
            print(f"DISCONNECTED : {username}")
            broadcast_system_message(f"LEAVE:{username}")
            log_chat_event(username, "Server", "system_leave", f"{username} disconnected.")
            update_and_display_dashboard()
        
        try:
            client_socket.close()
        except Exception:
            pass

def main():
    init_csv_stores()
    
    # Run the secure inactivity thread scanner
    monitor = threading.Thread(target=inactivity_monitor_thread, daemon=True)
    monitor.start()
    
    engine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    engine.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        engine.bind((HOST, PORT))
        engine.listen(15)
        print(f"Server is listening on secure TCP Port {PORT}")
        
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