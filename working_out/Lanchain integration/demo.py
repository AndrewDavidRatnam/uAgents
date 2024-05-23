from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol, Model
from pydantic import Field
from ai_engine import UAgentResponse, UAgentResponseType
import asyncio 
# Extend your protocol with Wikipedia data fetching
class WikiReq(Model):
    search_keyword: str = Field(description="This describes the keyword you want to search on wiki")


 
# SEED_PHRASE = "lang_chain_agent recovery phrase"
 
# # Copy the address shown below
# print(f"Your agent's address is: {Agent(seed=SEED_PHRASE).address}")
 
# AGENT_MAILBOX_KEY = "5934106a-ebb5-449e-8b78-229f8744e2a5"
 
# Now your agent is ready to join the agentverse!
WikiAgent = Agent(
    name="Wiki Agent",
    seed="WikiAgent",
    port=8000,
     endpoint=["http://127.0.0.1:8000/submit"]
)
fund_agent_if_low(WikiAgent.wallet.address()) #funding agent.
print(WikiAgent.address)
wiki_protocol = Protocol("Wiki Protocol")

 
@wiki_protocol.on_message(model=WikiReq)
async def load_dalle(ctx: Context, sender: str, msg: WikiReq):
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    ctx.logger.info(msg.search_keyword)
    try:
        result = wikipedia.run(msg.search_keyword)
    except Exception as e:
        ctx.logger.info(f"Error generating response: {e}")
    # Send an error response back to the user
    # await ctx.send(
    #     sender, UAgentResponse(message=str(result), type=UAgentResponseType.FINAL)
    # )
    print(result)
 
WikiAgent.include(wiki_protocol, publish_manifest=True)
WikiAgent.run()


