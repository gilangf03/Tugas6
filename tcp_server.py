import socket
import threading

def handle_client(conn, addr):
    print(f"[TERHUBUNG] {addr}")
    conn.settimeout(40)

    def terima_pesan():
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[PUTUS] {addr} keluar.")
                    break
                print(f"\n[CLIENT {addr}] {data.decode('utf-8')}")
            except socket.timeout:
                print(f"[TIMEOUT] Tidak ada data dari {addr} dalam 10 detik.")
                break
            except ConnectionResetError:
                print(f"[ERROR] Koneksi {addr} terputus.")
                break
        conn.close()
        print(f"[TUTUP] {addr} ditutup.")

    # Jalankan thread untuk terima pesan dari client
    thread = threading.Thread(target=terima_pesan, daemon=True)
    thread.start()

    # Server bisa kirim balasan manual
    try:
        while True:
            pesan = input("[BALAS] Ketik pesan ke client: ")
            if pesan.lower() == "exit":
                break
            conn.sendall(pesan.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[TUTUP] Koneksi ke {addr} ditutup dengan aman.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(1)
    print("[SERVER AKTIF] Menunggu koneksi di port 5000...")

    try:
        conn, addr = server.accept()
        handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\n[BERHENTI] Server dimatikan.")
    finally:
        server.close()
        print("[TUTUP] Socket server ditutup.")

if __name__ == "__main__":
    start_server()