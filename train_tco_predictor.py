import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("⏳ Lade die 10.000 topographischen Datensätze aus München West...")
df = pd.read_csv('telemetry_matrix_with_topography.csv')

# ==============================================================================
# 1. Features (X) und Target (y) definieren
# ==============================================================================
FEATURES = [
    'latitude', 
    'longitude', 
    'distance_chunk_km', 
    'payload_kg',
    'hour_of_day',
    'elevation_meters', 
    'slope_percentage'
]

X = df[FEATURES]
y = df['Sprit_Verbrauch_Ist_Liter']

# ==============================================================================
# 2. Train-Test-Split (80% Training, 20% Validierung)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================================================================
# 3. Modell-Training & Hyperparameter-Check
# ==============================================================================
print("\n🤖 Trainiere das erweiterte TCO-Predictor Modell...")
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Modell erfolgreich auf 10.000 Real-Szenarien trainiert!")

# ==============================================================================
# 4. Validierung (Beseitigung der alten 'nan'-Warnung)
# ==============================================================================
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n📊 --- VALIDIERUNGS-KENNZAHLEN ---")
print(f"-> Bestimmtheitsmass R² (Genauigkeit): {r2*100:.2f}%")
print(f"-> Mittlerer Fehler (RMSE): {rmse:.4f} Liter")

# Gewichte für unsere Lambda-Funktion anzeigen lassen
print(f"\n⚙️ --- MODELL-GEWICHTE FÜR DEINEN BRAIN-SERVICE ---")
print(f"Intercept (Basiswert): {model.intercept_:.4f}")
for feature, coef in zip(FEATURES, model.coef_):
    print(f"-> {feature}: {coef:.6f}")

# ==============================================================================
# 5. Modell-Export
# ==============================================================================
model_filename = 'tco_fuel_predictor.joblib'
joblib.dump(model, model_filename)
print(f"\n💾 KI-Modell erfolgreich als '{model_filename}' exportiert.")