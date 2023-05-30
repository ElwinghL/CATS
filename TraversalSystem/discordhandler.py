import random
from discord import Webhook, Embed

global lastSent
global lastEmbed


async def post_to_discord(subject, webhook_url, message, routeName, session, thread=None):

    global lastSent
    photo = getPhoto()

    try:
        webhook = Webhook.from_url(webhook_url, session=session)

        embed = Embed(title=subject, description=message)
        embed.set_footer(text="Carrier Administration and Traversal System")
        embed.set_author(name=routeName)
        embed.set_image(url=photo)

        if (thread != None):
            lastSent = await webhook.send(embed=embed, wait=True, thread=thread)
        else:
            lastSent = await webhook.send(embed=embed, wait=True)

    except:
        print("Discord webhook not set up")


async def post_with_fields(subject, webhook_url, message, routeName, carrierStage, maintenanceStage, session, thread=None):
    global lastSent
    global lastEmbed
    photo = getPhoto()

    try:
        webhook = Webhook.from_url(webhook_url, session=session)

        lastEmbed = embed = Embed(title=subject, description=message)
        embed.set_image(url=photo)
        embed.set_author(name=routeName)
        embed.set_footer(text="Carrier Administration and Traversal System")

        embed.add_field(name="Jump stage", value=carrierStage)
        embed.add_field(name="Maintenance stage", value=maintenanceStage)

        webhook.add_embed(embed)

        if (thread != None):
            lastSent = await webhook.send(embed=embed, wait=True, thread=thread)
        else:
            lastSent = await webhook.send(embed=embed, wait=True)

    except:
        print("Discord webhook not set up")


async def update_fields(carrierStage, maintenanceStage):
    global lastSent
    global lastEmbed

    try:
        default_carrier_stage = "Waiting...\nJump locked\nLockdown protocol active\nPowering FSD\nInitiating FSD\nEntering hyperspace portal\nTraversing hyperspace\nExiting hyperspace portal\nFSD cooling down\nJump complete"

        default_maintenance_stage = "Waiting\nPreparing carrier for hyperspace\nServices taken down\nLanding pads retracting\nBulkheads closing\nAirlocks sealing\nTask confirmation\nWaiting\nRestocking Tritium\nDone"

        c_stage_list = default_carrier_stage.split("\n")
        m_stage_list = default_maintenance_stage.split("\n")

        new_carrier_stage = ""
        new_maintenance_stage = ""

        i = 0
        for stage in c_stage_list:
            if i < carrierStage:
                new_carrier_stage += "~~" + stage + "~~\n"
            elif i == carrierStage:
                new_carrier_stage += "**" + stage + "**\n"
            else:
                new_carrier_stage += stage + "\n"
            i += 1

        i = 0
        for stage in m_stage_list:
            if i < maintenanceStage:
                new_maintenance_stage += "~~" + stage + "~~\n"
            elif i == maintenanceStage:
                new_maintenance_stage += "**" + stage + "**\n"
            else:
                new_maintenance_stage += stage + "\n"
            i += 1

        lastEmbed.clear_fields()

        lastEmbed.add_field(name="Jump stage", value=new_carrier_stage)
        lastEmbed.add_field(name="Maintenance stage",
                            value=new_maintenance_stage)

        await lastSent.edit(embed=lastEmbed)
    except:
        print("Discord webhook not set up")


def getPhoto():
    with open("photos.txt", "r") as photosFile:
        return random.choice(photosFile.read().split("\n"))
