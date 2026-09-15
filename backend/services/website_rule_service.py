from sqlalchemy.orm import Session
from models import WebsiteRule, User, UserWebsiteRule


def create_website_rules(domain: str, action: str, session: Session):
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
        raise ValueError("User not found")

    website_rule = (
        session.query(WebsiteRule).filter(WebsiteRule.id == website_rule_id).first()
    )

    if website_rule is None:
        raise ValueError("Website rule not found")

    existing_rule = (
        session.query(UserWebsiteRule)
        .filter(
            UserWebsiteRule.user_id == user_id,
            UserWebsiteRule.website_rule_id == website_rule_id,
        )
        .first()
    )

    if existing_rule:
        raise ValueError("User already has a rule for this website")
    
    user_website_rule=UserWebsiteRule(
        user_id=user_id,
        website_rule_id=website_rule_id,
        action=action
    )
    session.add(user_website_rule)
    session.commit()
    session.refresh(user_website_rule)

    return user_website_rule
