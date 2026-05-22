"""
Модуль аналитики: топ услуг, средние суммы, выручка, доли, группировки.
"""

import pandas as pd

def top_services_by_orders(transactions, n=5):
    """Топ‑n услуг по количеству заказов."""
    return transactions['service'].value_counts().head(n)

def avg_amount_by_city(transactions):
    """Средняя сумма транзакции по городам (сортировка по убыванию)."""
    return transactions.groupby('city')['amount'].mean().sort_values(ascending=False)

def service_with_max_revenue(transactions):
    """Услуга с наибольшей выручкой и сама выручка."""
    revenue = transactions.groupby('service')['amount'].sum()
    return revenue.idxmax(), revenue.max()

def payment_method_percentage(transactions):
    """Процент транзакций по каждому способу оплаты."""
    return transactions['payment_method'].value_counts(normalize=True) * 100

def revenue_last_month(transactions):
    """Выручка за последний месяц (с первого дня последнего месяца)."""
    last_date = transactions['transaction_date'].max()
    month_start = last_date.replace(day=1)
    return transactions[transactions['transaction_date'] >= month_start]['amount'].sum()

def wealth_category(net_worth):
    """Категория клиента по капиталу."""
    if pd.isna(net_worth):
        return 'Неизвестно'
    elif net_worth < 100_000:
        return 'Низкий капитал (<100k)'
    elif net_worth <= 1_000_000:
        return 'Средний капитал (100k-1M)'
    else:
        return 'Высокий капитал (>1M)'

def revenue_by_wealth(merged_df):
    """Выручка в разрезе категорий капитала."""
    merged_df = merged_df.copy()
    merged_df['wealth_level'] = merged_df['net_worth'].apply(wealth_category)
    return merged_df.groupby('wealth_level')['amount'].sum().sort_values(ascending=False)

def average_amount_by_age(merged_df):
    """Средняя сумма транзакции в зависимости от возраста (DataFrame: age, avg_amount)."""
    return merged_df.groupby('age')['amount'].mean().reset_index()