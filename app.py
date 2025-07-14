
import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
# Debes subir tu archivo de credenciales JSON al mismo directorio
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(credentials)

# Reemplaza esto con el nombre de tu hoja de cálculo
SPREADSHEET_NAME = "Pagos Promo CVI"
spreadsheet = client.open(SPREADSHEET_NAME)

# Detectar mes actual y hoja correspondiente
mes_actual = datetime.datetime.now().strftime("%B").upper()
try:
    worksheet = spreadsheet.worksheet(mes_actual)
except:
    worksheet = spreadsheet.add_worksheet(title=mes_actual, rows="1000", cols="20")
    worksheet.append_row(["Fecha", "Nombre", "Monto", "Moneda", "Tipo de Cuota", "Método", "Referencia", "Nota"])

# --- INTERFAZ DE LA APP ---
st.title("Registro de Pagos - Promo CVI")

with st.form("form_pago"):
    nombre = st.selectbox("Nombre del alumno", [
        "PEDRO SAMUEL ACOSTA GARCIA",
        "MARIANA ACOSTA LA ROSA",
        "CLEIVER ACUÑA",
        "VICTORIA VALENTINA AGUIAR MORALES",
        "VALERIA ALFONZO",
        "ADRIAN JOSE ALVAREZ MARCANO",
        "ERNESTO ARRIOJAS",
        "ISABELLA ANTONIETA BARRETO RODRIGUEZ"
        # Puedes seguir agregando más
    ])
    fecha = st.date_input("Fecha del pago", datetime.date.today())
    monto = st.number_input("Monto", min_value=0.0, step=0.5)
    moneda = st.selectbox("Moneda", ["$", "Bs"])
    tipo_cuota = st.selectbox("Tipo de cuota", ["C1", "C2", "PR"])
    metodo = st.selectbox("Método de pago", ["EFECTIVO ($)", "PAGO MÓVIL", "ZELLE", "BINANCE", "TRANSFERENCIA"])
    referencia = st.text_input("Referencia (opcional)")
    nota = st.text_area("Nota (opcional)")

    submitted = st.form_submit_button("Registrar pago")

    if submitted:
        nueva_fila = [str(fecha), nombre, monto, moneda, tipo_cuota, metodo, referencia, nota]
        worksheet.append_row(nueva_fila)
        st.success("✅ Pago registrado correctamente.")
