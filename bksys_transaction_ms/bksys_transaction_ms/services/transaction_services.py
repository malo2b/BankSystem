from fastapi import Depends, HTTPException

from aiomysql import DictCursor

from ..database import get_db
from ..schemas import (
    Paginated,
    PaginatedTransactionResponse,
    Transaction,
    TransactionRequest,
)


class TransactionService:
    def __init__(self, db=Depends(get_db)) -> None:
        self.db: DictCursor = db

    async def get_transactions(
        self, account_id: int, paginated: Paginated
    ) -> PaginatedTransactionResponse:
        """Get transactions for a given account with pagination info."""
        query: str = """
            SELECT
                idTransaction as id,
                idAccount as id_account,
                amount,
                type as transaction_type,
                transactionDate as transaction_date,
                COUNT(*) OVER() as total_count
            FROM Transaction WHERE idAccount = %s
            ORDER BY transactionDate DESC
            LIMIT %s OFFSET %s
            """
        params: tuple = (account_id, paginated.limit, paginated.offset)
        async with self.db.cursor(DictCursor) as cursor:
            await cursor.execute(query, params)
            result = await cursor.fetchall()

        if not result:
            # Check if account exists
            query: str = """
                SELECT idAccount FROM Account WHERE idAccount = %s
                """
            params: tuple = (account_id,)
            async with self.db.cursor(DictCursor) as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchone()
            if not result:
                # Account not found
                raise HTTPException(status_code=404, detail="Account not found.")
            else:
                # Account found but no transactions
                return PaginatedTransactionResponse.model_construct(
                    data=[], pagination=paginated.with_total(0)
                )

        return PaginatedTransactionResponse.model_construct(
            data=[Transaction(**row) for row in result],
            pagination=paginated.with_total(result[0]["total_count"]),
        )

    async def add_transaction(self, transaction: TransactionRequest) -> Transaction:
        """Send a transaction."""
        # Transaction query
        transaction_query: str = """
            INSERT INTO Transaction (idAccount, amount, type, transactionDate)
            VALUES (%s, %s, %s, %s)
            """
        transaction_params: tuple = (
            transaction.id_account,
            transaction.amount,
            transaction.transaction_type,
            transaction.transaction_date,
        )
        # Update account query
        if transaction.transaction_type == "Incoming":
            update_account_query: str = """
                UPDATE Account SET balance = balance + %s WHERE idAccount = %s
                """
        else:
            update_account_query: str = """
                UPDATE Account SET balance = balance - %s WHERE idAccount = %s
                """
        update_account_params: tuple = (transaction.amount, transaction.id_account)

        # Execute queries
        try:
            async with self.db.cursor(DictCursor) as cursor:
                await cursor.execute(transaction_query, transaction_params)
                await cursor.execute(update_account_query, update_account_params)
                await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

        return transaction
