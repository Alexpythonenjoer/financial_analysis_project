import os
import sys

# Определяем корневую директорию проекта (папка, содержащая src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'charts'), exist_ok=True)

# Добавляем путь к модулям src (хотя они уже в той же папке, но для уверенности)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_cleaning import load_data, prepare_data
from analysis import (
    top_services_by_orders, avg_amount_by_city, service_with_max_revenue,
    payment_method_percentage, revenue_last_month, revenue_by_wealth,
    average_amount_by_age
)
from visualization import (
    plot_amount_distribution, plot_revenue_by_service,
    plot_avg_amount_vs_age, plot_forecast
)
from forecasting import prepare_daily_demand, train_linear_model, forecast_next_month, save_forecast

def main():
    # 1. Загрузка и очистка (передаём полные пути)
    trans, clients = load_data(
        transactions_path=os.path.join(DATA_DIR, 'transactions_data.xlsx'),
        clients_path=os.path.join(DATA_DIR, 'clients_data.json')
    )
    trans, clients = prepare_data(trans, clients)
    merged = trans.merge(clients, on='client_id', how='left')

    # 2. Анализ (вывод в консоль)
    print("=== РЕЗУЛЬТАТЫ АНАЛИЗА ===\n")
    print("Топ-5 услуг по количеству заказов:\n", top_services_by_orders(trans), "\n")
    print("Средняя сумма по городам (первые 5):\n", avg_amount_by_city(trans).head(), "\n")
    top_service, top_rev = service_with_max_revenue(trans)
    print(f"Услуга с наибольшей выручкой: {top_service} ({top_rev:,.2f})\n")
    print("Доля способов оплаты (%):\n", payment_method_percentage(trans), "\n")
    print(f"Выручка за последний месяц: {revenue_last_month(trans):,.2f}\n")

    # 3. Выручка по категориям капитала
    rev_by_wealth = revenue_by_wealth(merged)
    print("Выручка по уровню капитала:\n", rev_by_wealth, "\n")

    # 4. Визуализация (передаём пути сохранения)
    plot_amount_distribution(trans, save_path=os.path.join(OUTPUT_DIR, 'charts', 'distribution.png'))
    plot_revenue_by_service(trans, save_path=os.path.join(OUTPUT_DIR, 'charts', 'revenue_by_service.png'))
    plot_avg_amount_vs_age(merged, save_path=os.path.join(OUTPUT_DIR, 'charts', 'avg_amount_vs_age.png'))

    # 5. Прогнозирование
    daily = prepare_daily_demand(trans)
    model = train_linear_model(daily)
    forecast_dates, forecast_vals, total_forecast = forecast_next_month(model, daily)
    print(f"Прогнозируемое количество транзакций в следующем месяце: {total_forecast:.0f}")
    save_forecast(forecast_dates, forecast_vals, save_path=os.path.join(OUTPUT_DIR, 'forecast.csv'))
    plot_forecast(daily, forecast_dates, forecast_vals, save_path=os.path.join(OUTPUT_DIR, 'charts', 'forecast.png'))

    print("\nАнализ завершён. Результаты сохранены в папку", OUTPUT_DIR)
    print("Тип transaction_date:", trans['transaction_date'].dtype)
    print("Пример дат:", trans['transaction_date'].head())
if __name__ == '__main__':
    main()