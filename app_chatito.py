import flet as ft
import requests

API_KEY = ""
WEBHOOK_URL = "TU_WEBHOOK_DE_MACRODROID"
MODELO = "gemini-3.6-flash"

def main(page: ft.Page):
    page.title = "Chatito IA"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15

    # Lista donde se mostrarán las burbujas de chat
    chat_list = ft.ListView(expand=True, spacing=12, auto_scroll=True)
    
    # Campo de texto para escribir
    user_input = ft.TextField(
        hint_text="Escribe o habla con Chatito...",
        expand=True,
        border_radius=25,
        filled=True,
        border_color=ft.colors.TRANSPARENT
    )

    def agregar_mensaje(texto, es_usuario):
        # Crear burbujas de chat estilo app moderna
        burbuja = ft.Container(
            content=ft.Text(texto, color=ft.colors.WHITE if es_usuario else ft.colors.BLACK),
            bgcolor=ft.colors.BLUE_700 if es_usuario else ft.colors.GREY_300,
            padding=12,
            border_radius=15,
            alignment=ft.alignment.center_right if es_usuario else ft.alignment.center_left,
            margin=ft.margin.only(left=50 if es_usuario else 0, right=0 if es_usuario else 50)
        )
        chat_list.controls.append(burbuja)
        page.update()

    def enviar_mensaje(e):
        if not user_input.value.strip():
            return
        
        texto_usuario = user_input.value
        agregar_mensaje(texto_usuario, es_usuario=True)
        user_input.value = ""
        page.update()

        # Petición a la API de Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": texto_usuario}]}]}

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                resultado = response.json()
                texto_ia = resultado['candidates'][0]['content']['parts'][0]['text']
                agregar_mensaje(texto_ia, es_usuario=False)
                
                # Disparar Webhook de MacroDroid
                try:
                    requests.get(WEBHOOK_URL)
                except:
                    pass
            else:
                agregar_mensaje("Error: Límite de cuota alcanzado por hoy.", es_usuario=False)
        except Exception as ex:
            agregar_mensaje(f"Error de conexión: {ex}", es_usuario=False)
        
        page.update()

    def abrir_micrifono(e):
        # Aquí conectaremos la función de voz próximamente
        agregar_mensaje("🎤 (Micrófono activado: función de voz en desarrollo)", es_usuario=False)

    # Botones de la barra inferior (Micrófono y Enviar)
    mic_button = ft.IconButton(
        icon=ft.icons.MIC_ROUNDED,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.GREY_800,
        on_click=abrir_micrifono
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        on_click=enviar_mensaje
    )

    # Fila que junta el input de texto, el botón de voz y el de enviar
    input_row = ft.Row([user_input, mic_button, send_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    page.add(chat_list, input_row)

ft.app(target=main)
