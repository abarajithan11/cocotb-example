import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
def test_register_simple(dut):

    ''' Clock Generation '''
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    ''' Assign random values to input, wait for a clock and verify output '''
    for i in range(10):
        val = random.randint(0, 255)
        dut.d.value = val
        
        cocotb.log.info("hello")
        
        yield FallingEdge(dut.clk)
        assert dut.q.value == val, f"Failed on the {i}th cycle. Got {dut.q.value}, expected {val}"
        