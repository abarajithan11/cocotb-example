from cocotb_test.simulator import run
from glob import glob
import pytest

@pytest.mark.parametrize(
    "parameters", [
        {"WIDTH_IN": "2", "WIDTH_OUT": "16"}, 
        {"WIDTH_IN": "16"}
        ])
def test_dff(parameters):
    run(
        verilog_sources=glob('dff/hdl/*'),
        toplevel="dff",            # top level HDL
        module="dff_cocotb",       # name of cocotb test module
        simulator="icarus",

        parameters=parameters,
        extra_env=parameters,
        sim_build="dff/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )