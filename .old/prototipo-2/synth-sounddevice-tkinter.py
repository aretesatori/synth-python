import tkinter as tk
import sounddevice as sd
import numpy as np

# Frecuencias musicales para las teclas del piano (incluyendo sostenidos y octava inferior)
KEY_FREQUENCIES = {
    'C': 523.25,  # C4 (Do)
    'C#': 554.37, # C#4 (Do#)
    'D': 587.33,  # D4 (Re)
    'D#': 622.25, # D#4 (Re#)
    'E': 659.25,  # E4 (Mi)
    'F': 698.46,  # F4 (Fa)
    'F#': 739.99, # F#4 (Fa#)
    'G': 783.99,  # G4 (Sol)
    'G#': 830.61, # G#4 (Sol#)
    'A': 880.00,  # A4 (La)
    'A#': 932.33, # A#4 (La#)
    'B': 987.77,  # B4 (Si)
    'C3': 261.63, # C3 (Do bajo)
    'C#3': 277.18, # C#3 (Do# bajo)
    'D3': 293.66, # D3 (Re bajo)
    'D#3': 311.13, # D#3 (Re# bajo)
    'E3': 329.63, # E3 (Mi bajo)
    'F3': 349.23, # F3 (Fa bajo)
    'F#3': 369.99, # F#3 (Fa# bajo)
    'G3': 392.00, # G3 (Sol bajo)
    'G#3': 415.30, # G#3 (Sol# bajo)
    'A3': 440.00,  # A3 (La bajo)
    'A#3': 466.16, # A#3 (La# bajo)
    'B3': 493.88  # B3 (Si bajo)
}

# Parámetros del sonido
SAMPLE_RATE = 44100  # Frecuencia de muestreo
DURATION = 0.5       # Duración de la nota

# def generate_wave(frequency, duration, sample_rate):
#     """Genera una onda sinusoidal de una frecuencia dada"""
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     wave = 0.5 * np.sin(2 * np.pi * frequency * t)
#     return wave

def generate_wave(frequency, duration, sample_rate):
    """Genera una onda cuadrada de una frecuencia dada"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave1 = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))  # Onda cuadrada
    wave2 = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = wave1 + 2*wave2
    return wave


def play_tone(frequency):
    """Reproduce una nota con una frecuencia específica"""
    wave = generate_wave(frequency, DURATION, SAMPLE_RATE)
    sd.play(wave, SAMPLE_RATE)
    sd.wait()

def on_key_press(event):
    """Maneja el evento de pulsación de tecla"""
    key = event.char.upper()
    if key in KEY_FREQUENCIES:
        play_tone(KEY_FREQUENCIES[key])

def create_piano_gui(root):
    """Crea la interfaz gráfica del piano"""
    label = tk.Label(root, text="Sintetizador", font=("Arial", 24))
    label.pack()

    # Crear botones para las teclas blancas y negras del piano
    white_frame = tk.Frame(root)
    white_frame.pack(pady=10)
    black_frame = tk.Frame(root)
    black_frame.pack()

    # Octava inferior
    for key in ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3']:
        button = tk.Button(white_frame, text=key, width=5, height=3, font=("Arial", 18),
                           command=lambda k=key: play_tone(KEY_FREQUENCIES[k]))
        button.pack(side=tk.LEFT)

    # Notas negras de la octava inferior
    for key in ['C#3', 'D#3', '', 'F#3', 'G#3', 'A#3', '']:
        if key:
            button = tk.Button(black_frame, text=key, width=3, height=2, font=("Arial", 12),
                               bg='black', fg='white',
                               command=lambda k=key: play_tone(KEY_FREQUENCIES[k]))
            button.pack(side=tk.LEFT)
        else:
            spacer = tk.Label(black_frame, text="  ", width=3, height=2)
            spacer.pack(side=tk.LEFT)

    # Octava superior
    for key in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        button = tk.Button(white_frame, text=key, width=5, height=3, font=("Arial", 18),
                           command=lambda k=key: play_tone(KEY_FREQUENCIES[k]))
        button.pack(side=tk.LEFT)

    # Notas negras de la octava superior
    for key in ['C#', 'D#', '', 'F#', 'G#', 'A#', '']:
        if key:
            button = tk.Button(black_frame, text=key, width=3, height=2, font=("Arial", 12),
                               bg='black', fg='white',
                               command=lambda k=key: play_tone(KEY_FREQUENCIES[k]))
            button.pack(side=tk.LEFT)
        else:
            spacer = tk.Label(black_frame, text="  ", width=3, height=2)
            spacer.pack(side=tk.LEFT)

    # Instrucción para tocar con teclado
    instruction = tk.Label(root, text="Use the keys C, D, E, F, G, A, B on your keyboard",
                           font=("Arial", 14))
    instruction.pack(pady=10)

# Crear la ventana principal
root = tk.Tk()
root.title("Sintetizador")

create_piano_gui(root)

# Ligar las teclas del teclado a la reproducción de notas
root.bind("<KeyPress>", on_key_press)

# Iniciar el bucle principal de la interfaz
root.mainloop()
