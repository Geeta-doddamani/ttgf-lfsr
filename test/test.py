import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


def get_lfsr_output(dut):
    """
    LFSR output is connected to uo_out[3:0].
    This function reads only lower 4 bits.
    """
    return int(dut.uo_out.value) & 0xF


@cocotb.test()
async def test_lfsr_4bit(dut):
    """
    Test for 4-bit LFSR Tiny Tapeout design.

    Expected sequence:
    1, 3, 7, F, E, D, A, 5, B, 6, C, 9, 2, 4, 8, then repeat.
    """

    # Start clock with 10 ns period
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply reset
    # rst_n = 0 means reset active
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    # After reset, LFSR should be seed value 0001
    await Timer(1, units="ns")
    assert get_lfsr_output(dut) == 0x1, (
        f"Reset failed: expected 1, got {get_lfsr_output(dut):X}"
    )

    # Release reset
    # rst_n = 1 means normal operation
    dut.rst_n.value = 1
    await Timer(1, units="ns")

    # Expected 4-bit LFSR sequence
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

    # First value after reset should still be 1
    actual = get_lfsr_output(dut)
    assert actual == expected_sequence[0], (
        f"Initial LFSR value wrong: expected {expected_sequence[0]:X}, got {actual:X}"
    )

    # Check remaining sequence on every clock edge
    for expected in expected_sequence[1:]:
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

        actual = get_lfsr_output(dut)

        dut._log.info(f"LFSR output = {actual:X}, expected = {expected:X}")

        assert actual == expected, (
            f"LFSR sequence wrong: expected {expected:X}, got {actual:X}"
        )

    # Check unused outputs
    assert int(dut.uo_out.value) >> 4 == 0, "Upper 4 bits of uo_out should be 0"
    assert int(dut.uio_out.value) == 0, "uio_out should be 0"
    assert int(dut.uio_oe.value) == 0, "uio_oe should be 0"

    dut._log.info("4-bit LFSR test passed successfully.")
