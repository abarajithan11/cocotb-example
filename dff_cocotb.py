import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
def test_dff_simple(dut):
    """ Test that d propagates to q """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    for i in range(10):
        val = random.randint(0, 255)
        dut.d <= val  # Assign the random value val to the input port d
        yield FallingEdge(dut.clk)
        assert dut.q.value == val, "output q was incorrect on the {}th cycle".format(i)