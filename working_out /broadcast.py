from uagents import Agent, Bureau, Context, Model, Protocol
from uagents.setup import fund_agent_if_low

alice = Agent(name="alice", seed="alice recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase")
charles = Agent(name="charles", seed="charles recovery phrase")

for _agent in [alice, bob, charles]:
    fund_agent_if_low(_agent.wallet.address())

class BroadcastExampleRequest(Model):
    pass

class BroadcastExampleResponse(Model):
    text: str

proto = Protocol(name="proto", version="1.0")

proto.on_message(model=BroadcastExampleRequest, replies=BroadcastExampleResponse)
async def handle_request(ctx: Context, sender: str, _msg: BroadcastExampleRequest):
    await ctx.send(sender, BroadcastExampleResponse(text=f"Hello from {ctx.name}"))


alice.include(proto)
bob.include(proto)

@charles.on_interval(period=5.0)
async def say_hello(ctx: Context):
    await ctx.broadcast(proto.digest, message=BroadcastExampleRequest()) #uses the proto digest and send who ever has that protocol

@charles.on_message(model=BroadcastExampleResponse)
async def handle_response(ctx: Context, sender: str, msg:BroadcastExampleResponse):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")


bureau = Bureau(port=8000, endpoint="http://localhost:8000/submit")
bureau.add(alice)
bureau.add(bob)
bureau.add(charles)

if __name__ == "__main__":
    bureau.run()