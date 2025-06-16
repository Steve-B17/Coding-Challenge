from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models
from sqlalchemy.exc import SQLAlchemyError


def get_challenge_quota(db: Session, user_id: str):
    try:
        return (db.query(models.ChallengeQuota)
                .filter(models.ChallengeQuota.user_id == user_id)
                .first())
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error while getting quota: {str(e)}")


def create_challenge_quota(db: Session, user_id: str):
    try:
        # Check if quota already exists
        existing_quota = get_challenge_quota(db, user_id)
        if existing_quota:
            return existing_quota

        # Create new quota
        db_quota = models.ChallengeQuota(
            user_id=user_id,
            quota_remaining=100,  # Explicitly set default quota
            last_reset_date=datetime.now()
        )
        db.add(db_quota)
        db.commit()
        db.refresh(db_quota)
        return db_quota
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error while creating quota: {str(e)}")


def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    # Removed the daily reset logic - users keep their remaining quota
    return quota


def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str
):
    try:
        db_challenge = models.Challenge(
            difficulty=difficulty,
            created_by=created_by,
            title=title,
            options=options,
            correct_answer_id=correct_answer_id,
            explanation=explanation
        )
        db.add(db_challenge)
        db.commit()
        db.refresh(db_challenge)
        return db_challenge
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error while creating challenge: {str(e)}")


def get_user_challenges(db: Session, user_id: str):
    try:
        return db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error while getting user challenges: {str(e)}")
