import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Función para iniciar historial en memoria
def iniciar_historial():
    return [
        {"role": "system", "content": "Eres un asistente útil y conversacional."}
    ]

# Inicializar historial en memoria
historial_mensajes = iniciar_historial()

# Guardar en historial.txt
def guardar_en_archivo(pregunta, respuesta):
    with open("historial.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"🟢 Pregunta: {pregunta}\n")
        archivo.write(f"🤖 Respuesta: {respuesta}\n")
        archivo.write("-" * 40 + "\n")

# Mostrar historial.txt
def mostrar_historial():
    if os.path.exists("historial.txt"):
        with open("historial.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            print("\n📜 HISTORIAL GUARDADO:\n")
            print(contenido)
    else:
        print("\n(El historial.txt aún no existe o está vacío)\n")

# Borrar historial.txt
def borrar_historial():
    if os.path.exists("historial.txt"):
        open("historial.txt", "w").close()
        print("\n🗑️ Historial borrado exitosamente.\n")
    else:
        print("\n(El archivo historial.txt no existe todavía)\n")

# Preguntar a ChatGPT con contexto
def preguntar_a_chatgpt(pregunta):
    historial_mensajes.append({"role": "user", "content": pregunta})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historial_mensajes
    )
    respuesta = response.choices[0].message.content.strip()
    historial_mensajes.append({"role": "assistant", "content": respuesta})
    guardar_en_archivo(pregunta, respuesta)
    return respuesta

# Mostrar menú
def mostrar_menu():
    print("\n🔹 OPCIONES DISPONIBLES:")
    print("[1] Hacer una pregunta")
    print("[2] Ver historial guardado")
    print("[3] Resetear conversación")
    print("[4] Borrar historial")
    print("[5] Salir")

# Programa principal con menú
if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción (1-5): ")

        if opcion == "1":
            pregunta = input("\n🟢 Tu pregunta: ")
            respuesta = preguntar_a_chatgpt(pregunta)
            print(f"\n🤖 Respuesta:\n{respuesta}\n")

        elif opcion == "2":
            mostrar_historial()

        elif opcion == "3":
            historial_mensajes = iniciar_historial()
            print("\n♻️ Conversación reiniciada. El contexto se ha borrado.\n")

        elif opcion == "4":
            borrar_historial()

        elif opcion == "5":
            print("\n👋 ¡Hasta luego, Carlos!\n")
            break

        else:
            print("\n❗ Opción no válida. Intenta de nuevo.\n")

