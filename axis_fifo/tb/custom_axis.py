import cocotb
from cocotb.triggers import RisingEdge
import random

'''
Signal Driver
'''
async def axis_source(data, NUM_DATA, VALID_PROB=0.5):
    
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

'''
Signal Monitor
'''
async def axis_sink(data, NUM_DATA, READY_PROB=0.5):

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