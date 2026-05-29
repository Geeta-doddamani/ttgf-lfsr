# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


def read_lfsr(dut):
    """
    The 4-bit LFSR output is connected to uo_out[3:0].
    This function reads only lower 4 bits.
    """
    return int(dut.uo_out.value) & 0xF


@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting 4-bit LFSR test")

    # Start clock: 10 ns period
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initialize all inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply active-low reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")

    # During reset, LFSR should load seed value 0001
    assert read_lfsr(dut) == 0x1, (
        f"Reset failed: expected LFSR = 1, got {read_lfsr(dut):X}"
    )

    # Release reset
    dut.rst_n.value = 1
    await Timer(1, unit="ns")

    # Expected 4-bit LFSR sequence:
    # 1 -> 3 -> 7 -> F -> E -> D -> A -> 5 -> B -> 6 -> C -> 9 -> 2 -> 4 -> 8 -> 1
    expected_sequence = [
        0x1,
        0x3,
        0x7,
        0xF,
        0xE,
        0xD,
        0xA,
        0x5,
        0xB,
        0x6,
        0xC,
        0x9,
        0x2,
        0x4,
        0x8,
        0x1,
        0x3,
        0x7,
        0xF,
        0xE
    ]

    # Check first value after reset
    actual = read_lfsr(dut)
    assert actual == expected_sequence[0], (
        f"Wrong initial value: expected {expected_sequence[0]:X}, got {actual:X}"
    )

    # Check sequence on each clock
    for expected in expected_sequence[1:]:
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")

        actual = read_lfsr(dut)
        dut._log.info(f"LFSR output = {actual:X}, expected = {expected:X}")

        assert actual == expected, (
            f"LFSR sequence failed: expected {expected:X}, got {actual:X}"
        )

        # Upper 4 bits of uo_out must remain 0
        upper_bits = int(dut.uo_out.value) >> 4
        assert upper_bits == 0, (
            f"uo_out[7:4] should be 0, got {upper_bits:X}"
        )

    # Check unused bidirectional IOs
    assert int(dut.uio_out.value) == 0x00, "uio_out should be 0"
    assert int(dut.uio_oe.value) == 0x00, "uio_oe should be 0"

    dut._log.info("4-bit LFSR test passed successfully")
