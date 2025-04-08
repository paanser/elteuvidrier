
import streamlit as st
import pandas as pd

# CONFIGURACIÓ DE PÀGINA
st.set_page_config(page_title="Pressupostador El Teu Vidrier", layout="centered")

# TÍTOL
st.title("Pressupostador El Teu Vidrier")

# CARREGAR TAULA DE MÚLTIPLES
tabla = pd.read_csv("tabla_multiplos_6x6_hasta_5m.csv", index_col=0)
tabla.columns = tabla.columns.astype(float)
tabla.index = tabla.index.astype(float)

def redondejar_multiplo(valor):
    if valor < 24:
        return 24
    elif valor > 504:
        return None
    residu = valor % 6
    return valor if residu == 0 else valor + (6 - residu)

# PAS 1: Demanar mesures
amplada = st.number_input("Amplada (cm)", min_value=1)
alcada = st.number_input("Alçada (cm)", min_value=1)

if amplada and alcada:

    # PAS 2: Mostrar m² reals
    m2_reals = round((amplada / 100) * (alcada / 100), 2)
    st.write(f"**m² reals:** {m2_reals} m²")

    # PAS 3: Mostrar m² corregits segons taula
    amplada_corr = redondejar_multiplo(amplada)
    alcada_corr = redondejar_multiplo(alcada)

    if amplada_corr in tabla.index and alcada_corr in tabla.columns:
        m2_corregits = float(tabla.loc[amplada_corr, alcada_corr])
    else:
        m2_corregits = 0
        st.error("Mesures fora del rang de la taula (24 cm a 504 cm).")

    st.write(f"**Mesures corregides:** {amplada_corr} cm x {alcada_corr} cm")
    st.write(f"**m² corregits:** {m2_corregits} m²")

    # PAS 4: Preu per m²
    preu_m2 = st.number_input("Introdueix el preu per m²", min_value=0.0, step=0.1)

    # PAS 5: Canto polit (Sí/No)
    cant_polit = st.radio("El vidre va polit?", ["Sí", "No"])

    metres_lineals = 0
    cost_cant_polit = 0

    if cant_polit == "Sí":
        # PAS 6: Costats a polir
        llargs = st.number_input("Costats llargs a polir", min_value=0, step=1)
        curts = st.number_input("Costats curts a polir", min_value=0, step=1)

        # PAS 7: Preu per metre lineal
        preu_cant = st.number_input("Preu per metre lineal de cant polit (€)", min_value=0.0, step=0.1)

        # Càlcul de metres lineals i cost
        metres_lineals = ((llargs * alcada_corr) + (curts * amplada_corr)) / 100
        cost_cant_polit = round(metres_lineals * preu_cant, 2)

    # PAS 8: Import lliure addicional
    import_extra = st.number_input("Introdueix un import extra (opcional)", min_value=0.0, step=0.1)

    # PAS 9: Marge comercial
    marge_percent = st.number_input("Vols aplicar un marge comercial (%)", min_value=0.0, step=1.0)

    # Càlculs finals
    base_vidre = round(m2_corregits * preu_m2, 2)
    subtotal_sense_marge = base_vidre + cost_cant_polit + import_extra
    marge = round(subtotal_sense_marge * (marge_percent / 100), 2)
    subtotal = subtotal_sense_marge + marge
    iva = round(subtotal * 0.21, 2)
    total = round(subtotal + iva, 2)

    # PAS 10: Mostrar resum final
    st.markdown("## Resum final")
    st.write(f"**Preu del vidre:** {base_vidre} €")
    st.write(f"**Preu del cant polit:** {cost_cant_polit} €")
    st.write(f"**Import extra:** {import_extra} €")
    st.write(f"**Marge comercial aplicat:** {marge} €")
    st.write(f"**Subtotal sense IVA:** {subtotal} €")
    st.write(f"**IVA (21%):** {iva} €")
    st.write(f"**Total amb IVA:** {total} €")
