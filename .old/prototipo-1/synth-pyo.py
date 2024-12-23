from pyo import *

s = Server().boot()

s.amp = 0.1

a = FM().out()
b = FM().out(1)

a.ctrl(title="FM left")
b.ctrl(title="Fm right")

oscs = Sine([100, 200, 300, 400, 500, 600, 700, 800], mul = 0.1)

s.gui(locals())

