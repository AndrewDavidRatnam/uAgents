import hashlib
from uagents import Agent, Bureau, Context, Model
from uagents.crypto import Identity 

class Message(Model):
    message:str
    digest: str # a string representing the SHA-256 hash of the message.
    signature: str # : a string representing the digital signature of the hash using the sender's private key.

"""
This function is used to hash a string message 
using the SHA-256 algorithm and return the resulting digest as bytes.
"""
def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()

alice = Agent(name="alice", seed="alice recovery password")
bob = Agent(name="bob", seed="bob recovery phrase")

@alice.on_interval(period=3.0)
async def send_message(ctx: Context):
    msg = "hello there bob"
    digest = encode(msg)
    
    await ctx.send(
        bob.address,
        Message(message=msg, digest=digest.hex(), signature=alice.sign_digest(digest))
    )

"""
alice_rx_message() function used to receive and process messages sent by bob:
"""
@alice.on_message(model=Message)
async def alice_rx_message(ctx: Context, sender: str, msg: Message):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify bob's message"
    ctx.logger.info("Bob's message verified!")
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

@bob.on_message(model=Message)
async def bob_rx_message(ctx: Context, sender:str, msg: Message):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), f"coudln't verify message from {sender}"

    ctx.logger.info("Alice's message verified")
    ctx.logger.info(f"Received message from sender {sender}: {msg.message}")

    reply_msg = "hello there alice"
    digest = encode(reply_msg)
    await ctx.send(
        alice.address,
        Message(message=reply_msg, digest=digest.hex(), signature=bob.sign_digest(digest))
    )

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()