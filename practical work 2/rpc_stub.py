
# Filename: rpc_stub.py
# Description: Module đóng gói giao thức RPC thủ công

import struct
import socket

# Định nghĩa các ID cho thủ tục RPC
RPC_ID_FILENAME = 1
RPC_ID_CHUNK = 2
RPC_ID_END = 3

# Cấu trúc Header: 2 số nguyên (integer) 4-byte
# Format 'ii' nghĩa là: int (rpc_id), int (payload_size) -> Tổng 8 bytes
HEADER_FORMAT = 'ii' 
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def rpc_send_filename(sock, filename):
    """
    Hàm Stub 1: Gửi tên file
    """
    filename_bytes = filename.encode('utf-8')
    payload_size = len(filename_bytes)
    
    # 1. Đóng gói Header: (ID=1, Size)
    header = struct.pack(HEADER_FORMAT, RPC_ID_FILENAME, payload_size)
    
    # 2. Gửi Header + Payload (Tên file)
    sock.sendall(header)
    sock.sendall(filename_bytes)

def rpc_send_chunk(sock, data_chunk):
    """
    Hàm Stub 2: Gửi một phần nội dung file
    """
    payload_size = len(data_chunk)
    
    # 1. Đóng gói Header: (ID=2, Size)
    header = struct.pack(HEADER_FORMAT, RPC_ID_CHUNK, payload_size)
    
    # 2. Gửi Header + Payload (Dữ liệu)
    sock.sendall(header)
    sock.sendall(data_chunk)

def rpc_end_file(sock):
    """
    Hàm Stub 3: Báo hiệu kết thúc
    """
    # Gửi Header với ID=3 và size=0
    header = struct.pack(HEADER_FORMAT, RPC_ID_END, 0)
    sock.sendall(header)

def recv_exact(sock, size):
    """
    Hàm hỗ trợ: Nhận chính xác n bytes (để tránh bị trôi dữ liệu)
    """
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data