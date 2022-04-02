from cocotb_test.simulator import run

def test_dff():
    run(
        verilog_sources=["dff.sv"], # sources
        toplevel="dff",            # top level HDL
        module="dff_cocotb",       # name of cocotb test module
        simulator="icarus"
    )