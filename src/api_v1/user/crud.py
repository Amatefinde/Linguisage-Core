from datetime import datetime

from src.core.database import db_helper
from src.core.database.models import User


async def set_user_last_verified_by_now(user: User):
    async with db_helper.session_factory() as session:
        db_user = await session.get(User, user.id)
        db_user.last_verification_request = datetime.utcnow()
        await session.commit()
