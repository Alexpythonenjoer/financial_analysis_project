"""
Модуль визуализации: распределение, выручка по услугам, зависимость от возраста.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_amount_distribution(transactions, save_path='../output/charts/distribution.png'):
    """Гистограмма распределения сумм транзакций."""
    plt.figure(figsize=(10,5))
    sns.histplot(transactions['amount'], bins=50, kde=True, color='skyblue')
    plt.title('Распределение сумм транзакций')
    plt.xlabel('Сумма транзакции')
    plt.ylabel('Частота')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

def plot_revenue_by_service(transactions, save_path='../output/charts/revenue_by_service.png'):
    """Горизонтальная столбцовая диаграмма выручки по услугам."""
    revenue = transactions.groupby('service')['amount'].sum().sort_values()
    plt.figure(figsize=(10,6))
    revenue.plot(kind='barh', color='coral')
    plt.title('Выручка по услугам')
    plt.xlabel('Выручка')
    plt.ylabel('Услуга')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

def plot_avg_amount_vs_age(merged_df, save_path='../output/charts/avg_amount_vs_age.png'):
    """Точечный график средней суммы транзакции от возраста с линией тренда."""
    age_avg = merged_df.groupby('age')['amount'].mean().reset_index()
    plt.figure(figsize=(12,6))
    sns.scatterplot(data=age_avg, x='age', y='amount', alpha=0.7)
    sns.regplot(data=age_avg, x='age', y='amount', scatter=False, color='red')
    plt.title('Средняя сумма транзакции в зависимости от возраста')
    plt.xlabel('Возраст')
    plt.ylabel('Средняя сумма транзакции')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

def plot_forecast(historical, forecast_dates, forecast_values,
                  save_path='../output/charts/forecast.png'):
    """Визуализация исторических данных и прогноза."""
    plt.figure(figsize=(12,5))
    plt.plot(historical['date'], historical['count'], 'o-', label='Факт')
    plt.plot(forecast_dates, forecast_values, 'r--', label='Прогноз')
    plt.title('Прогноз ежедневного спроса на следующий месяц')
    plt.xlabel('Дата')
    plt.ylabel('Количество транзакций')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()