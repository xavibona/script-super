lista_general = [
    {"supermercado": "Super A", "producto": "Yerba", "precio": 22000},
    {"supermercado": "Super B", "producto": "Yerba", "precio": 21500},
    {"supermercado": "Super C", "producto": "Yerba", "precio": 22500},
    {"supermercado": "Super A", "producto": "Azúcar", "precio": 9000},
    {"supermercado": "Super B", "producto": "Azúcar", "precio": 8800},
    {"supermercado": "Super C", "producto": "Azúcar", "precio": 8700}
]

producto_a_comparar = input("Ingrese el nombre del producto: ") #.strip() borra los caracteres seleccionados

# filtrar
lista_producto = [
    p for p in lista_general
    if p["producto"].lower() == producto_a_comparar.lower()
]

if not lista_producto:
    print("Producto no encontrado.")
else:
    # obtener precio minimo
    precio_minimo = min(lista_producto, key=lambda x: x["precio"])["precio"]

    # buscamos todos los que tengan ese precio
    mas_baratos = [
        p for p in lista_producto if p["precio"] == precio_minimo
    ]

    # print del mas barato
    if len(mas_baratos) == 1:
        print(f"El más barato está en {mas_baratos[0]['supermercado']} con precio {precio_minimo}")
    else:
        print(f"Empate en precio ({precio_minimo}) entre:")
        for p in mas_baratos:
            print(f"- {p['supermercado']}")
