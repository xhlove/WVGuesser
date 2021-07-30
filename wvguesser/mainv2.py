import os
import sys
import json
import math
import time
import binascii
import subprocess
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

MAIN_EXE = (Path('.') / 'main.exe').resolve().as_posix()


def guessInput(text: str):
    resp = subprocess.check_output(f'{MAIN_EXE} guessInput {text}')
    return resp.decode('utf-8').strip()


def getDeoaep(text: str):
    resp = subprocess.check_output(f'{MAIN_EXE} getDeoaep {text}')
    return resp.decode('utf-8').strip()


def run(hex_session_key: str):
    ts = time.time()
    encKey = binascii.a2b_hex(hex_session_key)
    print(hex_session_key)
    buf = [0] * 1026
    offset = 2
    while offset < 1026:
        print(f'当前进度 {(offset - 2) / 1024 * 100:.2f}% 耗时 {time.time() - ts:.2f}s')
        bt = math.floor((offset - 2) / 4)
        offs = math.floor((offset - 2) % 4)
        desired = (encKey[len(encKey) - bt - 1] >> (offs * 2)) & 3
        destail = hex_session_key[len(hex_session_key) - bt * 2:len(hex_session_key)]
        j = buf[offset]
        while j < 8:
            buf[offset] = j
            st = binascii.b2a_hex(bytes(buf)).decode('utf-8')
            # print(st)
            val = guessInput(st)
            # print(val)
            sub = int(val[len(val) - bt * 2 - 2:len(val) - bt * 2], 16)
            got = (sub >> (offs * 2)) & 3
            gtail = val[len(hex_session_key) - bt * 2:len(hex_session_key) + bt * 2]
            if got == desired and gtail == destail:
                if offset % 16 == 2:
                    print(val)
                break
            j += 1
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
    print(f'==> 耗时 {time.time() - ts:.2f}s')
    print("Output", buf)
    st = binascii.b2a_hex(bytes(buf)).decode('utf-8')
    outp = getDeoaep(st)
    print(outp)
    if len(outp) < 10:
        assert 1 == 0, 'Could not remove padding, probably invalid key'
    print(st)
    return outp


def decrypt_license_keys(session_key: str, context_enc: str, key_infos: dict):
    cmac_obj = CMAC.new(binascii.a2b_hex(session_key), ciphermod=AES)
    cmac_obj.update(binascii.a2b_hex(context_enc))

    enc_cmac_key = cmac_obj.digest()

    for index, [keyId, keyData, keyIv] in key_infos.items():
        cipher = AES.new(enc_cmac_key, AES.MODE_CBC, iv=binascii.a2b_hex(keyIv))
        decrypted_key = cipher.decrypt(binascii.a2b_hex(keyData))
        # clear_key = Padding.unpad(decrypted_key, 16)
        print(f'<id>:<k> {keyId}:{decrypted_key.hex()}')


def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = (Path('.') / 'offline_config.json').resolve().as_posix()
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    clear_session_key = run(config['enc_session_key'])
    decrypt_license_keys(clear_session_key, config['enc_key'], config['key_infos'])
    sys.stdin.read()


if __name__ == '__main__':
    main()