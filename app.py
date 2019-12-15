import streamlit as st
import pandas as pd
import os
import glob

st.markdown("# PuLink (Versión 1.0)")
st.markdown("## Una especie de Linkedin para sitios publicos")
st.markdown("Esta aplicación permite ver las ofertas de empleo, becas y ayudas de las entidades públicas."
            "Recogiendo todas las ofertas en un mismo sitio no será necesario buscar en cada una de dichas páginas."
            "Sugerencias porfa? :)")




@st.cache
def scrapear():
    os.system("python PuLink/spiders/fisabio.py")
    os.system("python PuLink/spiders/incliva.py")
    os.system("python PuLink/spiders/la_fe.py")
    os.system("python PuLink/spiders/manises.py")


@st.cache
def leer_datos():
    path = 'data'  # use your path
    all_files = glob.glob(path + "/*.csv")

    lista_trabajos = []
    for filename in all_files:
        datos = pd.read_csv(filename, index_col=None, header=0)
        lista_trabajos.append(datos)

    ofertas = pd.concat(lista_trabajos, axis=0, ignore_index=True,sort = False)
    ofertas.reset_index(drop=True)

    return(ofertas)


def mostrar_datos(filtered_ofertas, vista):
    if (vista == "Compacta"):

        filtered_ofertas['url'] = filtered_ofertas['url'].apply(lambda x: '<a href="{0}">Ir</a>'.format(x))
        st.markdown(filtered_ofertas.to_html(escape=False, index=False), unsafe_allow_html=True)

    if (vista == "Ligera"):
        for index, empleo in filtered_ofertas.iterrows():
            st.markdown("## [ " + empleo['titulo'] + "](" + empleo['url'] + ")")
            st.markdown("Entidad:  " + empleo['entidad'])
            st.markdown("Referencia:  " + empleo['referencia'])
            st.markdown("Ubicación:  " + empleo['ciudad'])
            st.markdown("Fecha de publicación: " + str(empleo['start_date']))
            st.markdown("Fecha final de presentación: " + str(empleo['deadline']))
            st.markdown("---")


scrapear()

ofertas = leer_datos()

# Sidebar -----------------------------------------------------------------

ciudad = st.sidebar.selectbox(
 'Ciudad:', ofertas['ciudad'].unique())

entidades = st.sidebar.multiselect(
 'Entidades disponibles:', ["FISABIO", "INCLIVA", "La Fe", "Hospital Sanitas"])

interes = st.sidebar.text_input('Buscar cargo:')

vista = st.sidebar.radio("Vista:", ["Ligera", "Compacta"])

# -------------------------------------------------------------------------

filtered_ofertas = ofertas[(ofertas['ciudad'] == ciudad)]
if (entidades):
    filtered_ofertas = filtered_ofertas[filtered_ofertas['entidad'].isin(entidades)]
if (interes):
    filtered_ofertas = filtered_ofertas[filtered_ofertas['titulo'].str.lower().str.contains(interes.lower())]


mostrar_datos(filtered_ofertas, vista)




