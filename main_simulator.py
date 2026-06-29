import sqlite3
from datetime import datetime
import streamlit as strl
import time
import pandas as pd
import numpy as np

# --- IMPORTATION DE L IA DE PRÉDICTION ---
try:
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Configuration de la page Web du Jumeau Numérique
strl.set_page_config(
    page_title="Jumeau Numérique - Smart Grid Cameroun",
    page_icon="⚡",
    layout="wide",
)

DB_NAME = "eneo_smartgrid.db"

# --- ENTRAÎNEMENT INITIAL D'UNE IA LOCALE (Machine Learning) ---
@strl.cache_resource
def entrainer_ia_predictive():
    """Simule un historique de données industrielles pour entraîner l'IA"""
    if not SKLEARN_AVAILABLE:
        return None
        
    np.random.seed(42)
    # Génère 500 exemples : [Niveau Eau, Température Ambiante] -> Puissance Réelle
    X_train = np.random.rand(500, 2)
    X_train[:, 0] = X_train[:, 0] * 100  # Niveau d'eau entre 0 et 100%
    X_train[:, 1] = 20 + X_train[:, 1] * 20  # Température entre 20°C et 40°C
    
    # La puissance dépend physiquement de l'eau, mais baisse légèrement s'il fait trop chaud (pertes thermiques)
    y_train = (400.0 * (X_train[:, 0] / 100.0)) - (0.5 * X_train[:, 1])
    y_train = np.clip(y_train, 0, 400)
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    return model

model_ia = entrainer_ia_predictive()

if not SKLEARN_AVAILABLE:
    strl.sidebar.warning("⚠️ Module 'scikit-learn' introuvable. Exécution en mode formule mathématique.")

# --- BASE DE DONNÉES ---
def init_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tHistoriqueCrise (
                id INTEGER PRIMARY KEY AUTOINCREMENT, date_action TEXT, niveau_barrage REAL,
                puissance_allouee REAL, mode_reseau TEXT, sms_envoye TEXT
            )
        """)
        conn.commit()

def log_action_to_db(level, power, mode, sms_status="Non requis"):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO tHistoriqueCrise (date_action, niveau_barrage, puissance_allouee, mode_reseau, sms_envoye) VALUES (?, ?, ?, ?, ?)",
                           (now, round(level, 1), round(power, 1), mode, sms_status))
            conn.commit()
    except Exception: pass

def get_historical_data():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            return pd.read_sql_query("SELECT date_action, niveau_barrage, puissance_allouee FROM tHistoriqueCrise ORDER BY id DESC LIMIT 15", conn).iloc[::-1]
    except Exception: return pd.DataFrame()

init_database()

# --- INTERFACE PRINCIPALE ---
strl.title("⚡ JUMEAU NUMÉRIQUE INDUSTRIEL AVEC IA PRÉDICTIVE (ML)")
strl.subheader("Machine Learning Scikit-Learn & Télémétrie Intégrée - Concours Présidentiel")
strl.write("---")

# Paramètres environnementaux avancés pour l'IA
col_param1, col_param2 = strl.columns(2)
with col_param1:
    water_level = strl.slider("Ajustez le niveau d'eau du réservoir du barrage (%) :", 0.0, 100.0, 75.0, 1.0)
with col_param2:
    temperature = strl.slider("Température ambiante extérieure (°C) [Impact thermique sur alternateur] :", 15.0, 45.0, 28.0, 0.5)

# --- CALCUL DE LA PUISSANCE VIA L'IA DE MACHINE LEARNING ---
if model_ia is not None:
    features_ia = np.array([[water_level, temperature]])
    puissance_predite_ia = float(model_ia.predict(features_ia)[0])
else:
    # Formule physique mathématique de secours autonome si scikit-learn est absent
    puissance_predite_ia = 400.0 * (water_level / 100.0)

# --- LOGIQUE DE RATIONNEMENT INTELLIGENT & CHRONOLOGIE SMS ---
sms_sent_log = "Aucun"

if puissance_predite_ia > 250.0:
    network_mode = "Stable"
    mode_status = "success"
    mode_text = "🟢 MODE RÉSEAU : STABLE (Production Nominale)"
    foyer_limit, foyer_stat = "Illimitée", "Alimenté"
    hospital_limit, hospital_stat = "Illimitée", "Alimenté"
    strl.sidebar.success("✅ **Réseau ENEO Nominal**\nAucune restriction nécessaire sur le réseau national.")
elif 100.0 <= puissance_predite_ia <= 250.0:
    network_mode = "Alerte Sec"
    mode_status = "warning"
    mode_text = "🟠 MODE ALERTE : RATIONNEMENT INTELLIGENT DE L'IA"
    foyer_limit, foyer_stat = "Bridé à 1200W", "Optimisé par IA"
    hospital_limit, hospital_stat = "Illimitée (Prioritaire)", "Alimenté"
    sms_sent_log = "SMS Rationnement Envoyé"
    strl.sidebar.warning(
        "💬 **SMS envoyé aux habitants :**\n"
        "*ENEO IA Info : Entrée en saison sèche. Vos compteurs sont limités à 1200W pour éviter les coupures.*"
    )
else:
    network_mode = "Survie Critique"
    mode_status = "error"
    mode_text = "🔴 CRITIQUE : URGENCE ET PROTECTION DES LIGNES HÔPITAUX"
    foyer_limit, foyer_stat = "Bridé à 200W", "Économie Stricte"
    hospital_limit, hospital_stat = "Illimitée", "Sécurisé"
    sms_sent_log = "SMS Crise Émis"
    strl.sidebar.error(
        "🚨 **SMS D'URGENCE envoyé aux habitants :**\n"
        "*ENEO IA ALERTE : Niveau du barrage critique ! Priorité absolue accordée aux Hôpitaux et 200W aux ménages.*"
    )

# --- SÉCURISATION DE L'ARCHIVAGE AUTOMATIQUE ---
log_action_to_db(water_level, puissance_predite_ia, network_mode, sms_sent_log)

# --- AFFICHAGE DU TABLEAU DE BORD ---
strl.write("---")
strl.header("📊 Analyse Exécutive : Machine Learning & Télémétrie")

col_metric1, col_metric2 = strl.columns(2)
with col_metric1:
    strl.metric(
        label="🔮 Puissance estimée par l'IA (Machine Learning)", 
        value=f"{puissance_predite_ia:.2f} MW",
        delta=f"Impact Chaleur: -{((400 * (water_level/100)) - puissance_predite_ia):.1f} MW" if model_ia else None
    )
with col_metric2:
    if mode_status == "success":
        strl.success(mode_text)
    elif mode_status == "warning":
        strl.warning(mode_text)
    else:
        strl.error(mode_text)

# =====================================================================
# 📟 JUMEAU NUMÉRIQUE : ÉMULATION TECHNIQUE DE L'AUTOMATE DE TERRAIN
# =====================================================================
strl.write("---")
strl.header("⚡ Jumeau Numérique : État Opérationnel de l'Automate Réseau")

if network_mode == "Stable":
    texte_lcd = "ENERGIE LIBRE"
    led_verte, led_jaune, led_rouge = "🟢 ALLUMÉE (Nominal)", "⚫ Éteinte", "⚫ Éteinte"
    vitesse_moteur = "3000 RPM (Pleine charge - 100%)"
    relais_status = "🟢 Au repos (Ligne principale active)"
elif network_mode == "Alerte Sec":
    texte_lcd = "BRIDE MAX 1200W"
    led_verte, led_jaune, led_rouge = "⚫ Éteinte", "🟡 ALLUMÉE (Rationnement)", "⚫ Éteinte"
    vitesse_moteur = "1500 RPM (Régulation PWM à 50%)"
    relais_status = "🟢 Au repos (Ligne principale active)"
else:
    texte_lcd = "BRIDE MAX 200W"
    led_verte, led_jaune, led_rouge = "⚫ Éteinte", "⚫ Éteinte", "🔴 ALLUMÉE (Alerte Maximale)"
    vitesse_moteur = "0 RPM (Arrêt Sécurité / Protection)"
    relais_status = "⚡ Activé (Bascule sur Résistance de délestage)"

col_lcd, col_leds, col_actuateurs = strl.columns(3)

with col_lcd:
    strl.subheader("📟 Écran LCD 16x2")
    strl.markdown(
        f"""
        <div style="background-color: #004d40; color: #00ffcc; font-family: 'Courier New', monospace; padding: 15px; border-radius: 8px; border: 3px solid #333; box-shadow: 2px 2px 10px rgba(0,0,0,0.3); font-size: 18px;">
            <strong>L1:</strong> SMART GRID CAM<br>
            <strong>L2:</strong> {texte_lcd}
        </div>
        """, 
        unsafe_allow_html=True
    )
    strl.caption("Émulation en temps réel du bus d'affichage HD44780")

with col_leds:
    strl.subheader("🚨 Indicateurs Lumineux")
    strl.markdown(f"**Voyant Vert (Stable) :** {led_verte}")
    strl.markdown(f"**Voyant Jaune (Rationnement) :** {led_jaune}")
    strl.markdown(f"**Voyant Rouge (Coupure/Critique) :** {led_rouge}")

with col_actuateurs:
    strl.subheader("⚙️ Organes Électromécaniques")
    strl.metric(label="Rotation de la Turbine", value=vitesse_moteur)
    strl.markdown(f"**État du Relais Commutateur :** {relais_status}")

if 'dernier_mode_ia' not in strl.session_state:
    strl.session_state['dernier_mode_ia'] = ''

if network_mode != strl.session_state['dernier_mode_ia']:
    strl.session_state['dernier_mode_ia'] = network_mode
    if network_mode == "Stable":
        strl.toast("Réseau Stable : Distribution normale au Cameroun", icon="🟢")
    elif network_mode == "Alerte Sec":
        strl.toast("Alerte Sécheresse : Déploiement du plan de bridage intelligent (1200W)", icon="🟡")
    elif network_mode == "Survie Critique":
        strl.toast("Urgence Critique : Isolation immédiate des lignes secondaires", icon="🔴")

# --- GRAPHES INTERACTIFS (COURBE PRÉDICTIVE RESTAURÉE) ---
strl.write("---")
strl.header("📈 Supervision Temporelle des Prédictions de l'IA")

# Génération d'une courbe prédictive dynamique simulant l'évolution de la puissance
heures = [f"{h:02d}:00" for h in range(24)]
puissances_predites = []
for h in range(24):
    # Simulation d'une variation naturelle de la puissance selon les heures de la journée
    variation_heure = np.sin(h * np.pi / 12) * 15.0
    p_heure = puissance_predite_ia + variation_heure
    puissances_predites.append(np.clip(p_heure, 0, 400))

df_prediction = pd.DataFrame({"Heures": heures, "Puissance Prédite (MW)": puissances_predites})
strl.line_chart(df_prediction.set_index("Heures"), color="#2E7D32")


# --- TABLE DES DIRECTIVES AUX COMPTEURS  ---
strl.write("---")
strl.header("📡 Plan d'Allocation Dynamique des Charges")

# On prépare la logique à l'avance pour éviter de faire planter le dictionnaire
if network_mode == "Survie Critique":
    allocation_industrie = "Délestage Total"
    etat_industrie = "Coupé"
elif network_mode == "Alerte Sec":
    allocation_industrie = "Régulé (Minimum)"
    etat_industrie = "Optimisé par IA"
else:
    allocation_industrie = "Illimitée"
    etat_industrie = "Nominal"

data = [
    {"Consommateur": "Hôpitaux Régionaux", "Priorité": "1 - ABSOLUE", "Allocation IA": hospital_limit, "État": hospital_stat},
    {"Consommateur": "Ménages (Douala/Yaoundé)", "Priorité": "2 - SECONDAIRE", "Allocation IA": foyer_limit, "État": foyer_stat},
    {"Consommateur": "Aciéries / Zones Indus", "Priorité": "3 - EFFACING", "Allocation IA": allocation_industrie, "État": etat_industrie},
]

# Affichage sécurisé sous forme de tableau Pandas pour éviter les bugs graphiques
df_table = pd.DataFrame(data)
strl.table(df_table)

# --- ARCHIVAGE MANUEL ---
strl.write("---")
if strl.button("💾 Archiver la prédiction de l'IA"):
    log_action_to_db(water_level, puissance_predite_ia, network_mode, sms_sent_log)
    strl.toast("Prédiction IA enregistrée avec succès !", icon="💾")
