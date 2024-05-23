from uagents import Agent, Context, Model, Bureau

class Transaction(Model):
    transaction_type: str
    amount: float

# Define the agent for user interaction
interaction_agent = Agent(name="interaction_agent",
                          port=8001)

# Define the agent for storing user input
storage_agent = Agent(name="storage_agent",
                      port=8002)

@interaction_agent.on_message(model=Transaction)  # Specify the model
async def handle_interaction(ctx: Context, sender: str, msg: Transaction):
    # Check if the message contains options for expenses or income
    if msg.transaction_type.lower() == "expenses":
        ctx.logger.info("Please enter the expense amount:")
        # Send a message to the storage agent to store the expense
        await storage_agent.store_expense(msg.amount)
    elif msg.transaction_type.lower() == "income":
        ctx.logger.info("Please enter the income amount:")
        # Send a message to the storage agent to store the income
        await storage_agent.store_income(msg.amount)
    else:
        ctx.logger.info("Invalid option. Please choose 'expenses' or 'income'.")

@storage_agent.on_event("startup")  # Adjust the period as needed
async def auto_store(ctx: Context):
    # Automatic storage of user input
    # Assuming user input is received here and stored accordingly
    expense_amount =  input("Enter expense amount: ")
    income_amount = input("Enter income amount: ")
    ctx.logger.info(f"Expense of {expense_amount} and income of {income_amount} stored automatically.")


bureau = Bureau()
bureau.add(storage_agent)
bureau.add(interaction_agent)

if __name__ == "__main__":
    bureau.run()
# if __name__ == "__main__":
#     interaction_agent.run()
#     storage_agent.run()