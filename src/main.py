from tkinter import Tk, Button, Scale, Label, HORIZONTAL, Frame, StringVar, OptionMenu
from pyo import Server, Sine, LFO, Adsr, Biquad

# Configuración inicial de PyO
server = Server().boot()
server.start()

# Crear la ventana principal
root = Tk()
root.title("Sintetizador con PyO")

# Variables globales para manejar el sonid
current_sound = None
adsr = None
filter_node = None  # Nodo para el filtro
wave_type = StringVar(root)  # Variable para el tipo de onda, asociada a la ventana
wave_type.set("Sine")  # Valor inicial: onda senoidal

# Función para generar sonido con ADSR, filtro y tipo de onda
def play_sound(freq):
    global current_sound, adsr, filter_node
    if current_sound:
        current_sound.stop()
    
    # Crear envolvente ADSR con los valores actuales
    adsr = Adsr(
        attack=max(attack.get() / 1000, 0.01),  # Ataque mínimo de 10 ms
        decay=decay.get() / 1000,
        sustain=0,  # Valor fijo para sustain
        release=0.3,  # Valor predeterminado para release
        mul=volume.get() / 100
    )
    
    # Seleccionar el tipo de oscilador según la onda elegida
    if wave_type.get() == "Sine":
        osc = Sine(freq=freq, mul=adsr)
    else:
        waveforms = {"Square": 1, "Sawtooth": 2, "Triangle": 3}
        osc = LFO(freq=freq, type=waveforms[wave_type.get()], mul=adsr)
    
    # Aplicar filtro pasabajo
    filter_node = Biquad(
        osc, 
        freq=filter_freq.get(),  # Control lineal de frecuencia
        q=filter_res.get(),  # Ajuste de resonancia
        type=0
    ).out()
    adsr.play()

# Función para detener el sonido
def stop_sound():
    global current_sound
    if current_sound:
        current_sound.stop()

# Frame para el teclado
keyboard_frame = Frame(root)
keyboard_frame.pack()

# Configuración de notas (dos octavas: C3 a B4)
notes = [
    ("C3", 130.81), ("C#3", 138.59), ("D3", 146.83), ("D#3", 155.56), ("E3", 164.81),
    ("F3", 174.61), ("F#3", 185.00), ("G3", 196.00), ("G#3", 207.65), ("A3", 220.00),
    ("A#3", 233.08), ("B3", 246.94),
    ("C4", 261.63), ("C#4", 277.18), ("D4", 293.66), ("D#4", 311.13), ("E4", 329.63),
    ("F4", 349.23), ("F#4", 369.99), ("G4", 392.00), ("G#4", 415.30), ("A4", 440.00),
    ("A#4", 466.16), ("B4", 493.88)
]

# Crear teclas del teclado
for i, (note, freq) in enumerate(notes):
    color = "black" if "#" in note else "white"
    btn = Button(keyboard_frame, text=note, bg=color, fg="white" if color == "black" else "black",
                 width=5, height=10, command=lambda f=freq: play_sound(f))
    btn.grid(row=0, column=i, padx=1, pady=1)
    btn.bind("<ButtonRelease-1>", lambda event: stop_sound())

# Frame para controles
controls_frame = Frame(root)
controls_frame.pack(pady=10)

# Volumen
volume_frame = Frame(controls_frame, relief="groove", bd=2)
volume_frame.pack(side="left", padx=5, pady=5)
Label(volume_frame, text="Volumen").pack()
volume = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL)
volume.set(50)
volume.pack()

# ADSR (sin sustain ni release)
adsr_frame = Frame(controls_frame, relief="groove", bd=2)
adsr_frame.pack(side="left", padx=5, pady=5)
Label(adsr_frame, text="ADSR").pack()
Label(adsr_frame, text="Attack (ms)").pack()
attack = Scale(adsr_frame, from_=10, to=5000, orient=HORIZONTAL)
attack.set(100)
attack.pack()

Label(adsr_frame, text="Decay (ms)").pack()
decay = Scale(adsr_frame, from_=0, to=5000, orient=HORIZONTAL)
decay.set(200)
decay.pack()

# Filtro
filter_frame = Frame(controls_frame, relief="groove", bd=2)
filter_frame.pack(side="left", padx=5, pady=5)
Label(filter_frame, text="Filtro").pack()

# Escala para la frecuencia de corte del filtro
Label(filter_frame, text="Frecuencia de Corte (Hz)").pack()
filter_freq = Scale(filter_frame, from_=0, to=10000, orient=HORIZONTAL, resolution=50)
filter_freq.set(1000)  # Valor inicial
filter_freq.pack()

# Escala para la resonancia del filtro
Label(filter_frame, text="Resonancia (Q)").pack()
filter_res = Scale(filter_frame, from_=0.1, to=10.0, orient=HORIZONTAL, resolution=1)
filter_res.set(1.0)  # Valor inicial
filter_res.pack()

# Forma de Onda
wave_frame = Frame(controls_frame, relief="groove", bd=2)
wave_frame.pack(side="left", padx=5, pady=5)
Label(wave_frame, text="Forma de Onda").pack()
wave_menu = OptionMenu(wave_frame, wave_type, "Sine", "Square", "Sawtooth", "Triangle")
wave_menu.pack()

# Iniciar la interfaz
root.mainloop()

# Finalizar el servidor de PyO al cerrar
server.stop()
server.shutdown()
