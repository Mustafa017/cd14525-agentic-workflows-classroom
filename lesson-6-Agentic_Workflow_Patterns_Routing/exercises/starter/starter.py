import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# --- Helper Function for API Calls ---
def call_openai(system_prompt, user_prompt, model="gpt-3.5-turbo"):
    """Simple wrapper for OpenAI API calls."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content


# --- Agents for Different Retail Tasks ---

def product_researcher_agent(query):
    """Product researcher agent gathers product information."""
    system_prompt = """You are a product research agent for a retail company. Your task is to provide 
    structured information about products, market trends, and competitor pricing."""
    
    user_prompt = f"Research this product thoroughly: {query}"
    return call_openai(system_prompt, user_prompt)


def customer_analyzer_agent(query):
    """Customer analyzer agent processes customer data and feedback."""
    system_prompt = """You are a customer analysis agent. Your task is to analyze customer feedback, 
    preferences, and purchasing patterns."""
    
    user_prompt = f"Analyze customer behavior for: {query}"
    return call_openai(system_prompt, user_prompt)


def pricing_strategist_agent(query, product_data=None, customer_data=None):
    """Pricing strategist agent recommends optimal pricing."""
    system_prompt = """You are a pricing strategist agent. Your task is to recommend optimal pricing 
    strategies based on product research and customer analysis."""
    
    # Done: Implement this function
    # It should use product_data and customer_data to inform the pricing strategy
    # Replace this with your implementation
    user_prompt = f"""
    Original Pricing Query: {query}
    Product Research Data:{product_data}
    Customer Analysis Data:{customer_data}
    Based on all the above information, please provide a recommended pricing strategy, suggest an
    optimal price or price range, and explain your reasoning."""

    return call_openai(system_prompt, user_prompt)


# --- Routing Agent with LLM-Based Task Determination ---
def routing_agent(query, *args):
    """Routing agent that determines which agent to use based on the query."""
    
    # Done: Implement the routing agent
    # 1. Use an LLM to analyze the query and determine the correct task type
    # 2. Route the query to the appropriate agent
    # 3. Return the results from the chosen agent
    # Replace this with your implementation
    
    agent_descriptions = "\n".join([f" - {agent.__name__} : {agent.__doc__}" for agent in args])
    # print(agent_descriptions)

    system_prompt = f"""You are an expert routing agent. your task is to recommend the best agent to run the query.
    agent descriptions:{agent_descriptions}
    query:{query}
    Respond only with the exact agent name (e.g., '{args[0].__name__}'), and nothing else.    
    """

    user_prompt = f"""Given the query {query}, which is the right agent to handle this? """

    agent_choice_name = call_openai(system_prompt, user_prompt)
    # print(agent_choice_name)

    for agent in args:
        if agent.__name__ == agent_choice_name:
            print(f"--- Routing task to {agent.__name__}... ---")
            return agent(query)

    return f"Error: Could not find an agent named '{agent_choice_name}'. Please check the routing prompt."





# --- Example Usage ---
if __name__ == "__main__":
    # Example queries
    queries = [
        "What are the specifications and current market trends for wireless earbuds?",
        "What do customers think about our premium coffee brand?",
        "What should be the optimal price for our new organic skincare line?"
    ]

    all_agents = [product_researcher_agent, customer_analyzer_agent, pricing_strategist_agent]

    
    # Process each query
    for query in queries:
        print(f"\nQuery: {query}")
        print("\nProcessing...")
        
        # Done: Use the routing agent to process the query
        results = routing_agent(query, *all_agents)
        # Print the results
        print(results)
        print("\n" + "-"*80)