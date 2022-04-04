from cocotb_test.simulator import run
from glob import glob
import pytest

@pytest.mark.parametrize(
    "parameters", [
        {"WIDTH": "8" , "DEPTH": "4"}, 
        {"WIDTH": "8", "DEPTH": "2"}, 
        ])
def test_axis_fifo(parameters):
    run(
        verilog_sources=glob('axis_fifo/hdl/*'),
        toplevel="axis_fifo",
        module="axis_fifo_tb",
        simulator="icarus",
        verilog_compile_args=["-g2012"],

        parameters=parameters,
        extra_env=parameters,
        sim_build="axis_fifo/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )