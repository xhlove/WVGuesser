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
hex_session_key = '8fd2cee76d6709890a42ff53ea79db760c79a88a8b81b7b1abd0682fa080f3165d4c672715e372bca3e100355306e48098631771f0a2f84805623320685db54b06e7dd28e25daf45d4d1d7ef6a4e6b9f7e985c9c1febfb2b731e3482f0b82c7f107d519f4502efbb81914a2d995101c679505cee56d5f3481be58852ec11f2630adb5994ac78a5f9a2df4fc975d6cb106242f9c1791488f80de1bb387de72436cc824b3f1268995a2c9e762dfb51ede36870cf0342ee398c8e8a654a4f2768e2c485d44e13b3ce399e6923c70780bc04142e56b053a6ac912ae8a4f60cb4e20383334dff05ee6a722730d9ff33cd970fa240d25d17dfa36cf4b8fe70809687f7'
instance.run(hex_session_key)

# python -m wvguesser.main