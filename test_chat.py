import socket
import threading
import time
import unittest

from server import ChatServer


class ChatTest(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer(("127.0.0.1", 0))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.connections = []

    def tearDown(self):
        for connection, _ in self.connections:
            connection.close()
        self.server.shutdown()
        self.server.server_close()

    def connect(self, name):
        connection = socket.create_connection(self.server.server_address, timeout=2)
        connection.sendall(f"{name}\n".encode())
        reader = connection.makefile(encoding="utf-8")
        self.connections.append((connection, reader))
        self.wait_for_clients(len(self.connections))
        return connection, reader

    def wait_for_clients(self, count):
        deadline = time.time() + 2
        while len(self.server.clients) != count and time.time() < deadline:
            time.sleep(0.01)
        self.assertEqual(len(self.server.clients), count)

    def test_messages_reach_other_clients(self):
        _, ana = self.connect("ana")
        bogdan, _ = self.connect("bogdan")
        self.assertEqual(ana.readline().strip(), "* bogdan a intrat in chat")

        bogdan.sendall(b"salut\n")
        self.assertEqual(ana.readline().strip(), "bogdan: salut")

    def test_leaving_is_announced(self):
        _, ana = self.connect("ana")
        bogdan, _ = self.connect("bogdan")
        ana.readline()

        bogdan.shutdown(socket.SHUT_RDWR)
        self.assertEqual(ana.readline().strip(), "* bogdan a iesit din chat")
        self.wait_for_clients(1)


if __name__ == "__main__":
    unittest.main()
