import sys
import math
import time
import binascii
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util import Padding

from wasmer import Store, Type, Function, FunctionType, Module, ImportObject

from wasmer import Instance as WasmerInstance


class Instance:

    def __init__(self, module: Module, store: Store):
        # 构建env 即外部导入函数
        _import_object = self.gen_import_object(store)
        # 初始化env并注册外部导入函数 -> register('env', {'key': func, ...})
        self.import_object = ImportObject()
        self.import_object.register('a', _import_object)
        self.asm = WasmerInstance(module, import_object=self.import_object)
        self.exports = self.asm.exports
        self.memory = self.exports.i
        self.stack = 0
        self._ctx = None # type: int
        self.export_configs = {
            'callback': self.exports.j,
            '_malloc': self.exports.k,
            '_freeStr': self.exports.m,
            '_guessInput': self.exports.n,
            '_getOutput': self.exports.o,
            '_getDeoaep': self.exports.p,
            'stackSave': self.exports.q,
            'stackRestore': self.exports.r,
            'stackAlloc': self.exports.s,
        }

    def run(self, hex_session_key: str):
        ts = time.time()
        self.initRuntime()
        encKey = binascii.a2b_hex(hex_session_key)
        print(hex_session_key)
        buf = [0] * 1026
        offset = 2
        while offset < 1026:
            bt = math.floor((offset - 2) / 4)
            offs = math.floor((offset - 2) % 4)
            desired = (encKey[len(encKey) - bt - 1] >> (offs * 2)) & 3
            print("desired", desired, offset, bt, offs)
            _start = len(hex_session_key) - bt * 2
            destail = hex_session_key[_start:_start + bt * 2]
            val = ''
            j = buf[offset]
            ccount = 0
            while j < 8:
                ccount += 1
                buf[offset] = j
                st = binascii.b2a_hex(bytes(buf)).decode('utf-8')
                val = self.guessInput(st)
                _start = len(val) - bt * 2 - 2
                sub = int(val[_start:_start + 2], 16)
                got = (sub >> (offs * 2)) & 3
                _start = len(hex_session_key) - bt * 2
                gtail = val[_start:_start + bt * 2]
                # print("", j, offset, sub, got, desired, "|||", gtail, destail)
                if got == desired and gtail == destail:
                    if offset % 16 == 2:
                        print(f'耗时 {time.time() - ts:.2f}s', val)
                    break
                j += 1
            # print('jjj', j)
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
        outp = self.getDeoaep(st)
        print(outp)
        if len(outp) < 10:
            assert 1 == 0, 'Could not remove padding, probably invalid key'
        print(st)
        return outp

    def decrypt_license_keys(self, session_key: str, context_enc: str, key_infos: dict):
        cmac_obj = CMAC.new(binascii.a2b_hex(session_key), ciphermod=AES)
        cmac_obj.update(binascii.a2b_hex(context_enc))

        enc_cmac_key = cmac_obj.digest()

        for index, [keyId, keyData, keyIv] in key_infos.items():
            cipher = AES.new(enc_cmac_key, AES.MODE_CBC, iv=binascii.a2b_hex(keyIv))
            decrypted_key = cipher.decrypt(binascii.a2b_hex(keyData))
            # clear_key = Padding.unpad(decrypted_key, 16)
            print(f'<id>:<k> {keyId}:{decrypted_key.hex()}')

    def _freeStr(self, ptr: int):
        return self.export_configs['_freeStr'](ptr)

    def initRuntime(self):
        return self.export_configs['callback']()

    def guessInput(self, text: str):
        # print('_guessInput', len(text))
        return self.ccall('_guessInput', str, text)

    def getDeoaep(self, text: str):
        return self.ccall('_getDeoaep', str, text)

    def stackAlloc(self, length: int):
        func_name = sys._getframe().f_code.co_name
        return self.export_configs[func_name](length)

    def stackSave(self):
        func_name = sys._getframe().f_code.co_name
        return self.export_configs[func_name]()

    def stackRestore(self, stack: int):
        func_name = sys._getframe().f_code.co_name
        return self.export_configs[func_name](stack)

    def stringToUTF8(self, data: str, ptr: int, max_write_length: int):
        _data = data.encode('utf-8')
        write_length = len(_data)
        if write_length == 0:
            self.memory.uint8_view()[ptr] = 0
        elif write_length > max_write_length:
            write_length = max_write_length
            self.memory.uint8_view()[ptr:ptr + write_length] = _data[:write_length]
        else:
            self.memory.uint8_view()[ptr:ptr + write_length] = _data
        return write_length

    def writeArrayToMemory(self, array: list, ptr: int):
        self.memory.int8_view()[ptr:ptr + len(array)] = array

    def writeBytesToMemory(self, data: bytes, ptr: int):
        self.memory.uint8_view()[ptr:ptr + len(data)] = list(data)

    def UTF8ToString(self, ptr: int) -> str:
        if ptr > 0:
            _memory = self.memory.uint8_view(offset=ptr)
            data = []
            index = 0
            while(_memory[index] != 0):
                data.append(_memory[index])
                index += 1
            return bytes(data).decode('utf-8')
        else:
            return ''

    def ccall(self, func_name: str, returnType: 'type', *args):
        def convertReturnValue(_ptr: int):
            if returnType == str:
                return self.UTF8ToString(_ptr)
            elif returnType == bool:
                return bool(returnType)
            return _ptr
        stack = 0
        _args = []
        for arg in args:
            if isinstance(arg, str):
                if stack == 0:
                    stack = self.stackSave()
                max_write_length = (len(arg) << 2) + 1
                ptr = self.stackAlloc(max_write_length)
                self.stringToUTF8(arg, ptr, max_write_length)
                _args.append(ptr)
            elif isinstance(arg, list):
                ptr = self.stackAlloc(len(arg))
                self.writeArrayToMemory(arg, ptr)
                _args.append(ptr)
            elif isinstance(arg, bytes):
                ptr = self.stackAlloc(len(arg))
                self.writeBytesToMemory(arg, ptr)
                _args.append(ptr)
            elif isinstance(arg, bytearray):
                ptr = self.stackAlloc(len(arg))
                self.writeBytesToMemory(arg, ptr)
                _args.append(ptr)
            else:
                _args.append(arg)
        ptr = self.export_configs[func_name](*_args)
        ret = convertReturnValue(ptr)
        if stack != 0:
            self.stackRestore(stack)
        return ret

    def cxa_allocate_exception(self, size: int):
        return self.malloc(size + 16) + 16

    def malloc(self, size: int):
        return self.export_configs['_malloc'](size)

    def cxa_throw(self, param_0, param_1, param_2):
        print('call cxa_throw')

    def abort(self, param_0):
        print('call abort')

    def emscripten_memcpy_big(self, dest: int, src: int, num: int = None):
        # print('call _emscripten_memcpy_big', dest, src, num)
        if num is None:
            num = len(self.memory.uint8_view()) - 1
        self.memory.uint8_view()[dest:dest + num] = self.memory.uint8_view()[src:src + num]
        return dest

    def emscripten_resize_heap(self, param_0):
        print('call emscripten_resize_heap')

    def environ_get(self, __environ, environ_buf):
        print('call environ_get', __environ, environ_buf)
        bufSize = 0
        strings = self.getEnvStrings()
        for index, string in enumerate(strings):
            ptr = environ_buf + bufSize
            self.memory.int32_view()[__environ + index * 4 >> 2] = ptr
            self.writeAsciiToMemory(string, ptr)
            bufSize += len(string) + 1
        return 0

    def environ_sizes_get(self, penviron_count: int, penviron_buf_size: int):
        print('call environ_sizes_get', penviron_count, penviron_buf_size)
        strings = self.getEnvStrings()
        self.memory.int32_view()[penviron_count >> 2] = len(strings)
        bufSize = 0
        for string in strings:
            bufSize += len(string) + 1
        self.memory.int32_view()[penviron_buf_size >> 2] = bufSize
        return 0

    def strftime_l(self, param_0, param_1, param_2):
        print('call strftime_l')

    def writeAsciiToMemory(self, string, buffer, dontAddNull: int = 0):
        for num in list(string.encode('utf-8')):
            self.memory.int8_view()[buffer >> 0] = num
            buffer += 1
        if dontAddNull == 0:
            self.memory.int8_view()[buffer >> 0] = 0

    def getEnvStrings(self):
        return ['USER=web_user', 'LOGNAME=web_user', 'PATH=/', 'PWD=/', 'HOME=/home/web_user', 'LANG=zh_CN.UTF-8', '_=./this.program']

    def gen_import_object(self, store: Store):
        cxa_allocate_exception_Func = Function(store, self.cxa_allocate_exception, FunctionType([Type.I32], [Type.I32]))
        cxa_throw_Func = Function(store, self.cxa_throw, FunctionType([Type.I32, Type.I32, Type.I32], []))
        abort_Func = Function(store, self.abort, FunctionType([], []))
        emscripten_memcpy_big_Func = Function(store, self.emscripten_memcpy_big, FunctionType([Type.I32, Type.I32, Type.I32], [Type.I32]))
        emscripten_resize_heap_Func = Function(store, self.emscripten_resize_heap, FunctionType([Type.I32], [Type.I32]))
        environ_get_Func = Function(store, self.environ_get, FunctionType([Type.I32, Type.I32], [Type.I32]))
        environ_sizes_get_Func = Function(store, self.environ_sizes_get, FunctionType([Type.I32, Type.I32], [Type.I32]))
        strftime_l_Func = Function(store, self.strftime_l, FunctionType([Type.I32, Type.I32, Type.I32, Type.I32, Type.I32], [Type.I32]))
        _import_object = {
            "b": cxa_allocate_exception_Func,
            "a": cxa_throw_Func,
            "c": abort_Func,
            "d": emscripten_memcpy_big_Func,
            "e": emscripten_resize_heap_Func,
            "g": environ_get_Func,
            "h": environ_sizes_get_Func,
            "f": strftime_l_Func,
        }
        return _import_object