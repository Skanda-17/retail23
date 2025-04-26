import pandas as pd
import pmdarima as pm
import warnings

warnings.filterwarnings("ignore")

# Load the dataset
df = pd.read_csv('datasets/train.csv', parse_dates=['date'])

def forecast_sales(store_nbr, family):
    # Filter based on store number and family
    subset = df[(df['store_nbr'] == int(store_nbr)) & (df['family'] == family)]
    
    if subset.empty:
        raise ValueError("No data found for the given store_nbr and family.")

    # Sort by date
    subset = subset.sort_values('date')

    # Prepare time series
    ts = subset.set_index('date')['sales']

    # Train Auto-ARIMA model
    model = pm.auto_arima(ts, seasonal=True, m=7, suppress_warnings=True, error_action="ignore")

    # Forecast for next 30 days
    n_periods = 30
    forecast = model.predict(n_periods=n_periods)

    # Create future dates
    future_dates = pd.date_range(ts.index[-1] + pd.Timedelta(days=1), periods=n_periods)

    # Prepare result dataframe
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'forecasted_sales': forecast
    })

    return forecast_df
