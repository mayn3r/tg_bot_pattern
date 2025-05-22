from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Dict, Awaitable, Any
from cache3 import Cache
from loguru import logger

from app.db_models import User


class UserRegisterMiddleware(BaseMiddleware):
    async def __call__(
                        self,
                        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                        event: Message,
                        data: Dict[str, Any]
                    ) -> Any:
        
        user_id: int = event.from_user.id # type: ignore
        username: str | None = event.from_user.username # type: ignore
        name: str | None = event.from_user.first_name # type: ignore
        
        
        user_model_cache = Cache('UserModels')
        
        if user_id in user_model_cache:
            user_model: User = Cache('UserModels')[user_id]
        else:
            user_model: User | None = await User.get_or_none(user_id=user_id) # type: ignore
            
            if not user_model:
                user_model: User = User(
                    user_id=user_id,
                    username=username,
                    name=name
                )
                
                await user_model.save()
            
            user_model_cache[user_id] = user_model

        data['user_model'] = user_model
        
        try:
            result = await handler(event, data)
            return result
        
        except Exception as e:
            logger.error('UserRegisterMiddleware: ' + str(e))