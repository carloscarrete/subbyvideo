import random
import string

def generar_id_aleatorio():
    caracteres = string.ascii_letters + string.digits  # letras mayúsculas, minúsculas y números
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(10))
    return id_aleatorio

# Ejemplo de uso
id_generado = generar_id_aleatorio()
print("ID generado:", id_generado)
