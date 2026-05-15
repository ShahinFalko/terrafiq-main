import streamlit as st
import pandas as pd
import requests
import folium
import plotly.express as px
from streamlit_folium import st_folium
from datetime import datetime

# --- 1. SETUP & STYLE ---
st.set_page_config(page_title="Terrafiq Matrix Control v2.9.9", layout="wide")

# Custom CSS für "Control Center" Look & Zentrierung
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .result-box {
        background-color: #1e3d2b;
        color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        border-left: 8px solid #2ecc71;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .digital-clock {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        color: #ff4500;
        text-align: right;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 0px;
        text-shadow: 0 0 10px #ff4500;
    }
    .live-label {
        font-size: 14px;
        color: #95a5a6;
        text-align: right;
        margin-top: -5px;
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    
    /* Zentrierung für die Tabelle */
    .stDataFrame div[data-testid="stTable"] div {
        text-align: center !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

API_URL = "https://1vlp62sdx7.execute-api.eu-central-1.amazonaws.com/calculate"

NODES = {
    'M_WEST': {'lat': 48.17, 'lon': 11.40, 'name': 'München West'},
    'HOLZ_K': {'lat': 47.88, 'lon': 11.70, 'name': 'Holzkirchen'},
    'AUG_O':  {'lat': 48.40, 'lon': 10.93, 'name': 'Augsburg Ost'},
    'LDS_L':  {'lat': 48.04, 'lon': 10.87, 'name': 'Landsberg a.L.'},
    'JET_S':  {'lat': 48.41, 'lon': 10.43, 'name': 'Jettingen-S.'},
    'MEM_M':  {'lat': 47.98, 'lon': 10.18, 'name': 'Memmingen'},
    'ULM_E':  {'lat': 48.45, 'lon': 10.08, 'name': 'Ulm-Elchingen'},
    'HDH_M':  {'lat': 48.67, 'lon': 10.15, 'name': 'Heidenheim'},
    'AAL_W':  {'lat': 48.88, 'lon': 10.18, 'name': 'Aalen'},
    'KIR_T':  {'lat': 48.64, 'lon': 9.45,  'name': 'Kirchheim u.T.'},
    'STR_K':  {'lat': 48.78, 'lon': 9.18,  'name': 'Stuttgart Kreuz'},
    'ESS_L':  {'lat': 48.74, 'lon': 9.31,  'name': 'Esslingen'}, 
    'WAI_B':  {'lat': 48.83, 'lon': 9.32,  'name': 'Waiblingen'},
    'KOR_W':  {'lat': 48.86, 'lon': 9.18,  'name': 'Kornwestheim'}
}

name_to_id = {node_data['name']: node_id for node_id, node_data in NODES.items()}

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("🏛️ TERRAFIQ v2.9.9")
    st.info("Echtzeit-Matrix: Topographie & Autobahn-Mapping aktiv.")
    
    start_name = st.selectbox("Startpunkt (München/Umland)", list(name_to_id.keys()), index=0)
    start_node = name_to_id[start_name]
    
    end_name = st.selectbox("Zielpunkt (Stuttgart/Korridor)", list(name_to_id.keys()), index=13)
    end_node = name_to_id[end_name]
    
    st.markdown("---")
    
    # --- ZEITPLANUNG (PREDICTIVE MODE - COMING SOON) ---
    st.subheader("⏰ Zeitplanung (Predictive)")
    st.caption("🚀 COMING SOON: KI-Prognose für Ankunftszeit.")
    c1, c2 = st.columns(2)
    # Nutze text_input statt Slider für den "Disabled"-Look ohne Fehler
    c1.text_input("Stunde", value=datetime.now().hour, disabled=True)
    c2.text_input("Minute", value="00", disabled=True)
    uhr = datetime.now().hour 
    
    st.markdown("---")
    st.subheader("🔧 TCO Faktoren")
    user_lohn = st.number_input("Fahrerlohn (€/h)", value=35)
    user_verschleiss = st.number_input("Verschleiß (€/km)", value=0.38, format="%.2f")
    
    st.markdown("---")
    st.caption("Datenquelle: TomTom Live Traffic, OpenWeather, Tankerkönig")

    # --- DEIN PORTFOLIO-BRANDING ---
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: left; font-size: 13px; color: #95a5a6; border-left: 3px solid #ff4500; padding-left: 10px;'>
            <b>Entwickelt von Shahin</b><br>
            Cloud-basierte TCO-Optimierung für den Güterkraftverkehr auf AWS.<br><br>
            <a href='https://www.linkedin.com/in/shahin-sharifi-najafabadi-47219b219' target='_blank' style='color: #3498db; text-decoration: none;'>🔗 Kontakt auf LinkedIn</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- 3. BERECHNUNG ---
if start_node == end_node:
    st.warning("⚠️ Start und Ziel sind identisch.")
else:
    now = datetime.now()
    st.markdown(f'<p class="digital-clock">{now.strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="live-label">LIVE-ANALYSE STAND: {now.strftime("%d.%m.%Y")}</p>', unsafe_allow_html=True)

    payload = {
        "start": start_node, "end": end_node, 
        "lohn": user_lohn, "verschleiss": user_verschleiss, "stunde": uhr
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            
            if len(data) > 0:
                best = data[0]

                # --- 4. ANZEIGE ---
                delay = best.get('traffic_delay_min', 0)
                clean_route = best['route'].replace("(", "").replace(")", "")
                
                st.markdown(f'<div class="result-box">🏆 BESTE ROUTE: {clean_route}</div>', unsafe_allow_html=True)

                if delay > 10:
                    st.error(f"⚠️ KRITISCHER STAU: +{delay} Min Verzögerung auf der Optimal-Route!")
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Gesamtkosten (TCO)", f"{best['gesamt_kosten_euro']} €")
                m2.metric("Echtzeit-Dauer", f"{best['zeit_h']} h", delta=f"{delay} min Stau", delta_color="inverse")
                m3.metric("CO2 Footprint", f"{best.get('co2_kg', 0)} kg")
                m4.metric("Distanz", f"{best['distanz_km']} km")

                col_l, col_r = st.columns(2)
                
                with col_l:
                    fig = px.bar(pd.DataFrame(data), x='rank', 
                                 y=['sprit_kosten', 'lohn_kosten', 'maut_kosten', 'verschleiss_kosten'], 
                                 title="Kosten-Struktur inkl. Topographie", barmode='stack', template="plotly_dark",
                                 color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_r:
                    m = folium.Map(location=[48.4, 10.5], zoom_start=8, tiles="cartodbpositron")
                    weights = [12, 7, 3]; colors = ['#2ecc71', '#3498db', '#e74c3c']
                    for i, r in enumerate(data[:3]):
                        path_nodes = r.get('pure_path', [])
                        if path_nodes:
                            points = [[NODES[node]['lat'], NODES[node]['lon']] for node in path_nodes]
                            folium.PolyLine(points, color=colors[i], weight=weights[i], opacity=0.8).add_to(m)
                    st_folium(m, width=550, height=350, key="folium_map")

                st.subheader("📋 Analyse-Matrix")
                df_display = pd.DataFrame(data)[['rank', 'route', 'gesamt_kosten_euro', 'distanz_km', 'zeit_h']]
                
                st.dataframe(df_display.style.format({
                        'gesamt_kosten_euro': '{:.2f} €',
                        'distanz_km': '{:.1f} km'
                    }).set_properties(**{'text-align': 'center'}), 
                    hide_index=True, use_container_width=True)
            else:
                st.info("Keine Route im Netzwerk gefunden.")
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")