from vkbottle.bot import BotLabeler, rules

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(456850585)]

@admin_labeler.message(command="halt")
async def halt(_):
    exit(0)
