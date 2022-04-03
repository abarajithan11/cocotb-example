from cocotb_test.simulator import run
from glob import glob

def test_dff():
    run(
        verilog_sources=glob('hdl/*'),
        toplevel="dff",            # top level HDL
        module="dff_cocotb",       # name of cocotb test module
        simulator="icarus"
    )