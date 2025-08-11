import json

# Leer archivo JSON con precios y promociones
with open("precios.json", "r", encoding="utf-8") as f:
    precios = json.load(f)

# Ejemplo de acceso a los datos
precio_yerba = precios["SuperA"]["yerba 1kg"]["precio"]
promos_yerba = precios["SuperA"]["yerba 1kg"]["promociones"]

print("Precio Yerba 1kg:", precio_yerba)
print("Promociones Yerba 1kg:", promos_yerba)

