from bot_app.domain.repositories.user_repositoriy import UserRepository


class HandleStartCommand:
    """Class for first visit"""
    def __init__(self, user_rep: UserRepository):
        self.user_rep = user_rep

    def execute(self,  user_id: int) -> None:
        self.user_rep.create_user(user_id)
