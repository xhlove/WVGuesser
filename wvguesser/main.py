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
hex_session_key = '87cb926617dfd527284b9c40a65a4165c9d3777563038b49b9100d33d36099906c43fd2eab832fa20d113113f9e84e6a06df0a93e4456f7d4026ca493834a332f4c6afc7f11da4290747ab8ffb7677bf99d97eda4b973f0f88e320c82093dc2f0c9cfba2d9943f92410d1a3ef2f508641758cdbf87c141925fae3d40b068295a2da1f3f47d30f781a02436687fe75fed926ef0aa2ec1a52ab6b75c03bdb38d85e4e3186671d910f6f24769d8037aeeed8df4cb6a7fc4a924d948e701aed91c567a8e44386d8d34112816379e7b7c2e18132491480c0931c5f045cc1c8cdb5916d306667f9438906cd29f6fd5e553dba26bda68a2ba978c4b71559bb4f7768971'
instance.run(hex_session_key)

# python -m wvguesser.main