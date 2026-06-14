import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("⏳ Lade die skalierte Sprit-Datenmatrix (10.000 Fahrten)...")
df = pd.read_csv('muenchen_test_10000.csv')

# ==============================================================================
# 1. Features (X) und Target (y) definieren -> JETZT AUF LITERN
# ==============================================================================
X = df.drop(columns=['Sprit_Verbrauch_Ist_Liter'])
y = df['Sprit_Verbrauch_Ist_Liter']  # Das neue Target!

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
print("✅ Modell erfolgreich auf Spritverbrauch trainiert!")

# ==============================================================================
# 4. Validierung auf den ungesehenen 2.000 Testdaten
# ==============================================================================
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred)) # Der Fehler ist jetzt direkt in Litern!

print(f"\n📊 --- VALIDIERUNGS-KENNZAHLEN (WEG B) ---")
print(f"-> Bestimmtheitsmass R² (auf Testdaten): {r2:.4f}")
print(f"-> Mittlerer Fehler (RMSE): {rmse:.4f} Liter Diesel") # Saubere Einheit!

# ==============================================================================
# 5. Modell-Export für die Cloud-Infrastruktur
# ==============================================================================
model_filename = 'tco_fuel_predictor.joblib' # Name angepasst auf Fuel!
joblib.dump(model, model_filename)
print(f"\n💾 KI-Modell erfolgreich als '{model_filename}' exportiert.")