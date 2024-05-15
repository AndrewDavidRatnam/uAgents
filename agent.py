from uagents import Agent, Context
 
alice = Agent(name="alice", seed="alice recovery phrase")
 
# print("uAgent address: ", alice.address)

# @alice.on_event("startup")
# async def say_hello(ctx: Context):
#     ctx.logger.info(f'hello, my name is {ctx.name}')
#     ctx.logger.info(f"Fetch network address{ctx.wallet.address()}" )
#     ctx.logger.info(f"uAgent address is:  {ctx.address}")
#     print("uAgent address: ", alice.address)
#     print(ctx == alice)

@alice.on_interval(period=1.0)
async def on_interval(ctx: Context):
    # class keyVakueStore
    #  def set(self, key: str, value: Any):
    #     self._data[key] = value
    #     self._save()

    current_count = ctx.storage.get("count") or 0

    ctx.logger.info(f"My count is: {current_count}")

    ctx.storage.set("count", current_count + 1)

 
if __name__ == "__main__":
    alice.run()