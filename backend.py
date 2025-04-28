# Importamos el módulo 're' para trabajar con expresiones regulares
import re

class CifradoManager:
    # Diccionario para aplicar la sustitución de caracteres
    SUBSTITUCION = {'j': '2', 'u': '7', 'a': '8', 'r': '1', 'y': '0'}
    # Diccionario inverso para revertir la sustitución
    SUBSTITUCION_INV = {v: k for k, v in SUBSTITUCION.items()}

    def __init__(self, clave):
        """
        Constructor de la clase. Inicializa los atributos necesarios
        y valida que la clave cumpla los requisitos de seguridad.
        """
        self.clave = clave
        self.orden = []
        self.columnas = 0
        self.espacios = []

        # Validamos la clave al crear el objeto
        es_valida, mensaje = self.validar_clave(clave)
        if not es_valida:
            raise ValueError(mensaje)

    def validar_clave(self, clave, min_longitud=6, max_longitud=20):
        """
        Valida que la clave cumpla con los requisitos de longitud,
        inclusión de mayúsculas, números y caracteres especiales.
        """
        if len(clave) < min_longitud or len(clave) > max_longitud:
            return False, f"La clave debe tener entre {min_longitud} y {max_longitud} caracteres."
        if not re.search(r"[A-Z]", clave):
            return False, "La clave debe contener al menos una letra mayúscula."
        if not re.search(r"[0-9]", clave):
            return False, "La clave debe contener al menos un número."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", clave):
            return False, "La clave debe contener al menos un caracter especial."
        return True, "Clave válida."

    def aplicar_sustitucion(self, texto):
        """
        Aplica el diccionario de sustitución sobre el texto ingresado.
        """
        return ''.join(self.SUBSTITUCION.get(c.lower(), c) for c in texto)

    def revertir_sustitucion(self, texto):
        """
        Revierte la sustitución aplicada previamente en el texto.
        """
        return ''.join(self.SUBSTITUCION_INV.get(c, c) for c in texto)

    def cifrar(self, mensaje):
        """
        Cifra el mensaje aplicando primero la sustitución de caracteres
        y luego una transposición basada en la clave.
        """
        # Aplicar sustitución al mensaje
        mensaje = self.aplicar_sustitucion(mensaje)

        # Guardar las posiciones de los espacios
        self.espacios = [i for i, c in enumerate(mensaje) if c == ' ']

        # Eliminar los espacios para formar la matriz
        limpio = ''.join(c for c in mensaje if c != ' ')

        # Definir dimensiones de la matriz
        self.columnas = len(self.clave)
        filas = (len(limpio) + self.columnas - 1) // self.columnas

        # Construir la matriz fila por fila
        matriz = []
        for i in range(filas):
            fila = list(limpio[i * self.columnas:(i + 1) * self.columnas])
            while len(fila) < self.columnas:
                fila.append(' ')  # Rellenar filas incompletas
            matriz.append(fila)

        # Determinar el orden de columnas según los caracteres de la clave
        self.orden = sorted(range(self.columnas), key=lambda x: ord(self.clave[x]))

        # Leer la matriz siguiendo el nuevo orden de columnas
        cifrado = ''.join(matriz[fila][col] for col in self.orden for fila in range(filas))
        return cifrado.rstrip()

    def descifrar(self, texto_cifrado):
        """
        Descifra el mensaje transpuesto y sustituido,
        restaurando la estructura original y los espacios.
        """
        # Calcular el número de filas y columnas
        filas = len(texto_cifrado) // self.columnas
        sobrante = len(texto_cifrado) % self.columnas

        # Reconstruir columnas de acuerdo al texto cifrado
        columnas_data = []
        idx = 0
        for i in range(self.columnas):
            long_col = filas + (1 if i < sobrante else 0)
            columnas_data.append(list(texto_cifrado[idx:idx + long_col]))
            idx += long_col

        # Reorganizar columnas en su orden original
        columnas_original = [None] * self.columnas
        for i, pos in enumerate(self.orden):
            columnas_original[pos] = columnas_data[i]

        # Reconstruir el mensaje fila por fila
        descifrado = []
        for fila in range(filas + (1 if sobrante > 0 else 0)):
            for col in range(self.columnas):
                if fila < len(columnas_original[col]):
                    descifrado.append(columnas_original[col][fila])

        # Eliminar relleno extra y restaurar espacios
        texto_plano = ''.join(descifrado).rstrip()
        if self.espacios:
            for pos in self.espacios:
                if pos <= len(texto_plano):
                    texto_plano = texto_plano[:pos] + ' ' + texto_plano[pos:]
        return self.revertir_sustitucion(texto_plano)

    def obtener_configuracion(self):
        """
        Devuelve un diccionario con los parámetros actuales
        del cifrado para permitir su reutilización.
        """
        return {
            "clave": self.clave,
            "orden": self.orden,
            "columnas": self.columnas,
            "espacios": self.espacios
        }

    def cargar_configuracion(self, config):
        """
        Carga una configuración previa de cifrado
        para permitir el descifrado correcto.
        """
        self.clave = config["clave"]
        self.orden = config["orden"]
        self.columnas = config["columnas"]
        self.espacios = config["espacios"]
