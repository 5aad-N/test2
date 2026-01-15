from typing import TypedDict
from .models import User, Item, Bid, Question


class UserDict(TypedDict):
    """Type definition for serialized user data"""

    id: int
    username: str
    email: str
    date_of_birth: str | None
    profile_image: str | None
    bid_item_ids: list[int]
    questioned_item_ids: list[int]


class ItemDict(TypedDict):
    """Type definition for serialized Item"""

    id: int
    owner_id: int
    owner_username: str
    title: str
    description: str
    starting_price: str
    current_price: str
    picture: str | None
    end_date: str
    created_at: str
    is_active: bool
    is_ended: bool
    bid_count: int
    winner_id: int | None
    winner_username: str | None


class BidDict(TypedDict):
    """Type definition for serialized Bid"""

    id: int
    item_id: int
    item_title: str
    bidder_id: int
    bidder_username: str
    amount: str
    created_at: str


class QuestionDict(TypedDict):
    """Type definition for serialized Question"""

    id: int
    item_id: int
    item_title: str
    asker_id: int
    asker_username: str
    question_text: str
    answer_text: str
    asked_at: str
    answered_at: str | None
    is_answered: bool


def serialize_user(user: User) -> UserDict:
    """
    Convert User model instance to typed dictionary for JSON serialization.

    Args:
        user: User model instance

    Returns:
        Dictionary containing user data with proper types
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "date_of_birth": str(user.date_of_birth) if user.date_of_birth else None,
        "profile_image": user.profile_image.url if user.profile_image else None,
        "bid_item_ids": user.bid_item_ids,
        "questioned_item_ids": user.questioned_item_ids,
    }


def serialize_item(item: Item) -> ItemDict:
    """
    Convert Item model instance to typed dictionary.

    Args:
        item: Item model instance

    Returns:
        Dictionary containing item data with proper types
    """
    return {
        "id": item.id,
        "owner_id": item.owner.id,
        "owner_username": item.owner.username,
        "title": item.title,
        "description": item.description,
        "starting_price": str(item.starting_price),
        "current_price": str(item.current_price),
        "picture": item.picture.url if item.picture else None,
        "end_date": item.end_date.isoformat(),
        "created_at": item.created_at.isoformat(),
        "is_active": item.is_active,
        "is_ended": item.is_ended,
        "bid_count": item.bid_count,
        "winner_id": item.winner.id if item.winner else None,
        "winner_username": item.winner.username if item.winner else None,
    }


def serialize_bid(bid: Bid) -> BidDict:
    """
    Convert Bid model instance to typed dictionary.

    Args:
        bid: Bid model instance

    Returns:
        Dictionary containing bid data with proper types
    """
    return {
        "id": bid.id,
        "item_id": bid.item.id,
        "item_title": bid.item.title,
        "bidder_id": bid.bidder.id,
        "bidder_username": bid.bidder.username,
        "amount": str(bid.amount),
        "created_at": bid.created_at.isoformat(),
    }


def serialize_question(question: Question) -> QuestionDict:
    """
    Convert Question model instance to typed dictionary.

    Args:
        question: Question model instance

    Returns:
        Dictionary containing question data with proper types
    """
    return {
        "id": question.id,
        "item_id": question.item.id,
        "item_title": question.item.title,
        "asker_id": question.asker.id,
        "asker_username": question.asker.username,
        "question_text": question.question_text,
        "answer_text": question.answer_text,
        "asked_at": question.asked_at.isoformat(),
        "answered_at": (
            question.answered_at.isoformat() if question.answered_at else None
        ),
        "is_answered": question.is_answered,
    }
