import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("⏳ Lade die reale, topographische Sprit-Datenmatrix aus München...")
# KORREKTUR: Wir nutzen jetzt die Datei mit den topographischen Features!
df = pd.read_csv('telemetry_matrix_with_topography.csv')

# ==============================================================================
# 1. Features (X) explizit definieren und in feste Reihenfolge bringen
# ==============================================================================
# Wir definieren die Features nun EXAKT so, wie sie aus der Silver-Zone kommen!
FEATURES = [
    'latitude', 
    'longitude', 
    'fuel_level_liters', 
    'distance_chunk_km', 
    'elevation_meters', 
    'slope_percentage'
]

X = df[FEATURES]
# Das Target bleibt der Spritverbrauch (wird in deiner CSV simuliert/berechnet)
# Hinweis: Falls deine CSV-Spalte für den Verbrauch anders heißt, passen wir das an.
y = df['fuel_level_liters'].shift(-1).fillna(df['fuel_level_liters']) # Beispiel für Verbrauchskorrelation

# ==============================================================================
# 2. Train-Test-Split (80% Training, 20% Validierung)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================================================================
# 3. Modell-Training
# ==============================================================================
print("\n🤖 Initialisiere Scikit-Learn Linear Regression Modell...")
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Modell erfolgreich auf topographischen Spritverbrauch trainiert!")

# ==============================================================================
# 4. Validierung auf den ungesehenen Testdaten
# ==============================================================================
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n📊 --- VALIDIERUNGS-KENNZAHLEN ---")
print(f"-> Bestimmtheitsmass R² (auf Testdaten): {r2:.4f}")
print(f"-> Mittlerer Fehler (RMSE): {rmse:.4f} Liter")

# ==============================================================================
# 5. Modell-Export für die Cloud-Infrastruktur (terrafiq-brain-service)
# ==============================================================================
model_filename = 'tco_fuel_predictor.joblib'
joblib.dump(model, model_filename)
print(f"\n💾 KI-Modell erfolgreich als '{model_filename}' exportiert.")