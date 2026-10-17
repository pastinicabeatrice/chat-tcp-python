import socket
import sys
import threading


def receive(connection):
    for line in connection.makefile(encoding="utf-8"):
        print(line, end="")
    print("Conexiunea cu serverul s-a inchis")


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    name = input("Numele tau: ").strip()

    with socket.create_connection((host, port)) as connection:
        connection.sendall(f"{name}\n".encode())
        threading.Thread(target=receive, args=(connection,), daemon=True).start()
        print("Scrie mesaje si apasa Enter. /iesire pentru a parasi chatul.")
        for line in sys.stdin:
            if line.strip() == "/iesire":
                break
            connection.sendall(line.encode())


if __name__ == "__main__":
    main()
