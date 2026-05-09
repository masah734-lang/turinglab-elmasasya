import pytest
from turinglab.tm_engine import Tape, SingleTapeTM


def test_tape_read_write():
    tape = Tape("101")

    assert tape.read(0) == "1"
    assert tape.read(1) == "0"
    assert tape.read(2) == "1"
    assert tape.read(3) == "B"

    tape.write(1, "1")

    assert tape.read(1) == "1"


def test_tape_contents():
    tape = Tape("101")
    assert tape.get_tape_contents() == "101"


def test_from_yaml_loads_machine():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")

    assert tm.name == "binary_increment"
    assert tm.start_state == "q0"
    assert "q_accept" in tm.accept_states


def test_binary_increment_1011():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011", max_steps=1000)

    assert result.accepted is True
    assert result.reason == "accept"
    assert result.final_tape.strip("B") == "1100"


def test_binary_increment_0():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("0", max_steps=1000)

    assert result.accepted is True
    assert result.final_tape.strip("B") == "1"


def test_binary_increment_111():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("111", max_steps=1000)

    assert result.accepted is True
    assert result.final_tape.strip("B") == "1000"


def test_history_is_recorded():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011", max_steps=1000)

    assert len(result.history) > 0
    assert result.history[0].state == "q0"
    assert result.history[0].head_position == 0


def test_timeout():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011", max_steps=1)

    assert result.accepted is False
    assert result.reason == "timeout"


def test_invalid_yaml_file():
    with pytest.raises(ValueError):
        SingleTapeTM.from_yaml("machines/file_not_found.yaml")


def test_verbose_output(capsys):
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    tm.run("1", max_steps=1000, verbose=True)

    captured = capsys.readouterr()

    assert "Adım" in captured.out
    assert "Durum" in captured.out
    assert "Şerit" in captured.out