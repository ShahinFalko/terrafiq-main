import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("⏳ Lade die skalierte Datenmatrix (10.000 Fahrten)...")
# Wir laden die große Datei, die wir vorhin physisch auf der Festplatte gesichert haben!
df = pd.read_csv('muenchen_test_10000.csv')

# ==============================================================================
# 1. Features (X) und Target (y) definieren
# ==============================================================================
# Wir schmeißen das Target aus den Features und nutzen alle restlichen Spalten zur Vorhersage
X = df.drop(columns=['CO2_Ausstoss_Ist'])
y = df['CO2_Ausstoss_Ist']

# ==============================================================================
# 2. Train-Test-Split (Strikte Trennung für die Validierung)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"-> Trainings-Datensätze: {X_train.shape[0]}")
print(f"-> Test-Datensätze (für die Validierung): {X_test.shape[0]}")

# ==============================================================================
# 3. Modell-Training
# ==============================================================================
print("\n🤖 Initialisiere Scikit-Learn Linear Regression Modell...")
model = LinearRegression()

# Das Modell lernt NUR aus den 8.000 Trainingsdaten
model.fit(X_train, y_train)
print("✅ Modell erfolgreich auf Trainingsdaten trainiert!")

# ==============================================================================
# 4. Validierung auf den ungesehenen 2.000 Testdaten
# ==============================================================================
y_pred = model.predict(X_test)

# Kennzahlen berechnen
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n📊 --- VALIDIERUNGS-KENNZAHLEN ---")
print(f"-> Bestimmtheitsmass R² (auf Testdaten): {r2:.4f}")
print(f"-> Mittlerer Fehler (RMSE): {rmse:.4f} kg CO2")

# ==============================================================================
# 5. Modell-Export für die Cloud-Infrastruktur
# ==============================================================================
model_filename = 'tco_co2_predictor.joblib'
joblib.dump(model, model_filename)
print(f"\n💾 KI-Modell erfolgreich als '{model_filename}' exportiert.")