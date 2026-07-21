# Assignment 8 – Scalable & Reliable GUI-Based Multi-Client Chat Application

## Overview

This project is an enhanced version of **Assignment 7**, focusing on improving the scalability, reliability, security, and maintainability of a GUI-based TCP Multi-Client Chat Application.

The application follows a **Client-Server Architecture** using **Python Socket Programming** and was tested using the **Mininet Network Emulator**.

---

# Objectives

The primary goals of this assignment are to:

- Improve scalability for multiple concurrent users
- Enhance connection reliability
- Implement automatic reconnection
- Improve resource and session management
- Introduce dynamic configuration management
- Evaluate application performance
- Strengthen application security

---

# Learning Outcomes

After completing this project, the following concepts were implemented:

- Client-Server Architecture
- TCP Socket Programming
- Thread Pool Optimization
- Connection & Session Management
- Automatic Reconnection
- Dynamic Configuration
- Performance Benchmarking
- Secure Authentication
- Wireshark Packet Analysis

---

# Technology Stack

- Python 3.x
- Socket Programming (TCP)
- Tkinter GUI
- Threading
- ThreadPoolExecutor
- JSON
- CSV
- SHA-256 Password Hashing
- Mininet
- Wireshark

---

# Project Structure

```
Assignment8/
│
├── server.py
├── client_gui.py
├── config.json
├── users.csv
├── chat_history.csv
├── security_log.txt
├── performance_results.csv
│
├── graphs/
│   ├── delay.png
│   ├── throughput.png
│   ├── cpu_usage.png
│   └── memory_usage.png
│
├── screenshots/
├── report.pdf
├── handwritten_reflection.pdf
└── README.md
```

---

# Features

## Authentication

- Username & Password Login
- Automatic User Registration
- SHA-256 Password Hashing
- Duplicate Login Prevention
- Failed Login Protection
- Account Lockout

---

## Messaging

- Broadcast Messaging
- Private Messaging
- Online User List
- Chat History Recovery

### Supported Commands

```text
/list
```

Display all online users.

```text
/msg <username> <message>
```

Send a private message.

```text
/logout
```

Logout gracefully.

---

# Assignment Tasks

## Task 1 – Connection Management

Implemented:

- TCP KeepAlive
- Automatic Disconnection Detection
- Resource Cleanup
- Socket Cleanup
- Inactivity Monitoring
- Graceful Client Removal
- Dashboard Updates

Client Features:

- Graceful Logout
- Automatic GUI Reset
- Proper Socket Closure

---

## Task 2 – Reliability Enhancement

### Automatic Reconnection

- Maximum 3 Retry Attempts
- Configurable Retry Delay
- Automatic Re-authentication
- Receiver Thread Restart

### Graceful Shutdown

Server:

- Notify Connected Clients
- Close All Sockets
- Clear Active Sessions

Client:

- Send `/logout`
- Close Socket Safely

### Timeout Handling

- Connection Timeout
- Socket Timeout
- Inactivity Timeout

### Exception Handling

Handled exceptions include:

- ConnectionResetError
- ConnectionAbortedError
- socket.timeout
- socket.error
- Authentication Errors
- Unexpected Exceptions

---

## Task 3 – Scalability Enhancement

### ThreadPoolExecutor

Instead of creating one thread per client, the server uses:

```python
ThreadPoolExecutor(max_workers=MAX_WORKERS)
```

Benefits:

- Better CPU Utilization
- Lower Memory Consumption
- Controlled Thread Creation
- Stable Under Heavy Load

### Snapshot Broadcast

Broadcast operations use client snapshots to reduce lock contention and improve scalability.

### Successfully Tested

- 5 Clients
- 8 Clients
- 10 Clients

without crashes.

---

## Task 4 – Configuration Management

All configurable values are stored inside:

```text
config.json
```

Includes:

### Network

- Host
- Port
- Worker Threads
- Queue Backlog

### Security

- Lockout Limit
- Lockout Duration
- Timeout
- Rate Limit
- Maximum Message Length

### Storage

- User Credentials
- Chat History
- Security Logs

If the configuration file is missing, it is automatically generated with default values.

---

## Task 5 – Performance Evaluation

Performance metrics collected:

- Delay
- Throughput
- CPU Usage
- Memory Usage

Results are stored in:

```text
performance_results.csv
```

Generated Graphs:

- Delay
- Throughput
- CPU Usage
- Memory Usage

---

## Task 6 – Wireshark Verification

Verified:

- TCP Three-Way Handshake
- Authentication Packets
- Chat Messages
- Private Messages
- Graceful Disconnect
- TCP FIN Packets

---

## Task 7 – GitHub Update

The Assignment 7 repository was updated with Assignment 8 enhancements.

Repository naming convention:

```text
ISEA-Phase3-TezpurUniversity-<RepositoryName>
```

---

## Task 8 – Handwritten Reflection

Included:

- Optimization with greatest improvement
- Importance of scalability
- Reliability challenges
- Most difficult optimization
- Future improvements for 100+ users

---

# Security Features

- SHA-256 Password Hashing
- Username Validation
- Input Sanitization
- HTML Escaping
- Protocol Delimiter Protection
- Security Logging

---

# Rate Limiting

Implemented anti-spam protection.

Users exceeding the configured message rate are temporarily throttled.

---

# Logging

The application maintains:

- User Credentials
- Chat History
- Security Logs

---

# Server Dashboard

Displays:

- Active Clients
- Messages Processed
- Broadcast Count
- Private Message Count

---

# Network Setup

Create Mininet topology:

```bash
sudo mn --topo single,11
```

Server IP:

```text
10.0.0.1
```

---

# Running the Application

## Start Server

```bash
python3 server.py
```

## Start Client

```bash
python3 client_gui.py
```

Open multiple terminals and login using your username and password.

New users are automatically registered.

---

# Performance Comparison

| Feature | Assignment 7 | Assignment 8 |
|----------|--------------|--------------|
| Thread per Client | ✔ | ThreadPoolExecutor |
| Configuration File | ❌ | ✔ |
| Auto Reconnect | ❌ | ✔ |
| Graceful Shutdown | Partial | ✔ |
| Connection Cleanup | Basic | Improved |
| Resource Management | Basic | Improved |
| Performance Evaluation | ❌ | ✔ |
| Graph Generation | ❌ | ✔ |
| Rate Limiting | ❌ | ✔ |
| Input Validation | Basic | Improved |
| TCP KeepAlive | ❌ | ✔ |
| Snapshot Broadcast | ❌ | ✔ |
| Dynamic Configuration | ❌ | ✔ |

---

# Expected Output

The server should:

- Accept multiple concurrent clients
- Broadcast messages
- Support private messaging
- Recover from failures
- Handle disconnects gracefully
- Reject invalid inputs
- Maintain security logs
- Successfully support up to 10 concurrent users

---

# Future Enhancements

- Async I/O using asyncio
- Non-blocking Sockets
- TLS/SSL Encryption
- SQLite/MySQL/PostgreSQL Integration
- Redis Session Management
- Docker Deployment
- Kubernetes Support
- Distributed Server Architecture
- Load Balancing

---

# Conclusion

This assignment successfully transformed the original GUI-based TCP Chat Application into a more **scalable**, **secure**, **reliable**, and **maintainable** system. Features such as **ThreadPoolExecutor**, **automatic reconnection**, **dynamic configuration**, **enhanced security**, **connection management**, and **performance evaluation** significantly improved the application's robustness. The system was successfully tested with **10 concurrent clients** using **Mininet**, demonstrating stable performance and improved software quality.
