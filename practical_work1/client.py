import socket
import os

# Cấu hình địa chỉ IP của server (thay đổi nếu chạy trên 2 máy khác nhau)
SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 12345
BUFFER_SIZE = 4096

def send_file(filepath):
    # Kiểm tra file có tồn tại không
    if not os.path.isfile(filepath):
        print(f"[-] Không tìm thấy file: {filepath}")
        return

    # 1. socket(): Tạo socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 2. connect(): Kết nối đến server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Đã kết nối đến server {SERVER_HOST}:{SERVER_PORT}")

        # Lấy tên file từ đường dẫn
        filename = os.path.basename(filepath)

        # --- Bắt đầu quá trình gửi file ---
        # Bước A: Gửi tên file kèm theo ký tự xuống dòng làm dấu phân cách
        # sendall() đảm bảo toàn bộ dữ liệu được gửi đi
        client_socket.sendall(filename.encode() + b'\n')

        # Bước B: Mở file để đọc (chế độ binary 'rb') và gửi nội dung
        with open(filepath, 'rb') as f:
            while True:
                # Đọc file theo từng khối (chunk)
                data = f.read(BUFFER_SIZE)
                if not data:
                    break # Đã đọc hết file
                # 3. send(): Gửi khối dữ liệu
                client_socket.sendall(data)

        print(f"[+] Đã gửi file {filename} thành công.")

    except ConnectionRefusedError:
        print("[-] Không thể kết nối. Hãy đảm bảo server đang chạy.")
    finally:
        # 4. close(): Đóng kết nối
        client_socket.close()

if __name__ == "__main__":
    file_to_send = input("Nhập đường dẫn file cần gửi (ví dụ: test.txt): ")
    send_file(file_to_send)
