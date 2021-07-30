import json
from pathlib import Path
from wasmer_compiler_cranelift import Compiler
from wasmer import wat2wasm, engine, Store, Module

from wvguesser.wasm_helper import Instance


wasm = wat2wasm(Path('wvguesser/wasm_gsr.wat').read_text(encoding='utf-8'))
# wasm = Path(r'wvguesser/wasm_gsr.wasm').read_bytes()
# 初始化一个存储器
store = Store(engine.JIT(Compiler))
# 载入wasm
module = Module(store, wasm)
# 初始化实例 内存+模块+外部导入函数
instance = Instance(module, store)

config = json.loads(Path('wvguesser/offline_config.json').read_text(encoding='utf-8'))

clear_session_key = instance.run(config['enc_session_key'])
instance.decrypt_license_keys(clear_session_key, config['enc_key'], config['key_infos'])

# python -m wvguesser.main