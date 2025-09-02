# app.py - Interactive Risk Map WebApp Prototype using Streamlit
# To run locally: Install dependencies with `pip install streamlit pandas plotly`
# Then run `streamlit run app.py`
# To deploy: 
# 1. Create a GitHub repository.
# 2. Upload this app.py file and a requirements.txt file containing: streamlit\npandas\nplotly
# 3. Sign up for Streamlit Cloud[](https://share.streamlit.io/), connect your GitHub repo, and deploy.
# Once deployed, Streamlit Cloud will provide a public URL where the app is running (e.g., https://your-app-name.streamlit.app).
# Note: This is a complete, professional prototype. Data is hardcoded from the provided Excel for simplicity.
# If you need to load from file, replace the data dict with pd.read_excel('yourfile.xlsx', sheet_name='Detalle_Completo').

import streamlit as st
import pandas as pd
import plotly.express as px

# Hardcoded data from the "Detalle_Completo" sheet
data = {
    'risk_id': ['R1', 'R2', 'R3', 'R6', 'R7', 'R5', 'R12', 'R4', 'R9', 'R8', 'R11', 'R10'],
    'risk_name': [
        'Cortes masivos / microcortes y baja tensión en picos de demanda',
        'Facturación elevada / subsidios mal aplicados / consumos no reconocidos',
        'Daños en electrodomésticos por variaciones de tensión',
        'Comunicación insuficiente o tardía sobre cortes programados / de emergencia',
        'Desinformación y estafas por canales no oficiales',
        'Atención presencial: colas y tiempos de espera altos en sucursales',
        'Eventos climáticos severos (viento/tormenta) que saturan canales',
        'Demoras en reconexión tras pago',
        'Fricción en canales digitales (chat/WhatsApp/call center): tono frío, pedir \'N° de servicio\' al inicio',
        'Falta de boleta / aviso de vencimiento y corte por \'falta de pago\'',
        'Heterogeneidad de servicio por conectividad limitada en interior',
        'Trámites de conexión / medidores: demoras o percepciones de \'burocracia\''
    ],
    'category': [
        'Técnico + Comunicación',
        'Comercial + Legal/Regulatorio',
        'Técnico + Comercial + Legal',
        'Comunicaciones + Técnica',
        'Comunicaciones + Seguridad',
        'Comercial',
        'Técnico + Comunicación + Continuidad',
        'Comercial + Técnica',
        'Comunicaciones + Comercial',
        'Comercial + Comunicaciones',
        'Operación + TI',
        'Comercial + Técnica'
    ],
    'triggers': [
        'Olas de calor, fallas en red/transmisión, mantenimiento; aumento súbito de demanda',
        'Cambios tarifarios/subsidios, estimaciones de consumo, errores de facturación',
        'Baja/alta tensión, tormentas, fallas de equipos',
        'Mantenimiento, fallas imprevistas, rumores',
        'Perfiles falsos, ofertas de \'descuentos\', cadenas apócrifas',
        'Altas de servicio, facturación elevada, cortes masivos que derivan a sucursales',
        'Alertas meteorológicas, temporada estival',
        'Pagos fuera de canales EDET, validación de acreditación',
        'Protocolos centrados en dato antes que en contención',
        'Problemas de distribución de boletas, cambios de domicilio, digitalización incompleta',
        'Baja conectividad, fallas de sistemas locales, capacitaciones desparejas',
        'Picos de altas, procesos presenciales, validaciones'
    ],
    'leading_indicators': [
        'Alertas meteorológicas, picos de llamados/WhatsApp, aumentos de menciones en redes, tareas programadas',
        'Picos de consultas por monto, amparos, coberturas mediáticas, ERSEPT',
        'Reclamos por tensión, mediciones fuera de norma, picos de reportes por daños',
        'Aumento de consultas por \'sin servicio\', desinformación viral',
        'Denuncias en redes, mentions de WhatsApp no oficial, reportes de fraude',
        'Fotos/videos de filas, saturación de turnos, quejas por demoras',
        'Pronósticos SMN, demanda pico, caídas simultáneas',
        'Consultas por reconexión, colas y llamados postpago',
        'Mensajes negativos virales, abandono de interacción',
        'Reclamos \'no recibí factura\', picos de cortes por morosidad',
        'Sucursales con KPI inferiores, caídas de sistemas, quejas por \'no hay sistema\'',
        'Quejas por turnos, tiempo a alta efectiva, menciones en reclamos'
    ],
    'likelihood_1to5': [5, 4, 4, 4, 3, 4, 3, 3, 4, 3, 4, 3],
    'impact_cliente_1to5': [5, 5, 5, 4, 4, 4, 4, 4, 3, 4, 3, 3],
    'impact_reputacional_1to5': [5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
    'impact_regulatorio_1to5': [4, 5, 5, 2, 3, 2, 2, 3, 2, 3, 2, 2],
    'virality_1to5': [5, 4, 3, 4, 4, 4, 4, 3, 4, 3, 2, 2],
    'exposición_tecnológica_1to5': [4, 3, 3, 3, 3, 2, 3, 3, 3, 2, 4, 2],
    'capacidad_respuesta_actual_1to5': [3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    'owners': [
        'Técnica + Comunicaciones',
        'Comercial + Legal/Regulatorio + Comunicaciones',
        'Técnica + Comercial + Legal',
        'Comunicaciones + Técnica',
        'Comunicaciones + Seguridad + Legal',
        'Comercial',
        'Técnica + Comunicaciones + Continuidad',
        'Comercial + Técnica',
        'Comunicaciones + Comercial',
        'Comercial + Comunicaciones',
        'Operación + TI',
        'Comercial + Técnica'
    ],
    'sla_respuesta_inicial_min': [15, 30, 60, 10, 30, 15, 10, 30, 5, 30, 60, 60],
    'sla_resolucion_horas': [6, 72, 120, 2, 24, 48, 12, 24, 1, 48, 24, 72],
    'brecha_respuesta_1to5': [3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    'WRI': [4.55, 4.3, 4.15, 3.5, 3.45, 3.4, 3.3, 3.199999999999999, 3.149999999999999, 3.1, 3.05, 2.65],
    'nivel_riesgo': ['CRÍTICO', 'CRÍTICO', 'ALTO', 'ALTO', 'ALTO', 'ALTO', 'MEDIO', 'MEDIO', 'MEDIO', 'MEDIO', 'MEDIO', 'MEDIO']
}

# Hardcoded weights from "Pesos_WRI" sheet (for reference or potential recalculation)
weights = {
    'likelihood_1to5': 0.2,
    'impact_cliente_1to5': 0.2,
    'impact_reputacional_1to5': 0.15,
    'impact_regulatorio_1to5': 0.15,
    'virality_1to5': 0.1,
    'exposición_tecnológica_1to5': 0.1,
    'brecha_respuesta_1to5': 0.1
}

df = pd.DataFrame(data)

# Calculate average impact for y-axis in risk map
df['avg_impact'] = df[['impact_cliente_1to5', 'impact_reputacional_1to5', 'impact_regulatorio_1to5']].mean(axis=1)

# Streamlit App
st.set_page_config(page_title="Mapa de Riesgo Interactivo - EDET", layout="wide")

st.title("Mapa de Riesgo Interactivo - Prototipo Profesional")

st.markdown("""
Este prototipo visualiza el mapa de riesgos de atención basado en los datos proporcionados.
- **Mapa de Riesgo**: Gráfico interactivo con probabilidad vs. impacto promedio, tamaño por WRI, color por nivel de riesgo.
- **Filtros**: Por categoría y nivel de riesgo.
- **Tabla**: Detalles completos con búsqueda.
- **Detalles del Riesgo**: Selecciona un riesgo para ver información detallada.
- **Pesos WRI**: Referencia de pesos usados para calcular WRI.
""")

# Sidebar for filters
st.sidebar.header("Filtros")
categories = sorted(df['category'].unique())
selected_categories = st.sidebar.multiselect("Categorías", categories, default=categories)

niveles = sorted(df['nivel_riesgo'].unique())
selected_niveles = st.sidebar.multiselect("Niveles de Riesgo", niveles, default=niveles)

filtered_df = df[df['category'].isin(selected_categories) & df['nivel_riesgo'].isin(selected_niveles)]

# Risk Map Chart
st.header("Mapa de Riesgo")
fig = px.scatter(
    filtered_df,
    x='likelihood_1to5',
    y='avg_impact',
    size='WRI',
    color='nivel_riesgo',
    hover_name='risk_name',
    hover_data=['risk_id', 'category', 'owners', 'triggers', 'leading_indicators', 'WRI'],
    labels={
        'likelihood_1to5': 'Probabilidad (1-5)',
        'avg_impact': 'Impacto Promedio (1-5)',
        'WRI': 'Índice de Riesgo Ponderado',
        'nivel_riesgo': 'Nivel de Riesgo'
    },
    color_discrete_map={'CRÍTICO': 'red', 'ALTO': 'orange', 'MEDIO': 'yellow'}
)
fig.update_layout(
    xaxis_range=[0.5, 5.5],
    yaxis_range=[0.5, 5.5],
    height=600,
    template='plotly_white'
)
st.plotly_chart(fig, use_container_width=True)

# Interactive Table
st.header("Tabla de Riesgos")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Risk Details
st.header("Detalles de Riesgo Seleccionado")
selected_risk = st.selectbox("Selecciona un Risk ID", filtered_df['risk_id'].unique())
if selected_risk:
    risk_data = filtered_df[filtered_df['risk_id'] == selected_risk].iloc[0]
    st.subheader(f"{risk_data['risk_id']} - {risk_data['risk_name']}")
    st.write(f"**Categoría**: {risk_data['category']}")
    st.write(f"**Propietarios**: {risk_data['owners']}")
    st.write(f"**Triggers**: {risk_data['triggers']}")
    st.write(f"**Leading Indicators**: {risk_data['leading_indicators']}")
    st.write(f"**Probabilidad**: {risk_data['likelihood_1to5']}")
    st.write(f"**Impacto Cliente**: {risk_data['impact_cliente_1to5']}")
    st.write(f"**Impacto Reputacional**: {risk_data['impact_reputacional_1to5']}")
    st.write(f"**Impacto Regulatorio**: {risk_data['impact_regulatorio_1to5']}")
    st.write(f"**Virality**: {risk_data['virality_1to5']}")
    st.write(f"**Exposición Tecnológica**: {risk_data['exposición_tecnológica_1to5']}")
    st.write(f"**Brecha Respuesta**: {risk_data['brecha_respuesta_1to5']}")
    st.write(f"**WRI**: {risk_data['WRI']}")
    st.write(f"**Nivel de Riesgo**: {risk_data['nivel_riesgo']}")
    st.write(f"**SLA Respuesta Inicial (min)**: {risk_data['sla_respuesta_inicial_min']}")
    st.write(f"**SLA Resolución (horas)**: {risk_data['sla_resolucion_horas']}")

# Weights Reference
st.header("Pesos para Cálculo de WRI")
weights_df = pd.DataFrame(list(weights.items()), columns=['Factor', 'Peso'])
st.table(weights_df)

st.markdown("---")

st.caption("Prototipo desarrollado.")
