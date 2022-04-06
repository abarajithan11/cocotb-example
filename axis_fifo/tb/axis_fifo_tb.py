import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Join, ClockCycles
from cocotbext.axi import (AxiStreamBus, AxiStreamSource, AxiStreamSink, AxiStreamMonitor)
from custom_axis import axis_sink, axis_source

import random
import numpy as np

NUM_DATA = 1000

@cocotb.test()
async def axis_fifo_test(dut):
    global NUM_DATA

    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.aresetn.value = 0
    await ClockCycles(dut.aclk, 2)
    dut.aresetn.value = 1

    data_in = np.random.randint(0, 255, size=(NUM_DATA), dtype=np.uint8)

    task_source = cocotb.start_soon(axis_source(data_in, NUM_DATA))
    task_sink = cocotb.start_soon(axis_sink(data_in, NUM_DATA))

    await Join(task_source)
    await Join(task_sink)

    cocotb.log.info("Done")
