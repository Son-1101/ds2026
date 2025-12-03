
import socket
import struct
import rpc_stub 

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8888

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)
    
    print(f"[*] Manual RPC Server đang chạy tại {SERVER_IP}:{SERVER_PORT}")

    # Chấp nhận kết nối
    client_socket, addr = server_socket.accept()
    print(f"[+] Client kết nối từ: {addr}")

    current_file = None
    
    try:
        while True:
            # 1. Nhận Header (8 bytes)
            header_data = rpc_stub.recv_exact(client_socket, rpc_stub.HEADER_SIZE)
            if not header_data:
                break # Client ngắt kết nối
            
            # 2. Giải mã Header -> Lấy rpc_id và kích thước payload
            rpc_id, payload_size = struct.unpack(rpc_stub.HEADER_FORMAT, header_data)
            
            # 3. Xử lý dựa trên rpc_id (Switch-case logic)
            if rpc_id == rpc_stub.RPC_ID_FILENAME:
            
                filename_bytes = rpc_stub.recv_exact(client_socket, payload_size)
                filename = filename_bytes.decode('utf-8')
                
                output_name = f"received_{filename}"
                print(f"[*] RPC 1 (Filename): Đang tạo file '{output_name}'")
                current_file = open(output_name, 'wb')
                
            elif rpc_id == rpc_stub.RPC_ID_CHUNK:
              
                chunk_data = rpc_stub.recv_exact(client_socket, payload_size)
                if current_file:
                    current_file.write(chunk_data)
               
                
            elif rpc_id == rpc_stub.RPC_ID_END:
             
                print("[*] RPC 3 (End): Hoàn tất truyền file.")
                if current_file:
                    current_file.close()
                    current_file = None
                break
                
            else:
                print(f"[-] RPC ID không hợp lệ: {rpc_id}")
                break
                
    except Exception as e:
        print(f"[-] Lỗi: {e}")
    finally:
        if current_file: current_file.close()
        client_socket.close()
        server_socket.close()
        print("[*] Server đã đóng.")

if __name__ == "__main__":
    start_server()