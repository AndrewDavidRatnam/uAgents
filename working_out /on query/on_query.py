import json
import asyncio
from uagents import Model
from uagents.query import query

AGENT_ADDRESS = "agent1qgfytc9e7ketwqc06xndvjmznqgr3md8w43hzxdv2hasp25ya43j2mnd32e"

class QueryRequest(Model):
    query: str

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]

async def make_agent_call(req: QueryRequest):
    try:
        response = await agent_query(req)
        return f"successful call - agent response: {response}"
    except Exception:
        return "unsuccessful agent call"
    
if __name__ == "__main__":
    request = QueryRequest(query="Your query here")
    print(asyncio.run(make_agent_call(request)))
