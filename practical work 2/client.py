
import socket
import os
import rpc_stub # Import module stub

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888
BUFFER_SIZE = 4096

def main():
  
    filepath = input("Nhập tên file cần gửi (ví dụ test.txt): ").strip()
    if not os.path.isfile(filepath):
        print("[-] Không tìm thấy file!")
        return

    # Kết nối Socket
    print(f"[*] Đang kết nối đến {SERVER_IP}:{SERVER_PORT}...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except ConnectionRefusedError:
        print("[-] Không thể kết nối đến Server.")
        return

    # --- BẮT ĐẦU QUY TRÌNH RPC ---
    filename = os.path.basename(filepath)
    
    
    print(f"[*] Gọi RPC 1: Gửi tên file '{filename}'...")
    rpc_stub.rpc_send_filename(client_socket, filename)
    
   
    print("[*] Gọi RPC 2: Đang gửi nội dung (Loop)...")
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            
            rpc_stub.rpc_send_chunk(client_socket, chunk)
            
   
    print("[*] Gọi RPC 3: Báo hiệu kết thúc file.")
    rpc_stub.rpc_end_file(client_socket)
    
    
    client_socket.close()
    print("[+] Hoàn thành thành công!")

if __name__ == "__main__":
    main()