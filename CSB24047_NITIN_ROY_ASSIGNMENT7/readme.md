# Assignment 7: Secure Network Application Development Using TCP

## 📌 Overview

This project is an extension of the multi-client TCP chat application developed in Assignment 6. The primary objective of this assignment was to enhance the application by implementing practical security mechanisms while maintaining the existing client-server architecture.

The application follows a **Client-Server architecture** using **Python TCP sockets** and provides a GUI-based chat client developed with **Tkinter**. Several security features have been integrated, including authentication, secure password storage, session management, duplicate login prevention, input validation, and secure logging.

---

## 🎯 Assignment Objectives

The following security features were implemented as required:

- User Authentication
- Secure Password Storage using SHA-256
- Duplicate Login Prevention
- Input Validation
- Failed Login Protection
- Session Management
- Secure Logging
- Wireshark Verification Support

---

# Project Structure

```
.
├── server.py    a# Assignment 8 – Scalable and Reliable GUI-Based Multi-Client Chat Application

**Course:** ISEA Phase 3 – Tezpur University  
**Assignment:** Assignment 8  
**Student:** <Your Name>  
**Roll No.:** <Your Roll Number>

---

# Overview

This assignment is an enhancement of **Assignment 7**. Instead of developing a new application, the existing GUI-based TCP multi-client chat application has been improved by focusing on:

- Scalability
- Reliability
- Connection Management
- Configuration Management
- Performance Evaluation
- Software Quality

The application follows a **Client-Server Architecture** using **Python Socket Programming** and was tested in the **Mininet network emulator**.

---

# Assignment Objectives

The primary objective of this assignment is to improve the existing chat application by:

- Supporting more concurrent users
- Improving fault tolerance
- Handling unexpected disconnections
- Managing resources efficiently
- Making configuration dynamic
- Evaluating performance before and after optimization

---

# Learning Outcomes

After completing this assignment, the following concepts were implemented and understood:

- Scalable client-server architecture
- Reliable socket communication
- Dynamic configuration management
- Thread optimization
- Resource cleanup
- Automatic reconnection
- Performance benchmarking
- Wireshark TCP analysis

---

# Technology Stack

- Python 3.x
- Socket Programming
- Threading
- ThreadPoolExecutor
- Tkinter GUI
- JSON
- CSV
- SHA-256 Hashing
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
│
├── report.pdf
├── handwritten_reflection.pdf
└── README.md
```

---

# Network Setup

The application was tested using Mininet.

Create topology:

```bash
sudo mn --topo single,11
```

Server IP

```
10.0.0.1
```

Concurrent clients tested

- 5 Clients
- 8 Clients
- 10 Clients

---

# Running the Application

## Start Server

```bash
python3 server.py
```

---

## Start Client

Open multiple terminals.

```bash
python3 client_gui.py
```

Login using

- Username
- Password

New users are automatically registered.

---

# Features

## Authentication

- Username & password authentication
- Automatic registration
- Password hashing using SHA-256
- Duplicate login prevention

---

## Messaging

Supports

- Broadcast messaging
- Private messaging
- Online user list
- Chat history recovery

Commands

```
/list
```

Shows online users.

```
/msg <username> <message>
```

Private messaging.

```
/logout
```

Gracefully disconnects.

---

# Assignment Tasks

---

# Task 1 – Connection Management

Implemented Features

- Automatic disconnected client detection
- TCP KeepAlive enabled
- Inactive client removal
- Resource cleanup
- Socket cleanup
- Meaningful error messages
- Dashboard updates
- Automatic removal from active client list

Implementation

Server

- TCP KeepAlive
- Inactivity monitoring thread
- Resource cleanup inside `finally`
- Active client removal
- Rate-limit cleanup

Client

- Graceful logout
- Graceful window close
- Automatic GUI reset after disconnect

---

# Task 2 – Reliability Enhancement

Implemented Features

### Automatic Reconnection

The client automatically reconnects after an unexpected disconnection.

Features

- Maximum 3 retries
- Retry delay
- Automatic authentication
- Receiver thread restart

---

### Graceful Shutdown

Server

- Notifies all clients
- Closes sockets
- Clears active sessions

Client

- Sends `/logout`
- Closes socket safely

---

### Timeout Handling

Implemented

- Socket timeout
- Inactivity timeout
- Connection timeout

---

### Better Exception Handling

Improved handling for

- ConnectionResetError
- ConnectionAbortedError
- socket.timeout
- socket.error
- Invalid authentication
- Duplicate login
- Unexpected exceptions

---

# Task 3 – Scalability Enhancement

The original Assignment 7 used:

- One thread per client

Assignment 8 improves scalability using:

## ThreadPoolExecutor

Instead of creating unlimited threads, the server now uses

```python
ThreadPoolExecutor(max_workers=MAX_WORKERS)
```

Benefits

- Controlled thread creation
- Lower memory usage
- Better CPU utilization
- Stable under heavy load

---

## Snapshot Broadcast

Broadcast now creates a snapshot of active clients before sending messages.

Benefits

- Reduced lock contention
- Better scalability
- Faster broadcasts

---

## Duplicate Login Prevention

Only one active session per username is allowed.

---

## Successfully Tested

- 5 Clients
- 8 Clients
- 10 Clients

without crashes.

---

# Task 4 – Configuration Management

All configurable values were moved into

```
config.json
```

No hardcoded values remain.

Configurable settings include

Network

- Host
- Port
- Worker threads
- Queue backlog

Security

- Lockout limit
- Lockout duration
- Timeout
- Rate limit
- Maximum message length

Storage

- Chat history
- User credentials
- Security logs

If `config.json` is missing, the server automatically creates one using default values.

---

# Task 5 – Performance Evaluation

Performance was compared before and after optimization.

Metrics

- Delay
- Throughput
- CPU Usage
- Memory Usage

Results are stored in

```
performance_results.csv
```

Graphs are generated in

```
graphs/
```

Graphs include

- Delay Graph
- Throughput Graph
- CPU Usage Graph
- Memory Usage Graph

---

# Task 6 – Wireshark Verification

TCP communication was captured using Wireshark.

Verified

- TCP Three-Way Handshake
- Authentication packets
- Chat messages
- Private messages
- Graceful disconnect
- FIN packets

---

# Task 7 – GitHub Update

The Assignment 7 repository was updated instead of creating a new repository.

Naming convention

```
ISEA-Phase3-TezpurUniversity-<RepositoryName>
```

Git history documents all improvements made for Assignment 8.

---

# Task 8 – Handwritten Reflection

The following questions were answered manually.

1. Which optimization produced the greatest improvement?

2. Why is scalability important?

3. What reliability issues did you discover?

4. Which optimization was the most difficult?

5. What additional improvements are required to support 100 users?

Scanned copy included as

```
handwritten_reflection.pdf
```

---

# Additional Improvements Implemented

Besides the required assignment tasks, the following enhancements were implemented.

## Security

- SHA-256 password hashing
- Username validation
- Input sanitization
- HTML escaping
- Protocol delimiter protection
- Security logging

---

## Rate Limiting

Implemented anti-spam protection.

Users exceeding the configured message rate are temporarily throttled.

---

## Login Protection

Implemented

- Failed login tracking
- Account lockout
- Lockout timer

---

## Message Validation

Implemented

- Maximum message length
- Invalid command rejection
- Empty password rejection

---

## Logging

Maintains

- Chat history
- Security log
- User credentials

---

## Dashboard

Server dashboard displays

- Active clients
- Messages processed
- Broadcast count
- Private message count

---

# Comparison Between Assignment 7 and Assignment 8

| Feature | Assignment 7 | Assignment 8 |
|----------|--------------|--------------|
| Thread per Client | ✔ | Improved using ThreadPoolExecutor |
| Configuration File | ❌ | ✔ config.json |
| Auto Reconnect | ❌ | ✔ |
| Graceful Shutdown | Partial | ✔ |
| Connection Cleanup | Basic | Improved |
| Resource Management | Basic | Improved |
| Performance Evaluation | ❌ | ✔ |
| Graph Generation | ❌ | ✔ |
| Rate Limiting | ❌ | ✔ |
| Input Sanitization | ❌ | ✔ |
| HTML Escaping | ❌ | ✔ |
| TCP KeepAlive | ❌ | ✔ |
| Snapshot Broadcast | ❌ | ✔ |
| Duplicate Login Protection | ✔ | Improved |
| Dynamic Configuration | ❌ | ✔ |

---

# Expected Output

The server should

- Accept multiple concurrent clients
- Support private messaging
- Broadcast messages
- Handle disconnects gracefully
- Recover from failures
- Reject invalid input
- Maintain security logs
- Handle 10 concurrent users without crashing

---

# Future Improvements

To support more than 100 concurrent users, the following improvements can be implemented:

- Async I/O using asyncio
- Event-driven networking
- Non-blocking sockets
- Database integration (SQLite/MySQL/PostgreSQL)
- TLS/SSL encryption
- Load balancing
- Redis for session management
- Distributed server architecture
- Docker deployment
- Kubernetes orchestration

---

# Conclusion

This assignment successfully enhanced the Assignment 7 chat application into a more scalable, reliable, and maintainable system. The implementation includes improved connection management, automatic reconnection, graceful shutdown, dynamic configuration using `config.json`, optimized thread management through `ThreadPoolExecutor`, enhanced security mechanisms, and comprehensive performance evaluation. The application was successfully tested with up to **10 concurrent clients** in Mininet, demonstrating improved stability and software quality while maintaining the original communication protocol.

---          # Secure TCP Server
├── client_gui.py          # GUI Client Application
├── users.csv              # Stores usernames and hashed passwords
├── chat_history.csv       # Chat history
├── security_log.txt       # Security event logs
├── screenshots/           # Assignment screenshots
├── report.pdf             # Assignment report
└── README.md
```

---

# Technologies Used

- Python 3
- Socket Programming (TCP)
- Tkinter GUI
- Threading
- CSV Storage
- SHA-256 Password Hashing (`hashlib`)
- Mininet
- Wireshark

---

# Features Implemented

## ✅ Task 1 – User Authentication

The application now requires users to log in using a username and password before joining the chat.

### Implementation

- Login GUI with username and password fields
- Password field masks user input
- Server authenticates every client
- New users are automatically registered
- Existing users must provide the correct password

---

## ✅ Task 2 – Secure Password Storage

Passwords are **never stored in plaintext**.

### Implementation

- Passwords are hashed using SHA-256 before storage.
- Only the hash value is stored inside `users.csv`.
- Authentication compares password hashes instead of actual passwords.

Example:

```
username,password_hash
alice,3d8d81a4c2...
```

---

## ✅ Task 3 – Duplicate Login Prevention

To improve account security, the same user cannot log in from multiple devices simultaneously.

### Implementation

The server maintains active sessions in memory.

If a user is already logged in:

- Login request is rejected
- Appropriate authentication failure message is returned
- Security event is logged

---

## ✅ Task 4 – Input Validation

Several validation rules were added to prevent invalid or malicious input.

### Username Validation

- 3–15 characters
- Letters
- Numbers
- Underscore only

### Password Validation

- Empty passwords are rejected.

### Message Validation

Oversized messages (>1000 characters) are rejected.

### Command Validation

Only supported commands are accepted:

- `/list`
- `/msg`
- `/logout`

Unsupported commands are blocked and logged.

---

## ✅ Task 5 – Failed Login Protection

To reduce brute-force attacks, failed login attempts are monitored.

### Rules

- Maximum of 5 failed attempts
- Account locked for 5 minutes
- Lockout timer automatically expires

All failed attempts are recorded in the security log.

---

## ✅ Task 6 – Session Management & Secure Logging

### Logout Support

Users can safely terminate their session using:

```
/logout
```

or by clicking the Logout button.

---

### Inactivity Timeout

Inactive users are automatically disconnected after the configured timeout period.

The server continuously monitors user activity using a background thread.

---

### Secure Logging

Security-related events are recorded inside:

```
security_log.txt
```

Logged events include:

- Successful login
- Failed login
- Duplicate login attempts
- Session timeout
- User logout
- Invalid usernames
- Oversized messages
- Unsupported commands

Passwords are **never logged**.

---

# Additional Features

Besides the required security tasks, the application also supports:

- Multi-client chat
- Private messaging
- Online user list
- Chat history storage
- Automatic registration for new users
- Dashboard showing server statistics
- Broadcast messaging
- Thread-safe client management

---

# Server Dashboard

The server continuously displays runtime statistics such as:

- Active connections
- Messages processed
- Broadcast messages
- Private messages

This helps monitor server activity during execution.

---

# Communication Flow

```
Client
   │
   │ Login Request
   ▼
Server
   │
Authenticate User
   │
   ├── Success
   │      │
   │      ▼
   │  Join Chat
   │
   └── Failure
          │
          ▼
 Authentication Failed
```

---

# Security Workflow

```
User Login
      │
      ▼
Input Validation
      │
      ▼
Password Hashing
      │
      ▼
Authentication
      │
      ├── Failed
      │      │
      │      ▼
      │ Increase Failed Counter
      │
      ├── Locked
      │      │
      │      ▼
      │ Reject Login
      │
      └── Success
             │
             ▼
 Duplicate Login Check
             │
             ▼
 Create Session
             │
             ▼
 Allow Chat Access
```

---

# Running the Project

## Start Server

```bash
python server.py
```

---

## Start Client

```bash
python client_gui.py
```

Run multiple clients from different Mininet hosts to test multi-user communication.

---

# Testing Performed

The application was tested for the following scenarios:

- Successful login
- New user registration
- Incorrect password
- Duplicate login prevention
- Empty password rejection
- Invalid username rejection
- Oversized message rejection
- Unsupported command rejection
- Private messaging
- Broadcast messaging
- Logout
- Session timeout
- Multiple simultaneous clients

---

# Wireshark Verification

The application supports packet capture using Wireshark.

Suggested filter:

```
tcp.port == 5000
```

Captured events include:

- Login request
- Failed authentication
- Successful authentication
- Chat communication
- Logout
- Session timeout

---

# Learning Outcomes

This assignment provided practical experience with:

- TCP socket programming
- Secure client-server communication
- Authentication systems
- Password hashing
- Session management
- Input validation
- Concurrent programming using threads
- Security logging
- Network traffic analysis using Wireshark

---

# Conclusion

This assignment successfully enhanced the original TCP chat application by incorporating essential application-level security features. Secure authentication, SHA-256 password hashing, duplicate login prevention, input validation, session timeout handling, and comprehensive security logging significantly improved the overall robustness of the system while preserving the existing networking architecture. The project demonstrates the practical implementation of secure software development principles in a real-world client-server application.