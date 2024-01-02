from aiomysql import DictCursor
from fastapi import Depends, HTTPException

from ..database import get_db
from ..schemas.payment_limit_schemas import PaymentLimit


class PaymentLimitService:
    def __init__(self, db=Depends(get_db)) -> None:
        self.db: DictCursor = db

    async def get_payment_limit(self, user_id: int) -> PaymentLimit:
        """Get payment limit for user."""
        query: str = """
            SELECT
                a.idAccount as account_id,
                a.idUser as user_id,
                al.currentLimit as current_limit
            FROM
                Account a
                INNER JOIN AccountLimit al ON a.idAccount = al.idAccount
            WHERE
                a.idUser = %s
        """
        params: tuple = (user_id,)
        async with self.db.cursor(DictCursor) as cursor:
            await cursor.execute(query, params)
            result = await cursor.fetchall()

        if result:
            return PaymentLimit(**result[0])
        raise HTTPException(
            status_code=404, detail=f"Payment limit not found for user_id `{user_id}`"
        )

    async def get_payment_limit_by_account(self, account_id: int) -> PaymentLimit:
        """Get payment limit for account."""
        query: str = """
            SELECT
                a.idAccount as account_id,
                a.idUser as user_id,
                al.currentLimit as current_limit
            FROM
                Account a
                INNER JOIN AccountLimit al ON a.idAccount = al.idAccount
            WHERE
                a.idAccount = %s
        """
        params: tuple = (account_id,)
        async with self.db.cursor(DictCursor) as cursor:
            await cursor.execute(query, params)
            result = await cursor.fetchall()

        if result:
            return PaymentLimit(**result[0])
        raise HTTPException(
            status_code=404,
            detail=f"Payment limit not found for account_id `{account_id}`",
        )
