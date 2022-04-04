import random
from types import coroutine
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Join
import numpy as np

NUM_DATA = 1000


async def axis_source(data, VALID_PROB=0.5):
    
    global NUM_DATA
    dut = cocotb.top

    def reset():
        dut.s_valid.value = dut.s_data.value = dut.s_last.value = dut.s_keep.value = 0
    reset()

    i_data, i_clk = 0, 0

    while True:
        if dut.s_ready.value:
            if i_data == NUM_DATA:
                break
            valid = random.choices([0,1], [1-VALID_PROB, VALID_PROB])[0]
            dut.s_valid.value = valid

            if valid:
                dut.s_valid.value = valid
                dut.s_data.value  = int(data[i_data])
                dut.s_keep.value  = 1

                if i_data == NUM_DATA-1:
                    dut.s_last.value = 1
                i_data += 1

        await RisingEdge(dut.aclk)
        i_clk += 1

    reset()


async def axis_sink(data, READY_PROB=0.5):

    global NUM_DATA
    dut = cocotb.top
    dut.m_ready.value = 1

    NUM_DATA = len(data)
    i_data, i_clk = 0, 0

    while True:
        if i_data == NUM_DATA:
            break

        ready = random.choices([0,1], [1-READY_PROB, READY_PROB])[0]
        dut.m_ready.value = ready
        
        await RisingEdge(dut.aclk)
        i_clk += 1

        if ready and dut.m_valid.value:
            assert dut.m_data.value == data[i_data], f'AXIS Sink failed at aclk={i_clk}. Expected: {data[i_data]}, received {int(dut.m_data.value)}'
            assert dut.m_keep.value == 1,      f'AXIS m_keep not received at aclk={i_clk}'

            if i_data == NUM_DATA-1:
                assert dut.m_last.value == 1, f'AXIS m_last not received'
            else:
                assert dut.m_last.value == 0, f'AXIS m_last raised at aclk={i_clk}'
            i_data += 1


    dut.m_ready.value = 0


@cocotb.test()
async def axis_fifo_test(dut):
    global NUM_DATA

    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.aresetn.value = 0
    await RisingEdge(dut.aclk)
    await RisingEdge(dut.aclk)
    dut.aresetn.value = 1

    data_in = np.random.randint(0, 255, size=(NUM_DATA), dtype=np.uint8)

    task_source = cocotb.start_soon(axis_source(data_in))
    task_sink = cocotb.start_soon(axis_sink(data_in))

    await Join(task_source)
    await Join(task_sink)

    cocotb.log.info("Done")
