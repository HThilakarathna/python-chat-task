import tkinter as tk
from tkinter import messagebox
import socket
import threading

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")

        self.entry_message = tk.Entry(master)
        self.entry_message.pack(pady=10)

        self.btn_send = tk.Button(master, text="Send", command=self.send_message)
        self.btn_send.pack()

        self.text_messages = tk.Text(master, height=20, width=50)
        self.text_messages.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))

        message_receiver = threading.Thread(target=self.receive_messages)
        message_receiver.start()

    def send_message(self):
        message = self.entry_message.get()
        self.client_socket.send(message.encode('utf-8'))
        self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.text_messages.insert(tk.END, f"{message}\n")
                self.text_messages.see(tk.END)
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
