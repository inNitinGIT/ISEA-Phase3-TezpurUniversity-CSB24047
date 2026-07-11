# GUI-Based Multi-Client Chat Application Using TCP

A Python-based **GUI chat application** that allows multiple clients to communicate over a TCP network. The project reuses the networking logic from Assignment 5 and replaces the terminal client with a graphical interface built using **Tkinter**.

---

## Project Objective

The goal of this project is to:

- Convert the terminal-based TCP chat client into a GUI application.
- Reuse the existing TCP server implementation.
- Learn GUI programming using Tkinter.
- Handle multiple clients using threads.
- Keep the networking logic separate from the GUI.

---

## Features

### Server
- Accepts multiple client connections.
- Broadcast messaging.
- Private messaging.
- Tracks online users.
- Stores chat history in a CSV file.
- Displays live server statistics.
- Join and leave notifications.

### Client (GUI)
- Simple login window.
- Chat window with scrollable messages.
- Send messages using a button or Enter key.
- Online users list.
- Private messaging by selecting a user.
- Disconnect button.
- Background thread for receiving messages without freezing the GUI.

---

## Technologies Used

- Python 3
- Socket Programming
- Tkinter
- Threading
- CSV
- Mininet
- Wireshark (for packet verification)

---

## Project Structure

```
.
├── server.py
├── client_gui.py
├── chat_history.csv
├── screenshots/
│   ├── login.png
│   ├── chat_window.png
│   ├── broadcast.png
│   ├── private_message.png
│   └── ...
├── report.pdf
└── README.md
```

---

## Network Topology

The application is tested using **Mininet**.

```
h1  ---> Chat Server

h2  ---> Client A
h3  ---> Client B
h4  ---> Client C
h5  ---> Client D
```

Start Mininet:

```bash
sudo mn --topo single,5
```

Verify the network:

```bash
nodes
net
pingall
```

---

## How to Run

### Step 1: Start the Server

On **h1**

```bash
python3 server.py
```

---

### Step 2: Start Clients

On each client (h2, h3, h4, h5)

```bash
python3 client_gui.py
```

---

### Step 3: Login

- Enter a username.
- Click **Connect**.

The chat window will open after a successful connection.

---

## Messaging

### Broadcast Message

Simply type a message and click **Send**.

Everyone connected to the server will receive it.

---

### Private Message

1. Select a user from the **Online Users** list.
2. Type your message.
3. Click **Send**.

The message will only be delivered to the selected user.

---

## Server Statistics

The server continuously displays:

- Connected users
- Total messages processed
- Broadcast messages
- Private messages

---

## Chat History

The server stores chat history in:

```
chat_history.csv
```

Each record contains:

- Timestamp
- Sender
- Receiver
- Message type
- Message

---

## GUI Components

The client interface includes:

- Login screen
- Username input
- Chat display
- Scrollable message area
- Online users list
- Message input box
- Send button
- Disconnect button

---

## Testing

The project was tested with multiple clients connected simultaneously.

The following features were verified:

- User login
- Multiple client connections
- Broadcast messaging
- Private messaging
- Online user updates
- User join notifications
- User leave notifications
- Client disconnection

---

## Wireshark Verification

Traffic was captured using:

```
tcp.port == 5000
```

The capture verifies:

- Client connection
- Broadcast messages
- Private messages
- Client disconnection

---

## Components Reused from Assignment 5

The following networking features were reused:

- TCP socket communication
- Multi-client server
- Broadcast messaging
- Private messaging
- Chat history logging
- Client management
- Thread handling

Only the client interface was changed from terminal-based to GUI.

---

## Future Improvements

Some possible enhancements include:

- User authentication
- Encrypted communication
- File sharing
- Group chat
- Emoji support
- Message timestamps in the GUI
- Better UI design
- Dark mode

---

## Author

**Name:** *Nitin Roy*

**Course:**Isea Networking Internship

**Assignment:** GUI-Based Multi-Client Chat Application Using TCP