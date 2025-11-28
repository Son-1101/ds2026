import socket
import os

print("--- ĐƯỜNG DẪN HIỆN TẠI CỦA SERVER ---")
print(os.getcwd())
print("------------------------------------")
# Cấu hình địa chỉ IP và Port cho server
SERVER_HOST = '0.0.0.0'  # Lắng nghe trên tất cả các card mạng
SERVER_PORT = 12345
BUFFER_SIZE = 4096  # Kích thước bộ đệm nhận dữ liệu (4KB)

def start_server():
    # 1. socket(): Tạo socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Cho phép sử dụng lại địa chỉ port ngay lập tức sau khi tắt server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. bind(): Gán socket với địa chỉ và port
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    
    # 3. listen(): Bắt đầu lắng nghe các kết nối đến
    server_socket.listen(1)
    print(f"[*] Server đang lắng nghe tại {SERVER_HOST}:{SERVER_PORT}")

    # 4. accept(): Chấp nhận một kết nối từ client
    client_socket, client_address = server_socket.accept()
    print(f"[+] Đã kết nối với {client_address}")

    # --- Bắt đầu quá trình nhận file ---
    received_data = b''
    filename = None

    # Bước A: Nhận dữ liệu cho đến khi tìm thấy dấu phân cách '\n' để lấy tên file
    while True:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            print("[-] Kết nối bị đóng trước khi nhận được tên file.")
            client_socket.close()
            server_socket.close()
            return
        received_data += chunk
        if b'\n' in received_data:
            # Tách tên file và phần đầu của nội dung file
            filename_bytes, file_content_start = received_data.split(b'\n', 1)
            filename = filename_bytes.decode()
            # Đặt lại phần dữ liệu đã nhận là phần nội dung file
            received_data = file_content_start
            break

    print(f"[*] Đang nhận file: {filename}")

    # Bước B: Mở file để ghi (chế độ binary 'wb') và ghi phần dữ liệu còn lại
    # Thêm tiền tố "received_" để tránh ghi đè file gốc nếu chạy trên cùng một máy
    output_filename = f"received_{filename}"
    with open(output_filename, 'wb') as f:
        # Ghi phần nội dung đã nhận cùng với tên file
        f.write(received_data)

        # 5. recv() loop: Tiếp tục nhận các phần còn lại của file
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break  # Kết thúc file (EOF)
            f.write(data)

    print(f"[+] Đã nhận file thành công và lưu thành: {output_filename}")
    
    # 6. close(): Đóng kết nối
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()