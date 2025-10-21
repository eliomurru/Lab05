import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # --- SEZIONE 3: Aggiunta di nuove automobili ---
    txt_aggiungi_auto = ft.Text("Aggiungi Nuova Automobile", size=20)

    input_marca = ft.TextField(label="Marca", width=200)
    input_modello = ft.TextField(label="Modello", width=200)
    input_anno = ft.TextField(label="Anno", width=100, input_filter=ft.NumbersOnlyInputFilter())

    # --- CONTATORE POSTI ---
    posti = ft.Ref[int]()
    posti.current = 4
    txt_posti = ft.Text(f"Posti: {posti.current}", size=16)

    def incrementa_posti(e):
        posti.current += 1
        txt_posti.value = f"Posti: {posti.current}"
        page.update()

    def decrementa_posti(e):
        if posti.current > 1:
            posti.current -= 1
            txt_posti.value = f"Posti: {posti.current}"
            page.update()

    btn_meno = ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_posti)
    btn_piu = ft.IconButton(ft.Icons.ADD, on_click=incrementa_posti)
    contatore_posti = ft.Row([ btn_meno, txt_posti, btn_piu ], alignment=ft.MainAxisAlignment.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def aggiungi_automobile_handler(e):
        marca = input_marca.value.strip()
        modello = input_modello.value.strip()
        anno_str = input_anno.value.strip()

        if not (marca and modello and anno_str):
            alert.show_alert("❌ Compila tutti i campi!")
            return

        try:
            anno = int(anno_str)
            if anno < 1900 or anno > 2025:
                raise ValueError
        except ValueError:
            alert.show_alert("❌ Errore: inserisci un anno numerico valido (es. 2023).")
            return

        try:
            n_posti = int(posti.value)
        except ValueError:
            alert.show_alert("❌ Errore: inserisci un numero valido di posti.")
            return

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, n_posti)
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            posti.value = 4
            txt_posti.value = f"Posti: {posti.value}"
            aggiorna_lista_auto()
            page.update()
            alert.show_alert("✅ Automobile aggiunta correttamente!")
        except Exception as e:
            alert.show_alert(f"❌ Errore: {e}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_automobile_handler)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # Ho deciso di definirli sopra con btn_meno, btn_piu, pulsante_aggiungi_auto

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        txt_aggiungi_auto,
        ft.Row([input_marca, input_modello, input_anno], alignment=ft.MainAxisAlignment.CENTER),
        contatore_posti,
        pulsante_aggiungi_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
