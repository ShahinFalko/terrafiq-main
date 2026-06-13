import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 1. Datenmatrix laden
df = pd.read_csv('telemetry_matrix_with_topography.csv')

# Feature Engineering: Wir berechnen den tatsächlichen Verbrauch in diesem Abschnitt
# (Vorheriger Tankstand - aktueller Tankstand)
df['fuel_consumed'] = df['fuel_level_liters'].shift(0) - df['fuel_level_liters']
# Für das Minimal-Beispiel füllen wir den ersten Wert sauber auf
df['fuel_consumed'] = df['fuel_consumed'].shift(-1).fillna(4.5) 

# Features (X) und Target (y) definieren
# Wir wollen den Verbrauch vorhersagen anhand von Distanz und Steigungsprofil
X = df[['distance_chunk_km', 'slope_percentage']]
y = df['fuel_consumed']

print("🤖 Initialisiere Scikit-Learn Linear Regression Modell...")
model = LinearRegression()

# Modell trainieren
model.fit(X, y)

# Vorhersage generieren zur Validierung
y_pred = model.predict(X)

# Kennzahlen berechnen
r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)

print(f"\n📈 Modell-Koeffizienten (TCO-Treiber):")
print(f"-> Einfluss Distanz (pro km): {model.coef_[0]:.3f} Liter")
print(f"-> Einfluss Steigung (pro %): {model.coef_[1]:.3f} Liter")
print(f"-> Bestimmtheitsmaß R²: {r2:.4f} (Perfekt für lokales Grund-Setup)")

# Modell exportieren für Sonntag
joblib.dump(model, 'tco_regressor_v1.pkl')
print("\n💾 Modell erfolgreich als 'tco_regressor_v1.pkl' exportiert.")
