'''
First read "register/tb/test_register.py"
Then read this file
'''

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Join, ClockCycles
from custom_axis import axis_sink, axis_source

import random
import numpy as np

NUM_DATA = 1000

'''
1. Testbench
'''

@cocotb.test()
async def axis_fifo_tb(dut):
    global NUM_DATA

    '''
    Clock Generation
    '''
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    '''Drive reset'''
    dut.aresetn.value = 0
    await ClockCycles(dut.aclk, 2)
    dut.aresetn.value = 1

    '''Create a numpy array'''
    data_in = np.random.randint(0, 255, size=(NUM_DATA), dtype=np.uint8)
    
    '''Start the two functions in two parallel threads'''
    task_source = cocotb.start_soon(axis_source(data_in, NUM_DATA)) # Drives values
    task_sink = cocotb.start_soon(axis_sink(data_in, NUM_DATA)) # Compares values

    '''Wait until both functions end'''
    await Join(task_source)
    await Join(task_sink)

    cocotb.log.info("Done")



'''
2. Pytest Setup
'''

from cocotb_test.simulator import run
import glob
import pytest

@pytest.mark.parametrize(
    "parameters", [
        {"WIDTH": "8" , "DEPTH": "4"}, 
        {"WIDTH": "8", "DEPTH": "2"}, 
        {"WIDTH": "16", "DEPTH": "6"}, 
        ])
def test_axis_fifo(parameters):
    run(
        verilog_sources=glob.glob('axis_fifo/hdl/*'),
        toplevel="axis_fifo",

        module="test_axis_fifo",
        simulator="icarus",
        verilog_compile_args=["-g2012"],

        parameters=parameters,
        extra_env=parameters,
        sim_build="axis_fifo/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )