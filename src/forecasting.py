"""
Модуль прогнозирования: подготовка временных рядов, обучение, предсказание.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def prepare_daily_demand(transactions):
    """Преобразует данные транзакций в ежедневную агрегацию."""
    # Принудительно убеждаемся, что столбец datetime
    if not pd.api.types.is_datetime64_any_dtype(transactions['transaction_date']):
        transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'], errors='coerce')
    # Удаляем строки, где дата не распарсилась
    transactions = transactions.dropna(subset=['transaction_date'])

    daily = transactions.groupby(transactions['transaction_date'].dt.date).size().reset_index()
    daily.columns = ['date', 'count']
    # Преобразуем date в datetime для дальнейших операций
    daily['date'] = pd.to_datetime(daily['date'])
    daily['day_number'] = (daily['date'] - daily['date'].min()).dt.days
    return daily


def train_linear_model(daily_df):
    """Обучает линейную регрессию на day_number -> count."""
    X = daily_df[['day_number']].values
    y = daily_df['count'].values
    model = LinearRegression()
    model.fit(X, y)
    return model


def forecast_next_month(model, daily_df, days_ahead=30):
    """
    Прогнозирует спрос на days_ahead дней вперёд.
    Возвращает (forecast_dates, forecast_values, total_forecast).
    """
    last_day = daily_df['day_number'].max()
    future_days = np.arange(last_day + 1, last_day + days_ahead + 1).reshape(-1, 1)
    pred_counts = model.predict(future_days)

    last_date = daily_df['date'].max()
    forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=days_ahead)
    total_forecast = pred_counts.sum()
    return forecast_dates, pred_counts, total_forecast


def save_forecast(forecast_dates, forecast_values, save_path='../output/forecast.csv'):
    """Сохраняет прогноз в CSV."""
    df = pd.DataFrame({'date': forecast_dates, 'predicted_count': forecast_values})
    df.to_csv(save_path, index=False)