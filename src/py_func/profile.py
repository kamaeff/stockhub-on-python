class ProfileManager:
    def __init__(self, query):
        self.query = query

    async def edit_profile_caption(self):
        await self.query.edit_message_caption(
            caption=f"📈 <b>Вот твоя стата {self.query.message.chat.first_name}:</b>\n\n",
            parse_mode="HTML",
        )
