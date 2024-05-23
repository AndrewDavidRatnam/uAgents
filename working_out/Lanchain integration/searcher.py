from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from uagents import Agent, Context, Protocol, Model
from pydantic import Field
from uagents.setup import fund_agent_if_low

from ai_engine import UAgentResponse, UAgentResponseType
class WikiReq(Model):
    search_keyword: str = Field(description="This describes the keyword you want to search on wiki")
 
searcher = Agent(name="searcher", seed="searcher", port=8001,
                  endpoint=["http://127.0.0.1:8001/submit"])
fund_agent_if_low(searcher.wallet.address())

@searcher.on_event("startup")
async def send_Wikireq(ctx:Context):
    
    add="agent1q075kyz9m7vr50l55u4z9f0edrjg3g9ddmt8xf6wattw30m2nl0wyvjjfwc"
    ctx.logger.info("Sending request to wiki search")
    await ctx.send(add,WikiReq(search_keyword="Itachi"))

fund_agent_if_low(searcher.wallet.address())
print(searcher.address)

if __name__ == "__main__":
    searcher.run()