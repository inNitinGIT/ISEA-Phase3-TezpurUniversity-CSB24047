import tkinter as tk
from tkinter import messagebox
import socket
import threading

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Chat Client")
        self.root.geometry("500x600")
        
        # Networking Configuration
        self.server_ip = "10.0.0.1" # Using the Mininet IP from your script
        self.port = 5000
        self.sock = None
        self.username = ""
        
        # Start with the login window
        self.create_login_window()

    def create_login_window(self):
        """Task 1: Develop a login window containing username and Connect button."""
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title Label
        tk.Label(self.login_frame, text="TCP Chat Application", font=("Helvetica", 16, "bold")).pack(pady=(120, 20))
        
        # Username Entry
        tk.Label(self.login_frame, text="Enter Username:", font=("Helvetica", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=25)
        self.username_entry.pack(pady=5)
        
        # Connect Button
        tk.Button(self.login_frame, text="Connect", command=self.connect_to_server, 
                  font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15).pack(pady=20)
        
        # Bind the 'Enter' key to the connect button for convenience
        self.root.bind('<Return>', lambda event: self.connect_to_server())

    def connect_to_server(self):
        """Validates user input and establishes the socket connection."""
        user = self.username_entry.get().strip()
        
        # Validate user input, prevent empty usernames
        if not user:
            messagebox.showwarning("Validation Error", "Username cannot be empty!")
            return
            
        try:
            # Setup socket connection
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.port))
            
            # Send username to server (reusing your existing logic)
            self.username = user
            self.sock.sendall(self.username.encode('utf-8'))
            
            # Transition to the Chat Interface
            self.login_frame.destroy()
            self.root.unbind('<Return>') # Unbind the enter key from login
            self.create_chat_window()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")

    def create_chat_window(self):
        """Task 2: Graphical Chat Interface"""
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # --- Top Bar (Status & Disconnect) ---
        top_frame = tk.Frame(self.chat_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(top_frame, text=f"Logged in as: {self.username}", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Disconnect", command=self.disconnect, bg="#f44336", fg="white").pack(side=tk.RIGHT)

        # --- Scrollable Message Area ---
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled', font=("Helvetica", 10))
        self.chat_display.pack(expand=True, fill=tk.BOTH, pady=(0, 10))

        # --- Bottom Bar (Input & Send) ---
        bottom_frame = tk.Frame(self.chat_frame)
        bottom_frame.pack(fill=tk.X)

        self.msg_entry = tk.Entry(bottom_frame, font=("Helvetica", 12))
        self.msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.msg_entry.bind('<Return>', lambda event: self.send_message()) # Hit Enter to send

        tk.Button(bottom_frame, text="Send", command=self.send_message, bg="#2196F3", fg="white", width=10).pack(side=tk.RIGHT)

        # --- Start Background Receiver (Prep for Task 5) ---
        receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receiver_thread.start()

    def send_message(self):
        """Handles sending messages to the server."""
        message = self.msg_entry.get().strip()
        if message:
            try:
                self.sock.sendall(message.encode('utf-8'))
                self.msg_entry.delete(0, tk.END) # Clear the input box after sending
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")

    def append_message(self, message):
        """Helper method to add text to the chat display and auto-scroll."""
        self.chat_display.config(state='normal') # Enable editing temporarily
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state='disabled') # Disable editing to prevent user typing
        self.chat_display.see(tk.END) # Automatic scrolling to the bottom

    def receive_messages(self):
        """Listens for incoming messages from the server in a background thread."""
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    self.append_message("[System] Disconnected from server.")
                    break
                
                # Append the received text to the GUI
                self.append_message(data.decode('utf-8'))
            except:
                self.append_message("[System] Connection closed.")
                break

    def disconnect(self):
        """Safely closes the socket and exits the application."""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.root.quit()




if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()