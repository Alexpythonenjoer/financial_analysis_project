"""
Модуль очистки данных: загрузка, удаление аномалий, заполнение пропусков.
"""

import pandas as pd
import numpy as np

def load_data(transactions_path='../data/transactions_data.xlsx',
              clients_path='../data/clients_data.json'):
    transactions = pd.read_excel(transactions_path)
    clients = pd.read_json(clients_path)
    return transactions, clients

def clean_transactions(df):
    """Очистка транзакций: удаление отрицательных сумм, некорректных дат."""
    df = df[df['amount'] > 0].copy()
    # Пробуем разные форматы дат
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce', dayfirst=False)
    # Если первая попытка не сработала, пробуем dayfirst=True (для форматов DD/MM/YYYY)
    if df['transaction_date'].isna().all():
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['transaction_date'])
    return df

def clean_clients(df):
    """Очистка клиентов: удаление записей без id, заполнение возраста и пола."""
    df = df.dropna(subset=['id']).copy()
    df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')
    df['age'] = df['age'].fillna(df['age'].median())
    df['gender'] = df['gender'].fillna(df['gender'].mode()[0])
    return df

def prepare_data(transactions, clients):
    """Полная подготовка (очистка + переименование для объединения)."""
    transactions = clean_transactions(transactions)
    clients = clean_clients(clients)
    clients = clients.rename(columns={'id': 'client_id'})
    return transactions, clients