# Importamos los módulos necesarios
import tkinter as tk
from tkinter import messagebox, scrolledtext
from backend import CifradoManager  # Importamos la clase de cifrado desde el backend

# Intentamos importar Hovertip para mostrar ayudas emergentes
try:
    from idlelib.tooltip import Hovertip
except ImportError:
    # Si no está disponible, definimos una función nula
    Hovertip = lambda widget, text: None

class App:
    def __init__(self, root):
        """
        Constructor de la clase App. Configura toda la interfaz gráfica (GUI) para cifrar y descifrar mensajes.
        """
        self.root = root
        self.root.title("Cifrado de Mensajes")
        self.root.geometry("800x500")
        self.root.configure(bg='#1e1e2f')

        # Estilos generales para frames y labels
        style_frame = {"bg": "#2e2e3e", "fg": "white", "padx": 10, "pady": 10, "bd": 2, "relief": tk.RIDGE}
        style_label = {"bg": "#2e2e3e", "fg": "white", "font": ("Arial", 11)}

        # Creamos dos frames principales: Cifrar y Descifrar
        self.frame_cifrar = tk.LabelFrame(root, text="Cifrar Mensaje", **style_frame)
        self.frame_descifrar = tk.LabelFrame(root, text="Descifrar Mensaje", **style_frame)
        self.frame_cifrar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_descifrar.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configuración de expansión en la ventana principal
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # === Sección de CIFRAR ===
        tk.Label(self.frame_cifrar, text="Mensaje a cifrar:", **style_label).pack(anchor="w")
        self.entrada_mensaje = scrolledtext.ScrolledText(self.frame_cifrar, wrap=tk.WORD, height=5)
        self.entrada_mensaje.pack(fill="both", padx=5, pady=5)
        Hovertip(self.entrada_mensaje, "Ingresa el texto plano que deseas cifrar.")

        tk.Label(self.frame_cifrar, text="Clave de cifrado:", **style_label).pack(anchor="w")
        self.entrada_clave = tk.Entry(self.frame_cifrar, show='*')
        self.entrada_clave.pack(fill="x", padx=5, pady=5)
        Hovertip(self.entrada_clave, "Debe contener mayúsculas, números y símbolos.")

        self.boton_cifrar = tk.Button(self.frame_cifrar, text="Cifrar", command=self.cifrar, bg="#4e88ff", fg="white")
        self.boton_cifrar.pack(pady=4, fill="x")

        self.boton_limpiar_cifrar = tk.Button(self.frame_cifrar, text="Limpiar", command=self.limpiar_cifrado, bg="#ff5c5c", fg="white")
        self.boton_limpiar_cifrar.pack(pady=2, fill="x")

        self.resultado_cifrado = scrolledtext.ScrolledText(self.frame_cifrar, wrap=tk.WORD, height=5, state='disabled')
        self.resultado_cifrado.pack(fill="both", padx=5, pady=5)

        # === Sección de DESCIFRAR ===
        tk.Label(self.frame_descifrar, text="Texto cifrado:", **style_label).pack(anchor="w")
        self.entrada_cifrado = scrolledtext.ScrolledText(self.frame_descifrar, wrap=tk.WORD, height=5)
        self.entrada_cifrado.pack(fill="both", padx=5, pady=5)
        Hovertip(self.entrada_cifrado, "Ingresa el texto cifrado a descifrar.")

        tk.Label(self.frame_descifrar, text="Clave usada para cifrar:", **style_label).pack(anchor="w")
        self.entrada_clave_descifrar = tk.Entry(self.frame_descifrar, show='*')
        self.entrada_clave_descifrar.pack(fill="x", padx=5, pady=5)

        self.boton_descifrar = tk.Button(self.frame_descifrar, text="Descifrar", command=self.descifrar, bg="#4ed36d", fg="white")
        self.boton_descifrar.pack(pady=4, fill="x")

        self.boton_limpiar_descifrar = tk.Button(self.frame_descifrar, text="Limpiar", command=self.limpiar_descifrado, bg="#ff5c5c", fg="white")
        self.boton_limpiar_descifrar.pack(pady=2, fill="x")

        self.resultado_descifrado = scrolledtext.ScrolledText(self.frame_descifrar, wrap=tk.WORD, height=5, state='disabled')
        self.resultado_descifrado.pack(fill="both", padx=5, pady=5)

        # Variable para almacenar configuración de cifrado
        self.configuracion_cifrado = None

    def cifrar(self):
        """
        Obtiene el mensaje y la clave ingresados, aplica el cifrado y muestra el resultado en la interfaz.
        """
        mensaje = self.entrada_mensaje.get("1.0", tk.END).strip()
        clave = self.entrada_clave.get()
        try:
            gestor = CifradoManager(clave)
            resultado = gestor.cifrar(mensaje)
            self.configuracion_cifrado = gestor.obtener_configuracion()

            self.resultado_cifrado.configure(state='normal')
            self.resultado_cifrado.delete("1.0", tk.END)
            self.resultado_cifrado.insert(tk.END, resultado)
            self.resultado_cifrado.configure(state='disabled')
        except ValueError as e:
            messagebox.showerror("Error de Clave", str(e))

    def descifrar(self):
        """
        Obtiene el texto cifrado y la clave ingresados, aplica el descifrado y muestra el resultado en la interfaz.
        """
        texto_cifrado = self.entrada_cifrado.get("1.0", tk.END).strip()
        clave = self.entrada_clave_descifrar.get()

        try:
            gestor = CifradoManager(clave)
            if self.configuracion_cifrado:
                gestor.cargar_configuracion(self.configuracion_cifrado)
            else:
                messagebox.showwarning("Advertencia", "No hay configuración previa de cifrado cargada.")

            resultado = gestor.descifrar(texto_cifrado)
            self.resultado_descifrado.configure(state='normal')
            self.resultado_descifrado.delete("1.0", tk.END)
            self.resultado_descifrado.insert(tk.END, resultado)
            self.resultado_descifrado.configure(state='disabled')
        except ValueError as e:
            messagebox.showerror("Error de Clave", str(e))

    def limpiar_cifrado(self):
        """
        Limpia los campos de entrada y resultado de la sección de cifrado.
        """
        self.entrada_mensaje.delete("1.0", tk.END)
        self.resultado_cifrado.configure(state='normal')
        self.resultado_cifrado.delete("1.0", tk.END)
        self.resultado_cifrado.configure(state='disabled')

    def limpiar_descifrado(self):
        """
        Limpia los campos de entrada y resultado de la sección de descifrado.
        """
        self.entrada_cifrado.delete("1.0", tk.END)
        self.resultado_descifrado.configure(state='normal')
        self.resultado_descifrado.delete("1.0", tk.END)
        self.resultado_descifrado.configure(state='disabled')

# Ejecutamos la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
