from django.contrib.auth import models

class DiscordUserOAuth2Manager(models.UserManager):
    def createNewUser(self, user):
        newUser = self.create(
                id = user["id"],
                discordTag = f"{user['username']}#{user['discriminator']}",
                avatar = user["avatar"],
                publicFlags = user["public_flags"],
                flags = user["flags"],
                locale = user["locale"],
                mfaEnabled = user["mfa_enabled"]
            )
        return newUser