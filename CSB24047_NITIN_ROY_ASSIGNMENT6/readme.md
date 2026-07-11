# GUI-Based Multi-Client Chat Application Using TCP

A Python chat application that lets multiple clients communicate over TCP, using a Tkinter GUI client and a multithreaded TCP server. This project extends the terminal-based chat system from Assignment 5 by replacing the terminal client with a graphical desktop interface, while reusing the server and networking logic unchanged.

**Author:** Nitin Roy
**Roll No:** CSB24047
**Course:** ISEA Networking Internship, Tezpur University
**Assignment:** Assignment 6 – GUI-Based Multi-Client Chat Application Using TCP

---

## Objective

- Convert the terminal-based TCP chat client into a GUI application.
- Reuse the existing TCP server implementation from Assignment 5 with minimal changes.
- Learn GUI programming using Tkinter.
- Handle multiple clients using threads.
- Keep networking logic separate from the GUI.

---

## Features

### Server (`server.py`)
- Accepts multiple client connections, one worker thread per client.
- Broadcast messaging to all online users.
- Private messaging via `/msg <username> <message>`.
- Tracks online/offline user state.
- Logs all chat activity to `chat_history.csv` (timestamp, sender, receiver, type, message).
- Displays a live server statistics dashboard (connected users, messages processed, broadcast/private counts).
- Join and leave notifications broadcast to all clients.

### Client GUI (`client_gui.py`)
- Login window with username entry and Connect button, with input validation.
- Chat window with a scrollable, auto-scrolling message area.
- Online users list — select a user to automatically send a private message.
- Send messages via button click or Enter key.
- Disconnect button for a clean session exit.
- Background thread for receiving messages, so the GUI never freezes while waiting on the network.

---

## Technologies Used

- Python 3
- Socket programming (TCP)
- Tkinter (`tkinter`, `tkinter.scrolledtext`)
- Threading
- CSV (chat history persistence)
- Mininet (network emulation)
- Wireshark (packet-level verification)

---

## Project Structure

```
.
├── server.py
├── client_gui.py
├── chat_history.csv
├── screenshots/
│   ├── loginwindow.png
│   ├── successful_connecting.png
│   ├── mainchat_window.png
│   ├── broadcast_message.png
│   ├── private_message.png
│   ├── client_connection.png
│   ├── user_leaving.png
│   ├── nodes.png
│   ├── net.png
│   └── pingall.png
├── capture.pcapng
├── Assignment6_Report.docx
└── README.md
```

---

## Network Topology

Tested using Mininet with one server host and four client hosts on a single switch:

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

Verify connectivity:

```bash
nodes
net
pingall
```

---

## Execution Steps

**1. Start the server** (on h1):

```bash
python3 server.py
```

**2. Start each client** (on h2, h3, h4, h5):

```bash
python3 client_gui.py
```

**3. Log in:**
- Enter a username in the login window.
- Click **Connect**.
- The chat window opens automatically on a successful connection.

**4. Chat:**
- **Broadcast:** type a message and click **Send** — all connected users receive it.
- **Private message:** select a user from the **Online Users** list, type a message, and click **Send** — only that user receives it.

---

## Implementation Summary

The client and server communicate over a single TCP connection per client on port `5000`. The server (`server.py`) is largely unchanged from Assignment 5: it still accepts connections, spawns a thread per client, tracks state in a shared `clients` dictionary, and logs every event to `chat_history.csv`. The only substantial change is on the client side — `client_gui.py` replaces Assignment 5's `input()`/`print()` terminal loop with Tkinter widgets (login form, scrollable chat log, online-users listbox, message entry, and buttons), and moves message reception into a dedicated background thread so the interface stays responsive while waiting on `socket.recv()`.

---

## Sample Screenshots

| Login Window | Successful Connection | Main Chat Window |
|---|---|---|
| `screenshots/loginwindow.png` | `screenshots/successful_connecting.png` | `screenshots/mainchat_window.png` |

Additional screenshots (broadcast messaging, private messaging, Mininet topology commands, and Wireshark captures for connection/broadcast/private-message/disconnection) are included in the `screenshots/` folder and detailed in `Assignment6_Report.docx`.

---

## Wireshark Verification

Traffic captured with filter:

```
tcp.port == 5000
```

Confirms, at the packet level:
- TCP three-way handshake on client connection
- Server fan-out of a broadcast message to all connected clients
- Point-to-point delivery of a private message to a single client
- FIN/ACK exchange on client disconnection

---

## Components Reused from Assignment 5

- TCP socket communication (connect/send/recv, port 5000)
- Multi-client server with per-client threads
- Broadcast messaging logic
- Private messaging (`/msg` command)
- Chat history logging to CSV
- Client/session state management and join/leave notifications

Only the client interface was changed from terminal-based to GUI.

---

## Future Improvements

- User authentication (password field)
- Encrypted communication (TLS)
- File sharing
- Group chat / channels
- Message timestamps displayed in the GUI
- Emoji support and improved UI styling
- Dark mode

---

## Report

Full report with GUI design decisions, testing results, and Wireshark verification: [`Assignment6_Report.docx`](./Assignment6_Report.docx)
