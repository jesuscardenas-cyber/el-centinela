from __future__ import annotations

import streamlit as st

from buscador.motor import MotorBusqueda

st.set_page_config(
    page_title="El Centinela - Scraper de noticias",
    page_icon="🔎",
    layout="wide",
)


def configurar_pagina() -> None:
    """Configura el encabezado principal de la aplicación."""

    st.title("🔎 El Centinela - Scraper de noticias")

    st.markdown(
        """
        Sistema de búsqueda y monitoreo de competencia.

        Ingresa las empresas y las palabras clave que deseas investigar.
        El sistema cruzará ambos elementos y ejecutará las búsquedas
        disponibles.
        """
    )


def obtener_lista(texto: str) -> list[str]:
    """
    Convierte un texto separado por comas o saltos de línea
    en una lista limpia.
    """

    elementos = texto.replace(",", "\n").splitlines()

    return [elemento.strip() for elemento in elementos if elemento.strip()]


def mostrar_estadisticas(estadisticas: dict) -> None:
    """Muestra las estadísticas generales de la búsqueda."""

    st.subheader("📊 Estadísticas")

    columnas = st.columns(5)

    columnas[0].metric(
        "Consultas",
        estadisticas.get("consultas", 0),
    )

    columnas[1].metric(
        "Tareas",
        estadisticas.get("tareas", 0),
    )

    columnas[2].metric(
        "Noticias encontradas",
        estadisticas.get("noticias_brutas", 0),
    )

    columnas[3].metric(
        "Noticias finales",
        estadisticas.get("noticias_finales", 0),
    )

    columnas[4].metric(
        "Tiempo",
        f"{estadisticas.get('tiempo_segundos', 0)} s",
    )


def mostrar_estadisticas_servicios(
    estadisticas: dict,
) -> None:
    """Muestra estadísticas desglosadas por servicio."""

    datos = estadisticas.get(
        "por_servicio",
        {},
    )

    if not datos:
        return

    st.subheader("🌐 Rendimiento por servicio")

    filas = []

    for servicio, valores in datos.items():
        filas.append(
            {
                "Servicio": servicio,
                "Tareas": valores.get("tareas", 0),
                "Exitosas": valores.get("exitosas", 0),
                "Fallidas": valores.get("fallidas", 0),
                "Noticias": valores.get("noticias", 0),
                "Reintentos": valores.get("reintentos", 0),
                "Tiempo promedio (s)": valores.get(
                    "tiempo_promedio",
                    0,
                ),
            }
        )

    st.dataframe(
        filas,
        width="stretch",
        hide_index=True,
    )


def preparar_resultados_para_mostrar(df):
    """
    Convierte los nombres internos del DataFrame
    a nombres amigables para la interfaz.
    """

    columnas = {
        "titulo": "Título",
        "fuente": "Fuente",
        "fecha": "Fecha",
        "servicio": "Servicio",
        "empresa": "Empresa",
        "palabra": "Palabra clave",
        "enlace": "Enlace",
    }

    columnas_disponibles = {
        interna: visible
        for interna, visible in columnas.items()
        if interna in df.columns
    }

    resultado = df[list(columnas_disponibles.keys())].copy()

    resultado.rename(
        columns=columnas_disponibles,
        inplace=True,
    )

    return resultado


def mostrar_resultados(df) -> None:
    """Muestra los resultados obtenidos."""

    st.subheader("📰 Resultados")

    if df.empty:
        st.info("No se encontraron resultados para los criterios indicados.")

        return

    st.success(f"Se encontraron {len(df)} resultados.")

    resultados_mostrar = preparar_resultados_para_mostrar(df)

    st.dataframe(
        resultados_mostrar,
        width="stretch",
        hide_index=True,
    )


def main() -> None:
    """Punto de entrada principal de la aplicación."""

    configurar_pagina()

    st.divider()

    st.subheader("🎯 Criterios de búsqueda")

    columna_empresas, columna_palabras = st.columns(2)

    with columna_empresas:
        empresas_texto = st.text_area(
            "Empresas",
            placeholder=("Ejemplo:\nLaboratorios Chopo\nLaboratorio Médico Polanco"),
            height=150,
        )

    with columna_palabras:
        palabras_texto = st.text_area(
            "Palabras clave",
            placeholder=("Ejemplo:\napertura\nexpansión\ninversión"),
            height=150,
        )

    empresas = obtener_lista(empresas_texto)

    palabras = obtener_lista(palabras_texto)

    st.caption(
        f"Empresas: {len(empresas)} | "
        f"Palabras clave: {len(palabras)} | "
        f"Consultas estimadas: "
        f"{len(empresas) * len(palabras)}"
    )

    st.divider()

    ejecutar = st.button(
        "🔎 Ejecutar búsqueda",
        type="primary",
        width="stretch",
    )

    if not ejecutar:
        return

    if not empresas:
        st.warning("Ingresa al menos una empresa.")

        return

    if not palabras:
        st.warning("Ingresa al menos una palabra clave.")

        return

    motor = MotorBusqueda()

    with st.spinner("Ejecutando búsqueda..."):
        try:
            df, estadisticas = motor.ejecutar(
                empresas,
                palabras,
            )

        except (
            RuntimeError,
            ValueError,
            KeyError,
            TypeError,
            OSError,
        ) as error:
            st.error("Ocurrió un error durante la ejecución de la búsqueda.")

            st.exception(error)

            return

    st.session_state["resultados"] = df
    st.session_state["estadisticas"] = estadisticas

    mostrar_estadisticas(estadisticas)

    mostrar_estadisticas_servicios(estadisticas)

    mostrar_resultados(df)


if __name__ == "__main__":
    main()
