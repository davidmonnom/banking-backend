from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, Float
from sqlalchemy.orm import relationship

from .database import Base


# Many2many relations
user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('userId', Integer, ForeignKey('users.id')),
    Column('groupId', Integer, ForeignKey('groups.id')),
)

transaction_categories = Table(
    'transaction_categories',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('transactionId', Integer, ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('categoryId', Integer, ForeignKey('categories.id', onupdate="CASCADE", ondelete="CASCADE"))
)

transaction_goals = Table(
    'transaction_goals',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('transactionId', Integer, ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('goalId', Integer, ForeignKey('goals.id', onupdate="CASCADE", ondelete="CASCADE"))
)

transaction_budgets = Table(
    'transaction_budgets',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('transactionId', Integer, ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('budgetId', Integer, ForeignKey('budgets.id', onupdate="CASCADE", ondelete="CASCADE"))
)


# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    externalId = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    display_name = Column(String)
    picture = Column(String)
    provider = Column(String, index=True)
    language = Column(String)
    darkMode = Column(Boolean)
    isAdmin = Column(Boolean, default=False)

    # one2many
    ownedGroup = relationship(
        "Group",
        backref="user",
        foreign_keys="Group.userOwnerId",
        cascade="all, delete")

    # many2many
    groups = relationship(
        "Group",
        secondary="user_groups",
        back_populates="users",
        cascade="all, delete")


# Group model
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    # Foreign keys
    userOwnerId = Column(Integer, ForeignKey("users.id"))

    # many2many
    users = relationship(
        "User",
        secondary="user_groups",
        back_populates="groups")


# Category model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String)
    name = Column(String)
    limit = Column(Integer)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"))

    # many2many
    transactions = relationship(
        "Transaction",
        secondary="transaction_categories",
        back_populates="categories",
        cascade="all, delete")


# Goal model
class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    amount = Column(Integer)
    dateEnd = Column(String)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"))

    # many2many
    transactions = relationship(
        "Transaction",
        secondary="transaction_goals",
        back_populates="goals",
        cascade="all, delete")


# Budget model
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    amount = Column(Integer)
    type = Column(String)
    startMonth = Column(String)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"))

    # many2many
    transactions = relationship(
        "Transaction",
        secondary="transaction_budgets",
        back_populates="budgets",
        cascade="all, delete")


# Item model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    itemId = Column(String, unique=True)
    accessToken = Column(String)
    publicToken = Column(String)
    institutionId = Column(String)
    institutionName = Column(String)
    webhook = Column(String)
    updateDate = Column(String)
    lastFailedUpdate = Column(String)
    expirationDate = Column(String)
    cursor = Column(String)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"))

    # one2many
    accounts = relationship("Account", back_populates="item")


# Account model
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    accountId = Column(String, unique=True)
    name = Column(String)
    mask = Column(String)
    officialName = Column(String)
    type = Column(String)
    subtype = Column(String)
    balances = Column(Float)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"))
    itemId = Column(Integer, ForeignKey("items.id"))

    # many2one
    item = relationship("Item", back_populates="accounts")


# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transactionId = Column(String, unique=True)
    amount = Column(Float)
    name = Column(String)
    merchantName = Column(String, nullable=True)  # Plaid sucks
    merchantWebsite = Column(String, nullable=True)  # Plaid sucks
    merchantEntityId = Column(String, nullable=True)  # Plaid sucks
    date = Column(String, index=True)
    isoCurrencyCode = Column(String)

    # Foreign keys
    groupId = Column(Integer, ForeignKey("groups.id"), index=True)
    accountId = Column(Integer, ForeignKey("accounts.id"), index=True)

    # categoryIds = Column(Integer, ForeignKey("categories.id"), index=True)
    # goalIds = Column(Integer, ForeignKey("goals.id"), index=True)
    # budgetIds = Column(Integer, ForeignKey("budgets.id"), index=True)

    # many2many
    categories = relationship(
        "Category",
        secondary="transaction_categories",
        cascade="all, delete")

    goals = relationship(
        "Goal",
        secondary="transaction_goals",
        cascade="all, delete")

    budgets = relationship(
        "Budget",
        secondary="transaction_budgets",
        cascade="all, delete")
