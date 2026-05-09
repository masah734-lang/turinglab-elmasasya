
import yaml
from dataclasses import dataclass
from typing import Dict, Tuple, List



@dataclass
class Configuration:
    step: int
    state: str
    tape: str
    head_position: int


@dataclass
class RunResult:
    accepted: bool
    reason: str
    final_tape: str
    steps: int
    history: List[Configuration]


class Tape:
    def __init__(self, input_string: str = "", blank_symbol: str = "B"):
        self.blank_symbol = blank_symbol
        self.tape: Dict[int, str] = {}

        for i, char in enumerate(input_string):
            self.tape[i] = char

    def read(self, position: int) -> str:
        return self.tape.get(position, self.blank_symbol)

    def write(self, position: int, symbol: str) -> None:
        self.tape[position] = symbol

    def get_tape_contents(self) -> str:
        if not self.tape:
            return self.blank_symbol

        min_pos = min(self.tape.keys())
        max_pos = max(self.tape.keys())

        return "".join(self.read(i) for i in range(min_pos, max_pos + 1))

    def get_display(self, head_position: int) -> str:
        if not self.tape:
            return f"[{self.blank_symbol}]"

        min_pos = min(min(self.tape.keys()), head_position)
        max_pos = max(max(self.tape.keys()), head_position)

        result = ""

        for i in range(min_pos, max_pos + 1):
            symbol = self.read(i)

            if i == head_position:
                result += f"[{symbol}]"
            else:
                result += symbol

        return result


class SingleTapeTM:
    def __init__(
        self,
        name: str,
        states: List[str],
        input_alphabet: List[str],
        tape_alphabet: List[str],
        blank: str,
        start_state: str,
        accept_states: List[str],
        reject_states: List[str],
        transitions: Dict[Tuple[str, str], Dict[str, str]],
    ):
        self.name = name
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.start_state = start_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.transitions = transitions

    @classmethod
    def from_yaml(cls, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise ValueError(f"YAML file not found: {file_path}")
        except yaml.YAMLError as error:
            raise ValueError(f"Invalid YAML format: {error}")

        required_fields = [
            "name",
            "states",
            "input_alphabet",
            "tape_alphabet",
            "blank",
            "start_state",
            "accept_states",
            "reject_states",
            "transitions",
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        transitions = {}

        for item in data["transitions"]:
            state = item["state"]
            read = item["read"]

            transitions[(state, read)] = {
                "next": item["next"],
                "write": item["write"],
                "move": item["move"],
            }

        return cls(
            name=data["name"],
            states=data["states"],
            input_alphabet=data["input_alphabet"],
            tape_alphabet=data["tape_alphabet"],
            blank=data["blank"],
            start_state=data["start_state"],
            accept_states=data["accept_states"],
            reject_states=data["reject_states"],
            transitions=transitions,
        )

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        tape = Tape(input_string, self.blank)
        state = self.start_state
        head_position = 0
        history = []

        for step in range(max_steps + 1):
            config = Configuration(
                step=step,
                state=state,
                tape=tape.get_tape_contents(),
                head_position=head_position,
            )
            history.append(config)

            if state in self.accept_states:
                return RunResult(
                    accepted=True,
                    reason="accept",
                    final_tape=tape.get_tape_contents(),
                    steps=step,
                    history=history,
                )

            if state in self.reject_states:
                return RunResult(
                    accepted=False,
                    reason="reject",
                    final_tape=tape.get_tape_contents(),
                    steps=step,
                    history=history,
                )

            current_symbol = tape.read(head_position)
            key = (state, current_symbol)

            if key not in self.transitions:
                return RunResult(
                    accepted=False,
                    reason="no_transition",
                    final_tape=tape.get_tape_contents(),
                    steps=step,
                    history=history,
                )

            transition = self.transitions[key]

            if verbose:
                print(
                    f"Adım {step} | Durum: {state} | "
                    f"Şerit: {tape.get_display(head_position)} | "
                    f"Hareket: {transition['move']}"
                )

            tape.write(head_position, transition["write"])

            if transition["move"] == "R":
                head_position += 1
            elif transition["move"] == "L":
                head_position -= 1
            elif transition["move"] == "S":
                pass
            else:
                raise ValueError(f"Invalid move direction: {transition['move']}")

            state = transition["next"]

        return RunResult(
            accepted=False,
            reason="timeout",
            final_tape=tape.get_tape_contents(),
            steps=max_steps,
            history=history,
        )