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
├── server.py              # Secure TCP Server
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