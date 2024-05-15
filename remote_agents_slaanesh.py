from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class Message(Model):
    message: str

RECIPIENT_ADDRESS="" 
#need to design a helper function to use already known addresses and update different addresses coming in
#now manually create another agent and then update it

slaanesh= Agent(
    name="slanaesh",
    port=8001,
    seed="slaanesh secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"]
)

print(slaanesh.address) #to get address

fund_agent_if_low(slaanesh.wallet.address())

@slaanesh.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message ):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    await ctx.send(sender, Message(message=f"hello there {sender}"))

if __name__ == "__main__":
    slaanesh.run()
