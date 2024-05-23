from uagents import Agent, Context, Model

class QueryRequest(Model):
    query: str

class Response(Model):
    text: str

QueryAgent = Agent(
    name="Query Agent",
    seed="Query Agent Seed Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

print(QueryAgent.address)

@QueryAgent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {QueryAgent.name}")
    ctx.logger.info(f"With address: {QueryAgent.address}")
    ctx.logger.info(f"And wallet address: {QueryAgent.wallet.address}")

@QueryAgent.on_query(model=QueryRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: QueryRequest):
    ctx.logger.info("Query received")
    try:
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

if __name__ =="__main__":
    QueryAgent.run()