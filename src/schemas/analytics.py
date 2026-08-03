from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TransactionAnalysisModel(BaseModel): # for taskiq
    start_date: date
    end_date: date

    registered_users_count: int
    registered_and_deposit_users_count: int
    registered_and_not_rollbacked_deposit_users_count: int

    not_rollbacked_deposit_amount: Decimal
    not_rollbacked_withdraw_amount: Decimal

    transactions_count: int
    not_rollbacked_transactions_count: int

class TransactionAnalyticsModel(BaseModel): # for clickhouse
    transaction_id: int
    user_id: int
    amount: Decimal
    currency: str
    status: str