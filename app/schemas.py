from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# Pydantic schema for Group
class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for User
class UserBase(BaseModel):
    externalId: str
    isAdmin: bool = False
    email: str
    first_name: str
    last_name: str
    picture: str
    provider: str
    language: str
    darkMode: bool


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    language: str
    darkMode: bool


class User(UserBase):
    id: int
    groups: Optional[List["Group"]] = []
    ownedGroup: Optional[List["Group"]] = []

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Category
class CategoryBase(BaseModel):
    color: str
    name: str
    limit: int
    groupId: int


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Goal
class GoalBase(BaseModel):
    name: str
    description: str
    amount: int
    dateEnd: str
    groupId: int


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Budget
class BudgetBase(BaseModel):
    name: str
    description: str
    amount: int
    type: str
    startMonth: str
    groupId: int


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Account
class AccountBase(BaseModel):
    name: str
    accountId: str
    mask: str
    officialName: str
    type: str
    subtype: str
    balances: float
    groupId: int
    itemId: int


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: str
    balances: float


class Account(AccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Transaction
class TransactionBase(BaseModel):
    transactionId: str
    accountId: int
    amount: float
    name: str
    merchantName: Optional[str] = None
    merchantWebsite: Optional[str] = None
    merchantEntityId: Optional[str] = None
    date: str
    isoCurrencyCode: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    name: str
    merchantName: Optional[str] = None
    merchantWebsite: Optional[str] = None
    merchantEntityId: Optional[str] = None
    categories: Optional[List[int]] = []
    goals: Optional[List[int]] = []
    budgets: Optional[List[int]] = []


class Transaction(TransactionBase):
    id: int
    categories: List["Category"]
    goals: List["Goal"]
    budgets: List["Budget"]
    # categoryIds: List[int]
    # goalIds: List[int]
    # budgetIds: List[int]

    model_config = ConfigDict(from_attributes=True)


# Pydantic schema for Item
class ItemBase(BaseModel):
    itemId: str
    accessToken: str
    publicToken: str
    groupId: int
    institutionId: Optional[str] = None
    institutionName: Optional[str] = None
    webhook: Optional[str] = None
    updateDate: Optional[str] = None
    lastFailedUpdate: Optional[str] = None
    expirationDate: Optional[str] = None
    cursor: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    updateDate: Optional[str] = None
    lastFailedUpdate: Optional[str] = None
    cursor: Optional[str] = None


class Item(ItemBase):
    id: int
    accounts: List["Account"]

    model_config = ConfigDict(from_attributes=True)
