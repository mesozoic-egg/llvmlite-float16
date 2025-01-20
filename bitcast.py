from __future__ import print_function

from ctypes import CFUNCTYPE, c_double
import ctypes

import llvmlite.binding as llvm


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

llvm_ir = """
define void @E_(float* noalias %data0,i16* noalias %data1) {
  %v0 = getelementptr inbounds i16, i16* %data1, i32 0
  %v1 = load i16, i16* %v0
  %v2 = zext i16 %v1 to i32
  ;%v3 = getelementptr inbounds half, half* %data0, i32 0
  %v3 = getelementptr inbounds float, float* %data0, i32 0
  %v4 = mul i32 %v2, 65536
  %v5 = bitcast i32 %v4 to float
  ;%v6 = fptrunc float %v5 to half
  ;store half %v6, half* %v3
  store float %v5, float* %v3
  ret void
}
   """

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("E_")

# Run the function via ctypes
float_arr = ctypes.c_uint32 * 1
half_arr = ctypes.c_uint16 * 1

cfunc = CFUNCTYPE(ctypes.c_void_p, float_arr, half_arr)(func_ptr)


# 17948 is int for the 16 bit value 0x461c
# IR code extend this to 0x0000461c, then left shift to become 0x461c0000
a = (ctypes.c_uint32 * 1)()
b = (ctypes.c_uint16 * 1)(17948)
print(hex(a[0]))
res = cfunc(a, b)
print(hex(a[0]))