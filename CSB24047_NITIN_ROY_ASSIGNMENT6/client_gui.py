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
        """Placeholder for Task 2: Graphical Chat Interface"""
        # We will build this in the next step!
        tk.Label(self.root, text=f"Welcome {self.username}! Chat UI goes here.", font=("Helvetica", 14)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()