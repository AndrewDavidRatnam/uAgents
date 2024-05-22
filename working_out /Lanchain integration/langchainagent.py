from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from uagents import Agent, Context, Protocol, Model
from pydantic import Field
from uagents.setup import fund_agent_if_low

from ai_engine import UAgentResponse, UAgentResponseType

 
lang_chain_agent = Agent(name="lang_chain_agent", 
                         seed="lang_chain_agent recovery phrase",
                         endpoint=["http://127.0.0.1:8000/submit"])

fund_agent_if_low(lang_chain_agent.wallet.address())
print(lang_chain_agent.address)
if __name__ == "__main__":
    lang_chain_agent.run()