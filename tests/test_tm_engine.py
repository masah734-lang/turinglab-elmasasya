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

def test_empty_input():
    tape = Tape("")
    assert tape.read(0) == "B"


def test_write_blank_symbol():
    tape = Tape("1")
    tape.write(0, "B")

    assert tape.read(0) == "B"


def test_tape_display():
    tape = Tape("101")

    display = tape.get_display(1)

    assert "[0]" in display

def test_missing_yaml_fields():
    with pytest.raises(ValueError):
        SingleTapeTM.from_yaml("machines/invalid_machine.yaml")

def test_required_python_api():
    from turinglab import SingleTapeTM, RunResult

    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")

    result: RunResult = tm.run(
        input_string="1011",
        max_steps=1000,
        verbose=False
    )

    assert result.accepted is True
    assert result.final_tape.strip("B") == "1100"
    assert isinstance(result.steps, int)
    assert len(result.history) > 0

    config = result.history[5]
    assert hasattr(config, "state")
    assert hasattr(config, "tape")
    assert hasattr(config, "head_position")

def test_no_transition():
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("2", max_steps=1000)

    assert result.accepted is False
    assert result.reason == "no_transition"


#tests for the unary increment machines
def test_unary_increment_1():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")

    result = tm.run("1")

    assert result.accepted is True
    assert result.final_tape.strip("B") == "11"


def test_unary_increment_111():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")

    result = tm.run("111")

    assert result.accepted is True
    assert result.final_tape.strip("B") == "1111"


def test_unary_increment_empty():
    tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")

    result = tm.run("")

    assert result.accepted is True
    assert result.final_tape.strip("B") == "1"



# Tests for the even 'a' machine
def test_even_a_accept():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")

    result = tm.run("aa")

    assert result.accepted is True


def test_even_a_accept_4():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")

    result = tm.run("aaaa")

    assert result.accepted is True


def test_even_a_reject():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")

    result = tm.run("a")

    assert result.accepted is False
    assert result.reason == "no_transition"


def test_even_a_reject_3():
    tm = SingleTapeTM.from_yaml("machines/even_a.yaml")

    result = tm.run("aaa")

    assert result.accepted is False
    assert result.reason == "no_transition"

# Tests for the binary compare machine
def test_binary_compare_accept():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")

    result = tm.run("1#0")

    assert result.accepted is True


def test_binary_compare_reject():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")

    result = tm.run("0#1")

    assert result.accepted is False
    assert result.reason == "reject"


def test_binary_compare_accept_1011_0011():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")

    result = tm.run("1011#0011")

    assert result.accepted is True


def test_binary_compare_reject_0011_1011():
    tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")

    result = tm.run("0011#1011")

    assert result.accepted is False
    assert result.reason == "reject"

# Tests for the unary to binary machine
def test_unary_to_binary():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    # 3 (111) -> 11
    result = tm.run("111")
    assert result.accepted is True
   
def get_binary_part(tape):
    binary_part = tape.split("#")[-1].strip("B")
    return binary_part[::-1]


def test_unary_to_binary_1():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    result = tm.run("1", max_steps=1000)

    assert result.accepted is True
    assert get_binary_part(result.final_tape) == "1"


def test_unary_to_binary_2():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    result = tm.run("11", max_steps=1000)

    assert result.accepted is True
    assert get_binary_part(result.final_tape) == "10"


def test_unary_to_binary_3():
    tm = SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")
    result = tm.run("111", max_steps=1000)

    assert result.accepted is True


#def test for strnig_copy
def test_string_copy_abba():
    tm = SingleTapeTM.from_yaml("machines/string_copy.yaml")
    result = tm.run("abba", max_steps=1000)

    assert result.accepted is True
    assert result.final_tape.strip("B") == "abba#abba"


def test_string_copy_ab():
    tm = SingleTapeTM.from_yaml("machines/string_copy.yaml")
    result = tm.run("ab", max_steps=1000)

    assert result.accepted is True
    assert result.final_tape.strip("B") == "ab#ab"


def test_string_copy_a():
    tm = SingleTapeTM.from_yaml("machines/string_copy.yaml")
    result = tm.run("a", max_steps=1000)

    assert result.accepted is True
    assert result.final_tape.strip("B") == "a#a"


 #test for 4 divide machine
def test_divisible_by_4_accept_100():
    tm = SingleTapeTM.from_yaml("machines/student_choice_4Divide.yaml")
    result = tm.run("100", max_steps=1000)

    assert result.accepted is True


def test_divisible_by_4_accept_1100():
    tm = SingleTapeTM.from_yaml("machines/student_choice_4Divide.yaml")
    result = tm.run("1100", max_steps=1000)

    assert result.accepted is True


def test_divisible_by_4_accept_1000():
    tm = SingleTapeTM.from_yaml("machines/student_choice_4Divide.yaml")
    result = tm.run("1000", max_steps=1000)

    assert result.accepted is True


def test_divisible_by_4_reject_101():
    tm = SingleTapeTM.from_yaml("machines/student_choice_4Divide.yaml")
    result = tm.run("101", max_steps=1000)

    assert result.accepted is False


def test_divisible_by_4_reject_11():
    tm = SingleTapeTM.from_yaml("machines/student_choice_4Divide.yaml")
    result = tm.run("11", max_steps=1000)

    assert result.accepted is False   
  