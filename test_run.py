from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/even_a.yaml")

result = tm.run("aaa")

print(result.accepted)
print(result.reason)
print(result.final_tape)
print(result.steps)