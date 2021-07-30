import sys
import json
import math
import time
import signal
import socket
import binascii
import subprocess
from typing import List
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from random import randint
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from notifypy import Notify
import ctypes
import socket


ctypes.windll.kernel32.SetConsoleTitleW("WVGuesser v1.1.0")

with open("WVGuesserConf.json") as json_data:
    config = json.load(json_data)

thread_conf = int(config['thread'])
notif_conf = str(config['notif'])


def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]


servers = []
clients = []
for i in range(5):
    port = find_free_port()

    MAIN_EXE = (Path('.') / 'main.exe').resolve().as_posix()
    p = subprocess.Popen(f'{MAIN_EXE} {port}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    servers.append(p)
    time.sleep(0.3)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', port))
    clients.append(client)


def handle_exit(signum, frame):
    close()


def close():
    try:
        [p.close() for p in clients]
        [p.kill() for p in servers]
    except Exception:
        pass


def call_func(client, msg: bytes):
    client.send(msg)
    resp = client.recv(1024)
    return resp.decode('utf-8').strip()


def multi_guessInput(bufs: List[bytes]):
    results = []
    with ThreadPoolExecutor(max_workers=thread_conf) as executor:
        results = executor.map(guessInput, clients, bufs)
    return results


def guessInput(client, buf: bytes):
    # return call_func(client, f'guessInput|{buf}\n')
    return call_func(client, b'guessInput|' + buf + b'\n')


def getDeoaep(client, buf: bytes):
    # return call_func(client, f'getDeoaep|{buf}\n')
    return call_func(client, b'getDeoaep|' + buf + b'\n')


def runv2(hex_session_key: str):
    ts = time.time()
    encKey = binascii.a2b_hex(hex_session_key)
    #print(hex_session_key)
    buf = [0] * 1026
    offset = 2
    while offset < 1026:
        print(f'[WVGuesser] {(offset - 2) / 1024 * 100:.2f}% / {time.time() - ts:.2f}s', end="\r")
        bt = math.floor((offset - 2) / 4)
        offs = math.floor((offset - 2) % 4)
        desired = (encKey[len(encKey) - bt - 1] >> (offs * 2)) & 3
        destail = hex_session_key[len(hex_session_key) - bt * 2:len(hex_session_key)]
        bufs = []
        j = buf[offset]
        for _j in range(5):
            buf[offset] = _j
            bufs.append(binascii.b2a_hex(bytes(buf)))
        for _j, val in enumerate(multi_guessInput(bufs)):
            sub = int(val[len(val) - bt * 2 - 2:len(val) - bt * 2], 16)
            got = (sub >> (offs * 2)) & 3
            gtail = val[len(hex_session_key) - bt * 2:len(hex_session_key) + bt * 2]
            if got == desired and gtail == destail:
                buf[offset] = _j
                j = buf[offset]
                break
        if j == 8:
            buf[offset] = 0
            offset -= 1
            if offset < 2:
                print('Could not match input')
                assert 1 == 0, "Could not find proper input encoding"
            buf[offset] += 1
            while buf[offset] == 8:
                buf[offset] = 0
                offset -= 1
                if offset < 2:
                    print('Could not match input')
                    assert 1 == 0, "Could not find proper input encoding"
                buf[offset] += 1
        else:
            offset += 1
    # print(f'==> Elapsed time {time.time() - ts:.2f}s')
    ctypes.windll.kernel32.SetConsoleTitleW(f'WVGuesser v1.1.0 - Elapsed time {time.time() - ts:.2f}s')
    # print("Output", buf)
    outp = getDeoaep(clients[0], binascii.b2a_hex(bytes(buf)))
    # print(outp)
    if len(outp) < 10:
        assert 1 == 0, 'Could not remove padding, probably invalid key'
    return outp


def decrypt_license_keys(session_key: str, context_enc: str, key_infos: dict):
    cmac_obj = CMAC.new(binascii.a2b_hex(session_key), ciphermod=AES)
    cmac_obj.update(binascii.a2b_hex(context_enc))

    enc_cmac_key = cmac_obj.digest()

    list_key = []

    for index, [keyId, keyData, keyIv] in key_infos.items():
        cipher = AES.new(enc_cmac_key, AES.MODE_CBC, iv=binascii.a2b_hex(keyIv))
        decrypted_key = cipher.decrypt(binascii.a2b_hex(keyData))
        # clear_key = Padding.unpad(decrypted_key, 16)
        list_key.append({'id': keyId, 'k': decrypted_key.hex()})
        # print(f'<id>:<k> {keyId}:{decrypted_key.hex()}')

    if len(list_key) >= 1:
        json_key = json.dumps(list_key)
        print(json_key)

        if notif_conf == "True":
            notification = Notify()
            notification.title = "WVGuesser"
            notification.message = f"{len(list_key)} keys found."
            notification.icon = "WVGUESSR.png"
            notification.send()
    else:
        print("No keys available.")


def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = (Path('.') / 'offline_config.json').resolve().as_posix()
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    clear_session_key = runv2(config['enc_session_key'])
    close()
    decrypt_license_keys(clear_session_key, config['enc_key'], config['key_infos'])
    sys.stdin.read()


if __name__ == '__main__':
    main()