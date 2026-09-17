from sqlalchemy.orm import Session
from models import WebsiteRule, User, UserWebsiteRule
from exceptions.website_rule_exception import (
    WebsiteRuleAlreadyExistsException,
    WebsiteRuleNotFoundException,
    UserWebsiteRuleAlreadyExistsException,
    UserNotFoundForWebsiteRuleException,
    UserWebsiteRuleNotFoundException,
)


def create_website_rules(domain: str, action: str, session: Session):

    existing_rule = (
        session.query(WebsiteRule).filter(WebsiteRule.domain == domain).first()
    )

    if existing_rule:
        raise WebsiteRuleAlreadyExistsException()

    website_rule = WebsiteRule(
        domain=domain,
        action=action,
    )

    session.add(website_rule)
    session.commit()
    session.refresh(website_rule)

    return website_rule


def create_user_website_rule(
    user_id: int, website_rule_id: int, action: str, session: Session
):
    user = session.query(User).filter(User.id == user_id).first()

    if user is None:
        raise UserNotFoundForWebsiteRuleException()

    website_rule = (
        session.query(WebsiteRule).filter(WebsiteRule.id == website_rule_id).first()
    )

    if website_rule is None:
        raise WebsiteRuleNotFoundException()

    existing_rule = (
        session.query(UserWebsiteRule)
        .filter(
            UserWebsiteRule.user_id == user_id,
            UserWebsiteRule.website_rule_id == website_rule_id,
        )
        .first()
    )

    if existing_rule:
        raise UserWebsiteRuleAlreadyExistsException()

    user_website_rule = UserWebsiteRule(
        user_id=user_id, website_rule_id=website_rule_id, action=action
    )
    session.add(user_website_rule)
    session.commit()
    session.refresh(user_website_rule)

    return user_website_rule


def get_all_website_rules(session: Session):
    return session.query(WebsiteRule).all()


def get_user_website_rules(user_id: int, session: Session):
    return (
        session.query(UserWebsiteRule).filter(UserWebsiteRule.user_id == user_id).all()
    )


def update_website_rule(Website_rule_id: int, action: str, session: Session):
    website_rule = (
        session.query(WebsiteRule).filter(WebsiteRule.id == Website_rule_id).first()
    )
    if website_rule is None:
        raise WebsiteRuleNotFoundException()

    website_rule.action = action

    session.commit()
    session.refresh(website_rule)

    return website_rule


def delete_website_rule(website_rule_id: int, session: Session):
    website_rule = (
        session.query(WebsiteRule).filter(WebsiteRule.id == website_rule_id).first()
    )

    if website_rule is None:
        raise WebsiteRuleNotFoundException()

    session.query(UserWebsiteRule).filter(
        UserWebsiteRule.website_rule_id == website_rule_id
    ).delete(synchronize_session=False)

    session.delete(website_rule)
    session.commit()

    return {"message": "Website rule deleted successfully"}


def update_user_website_rule(user_website_rule_id: int, action: str, session: Session):
    user_website_rule = (
        session.query(UserWebsiteRule)
        .filter(UserWebsiteRule.id == user_website_rule_id)
        .first()
    )

    if user_website_rule is None:
        raise UserWebsiteRuleNotFoundException()

    user_website_rule.action = action
    session.commit()
    session.refresh(user_website_rule)
    return user_website_rule


def delete_user_website_rule(user_website_rule_id: int, session: Session):
    user_website_rule = (
        session.query(UserWebsiteRule)
        .filter(UserWebsiteRule.id == user_website_rule_id)
        .first()
    )

    if user_website_rule is None:
        raise UserWebsiteRuleNotFoundException()

    session.delete(user_website_rule)
    session.commit()
    return {"message": "User website rule deleted successfully"}
