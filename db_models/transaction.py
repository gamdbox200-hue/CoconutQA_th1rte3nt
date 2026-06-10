from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AccountTransactionTemplate(Base):
    __tablename__ = 'account_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Account(user='{self.user}', balance={self.balance})>"