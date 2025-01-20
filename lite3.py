import llvmlite.binding as llvm
from llvmlite import ir

int16 = ir.IntType(16)
double = ir.DoubleType()
half = ir.HalfType()

fnty = ir.FunctionType(int16, (double,))

module = ir.Module(name=__file__)
func = ir.Function(module, fnty, name="fptest")

block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)
a, = func.args
result = builder.fptrunc(a, half, name="res")
result = builder.bitcast(result, int16)
builder.ret(result)
print(module)

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
llmod = llvm.parse_assembly(str(module))
llmod.verify()
engine = llvm.create_mcjit_compiler(llmod, target_machine)
engine.finalize_object()
engine.run_static_constructors()

print(target_machine.emit_assembly(llmod))