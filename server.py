import socketserver
import sys
import threading


class ChatHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.name = self.rfile.readline().decode().strip() or "anonim"
        self.server.join(self)
        for line in self.rfile:
            text = line.decode().strip()
            if text:
                self.server.broadcast(f"{self.name}: {text}", self)

    def finish(self):
        self.server.leave(self)
        super().finish()

    def send(self, message):
        try:
            self.wfile.write((message + "\n").encode())
        except OSError:
            pass


class ChatServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address):
        super().__init__(address, ChatHandler)
        self.clients = set()
        self.lock = threading.Lock()

    def join(self, client):
        with self.lock:
            self.clients.add(client)
        self.broadcast(f"* {client.name} a intrat in chat", client)

    def leave(self, client):
        with self.lock:
            if client not in self.clients:
                return
            self.clients.remove(client)
        self.broadcast(f"* {client.name} a iesit din chat", client)

    def broadcast(self, message, sender):
        print(message)
        with self.lock:
            recipients = [client for client in self.clients if client is not sender]
        for client in recipients:
            client.send(message)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    with ChatServer(("0.0.0.0", port)) as server:
        print(f"Serverul de chat asculta pe portul {port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
