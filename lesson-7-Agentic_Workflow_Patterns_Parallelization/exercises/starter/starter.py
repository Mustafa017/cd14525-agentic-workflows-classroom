import os
from openai import OpenAI
from dotenv import load_dotenv
import threading

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(system_prompt, user_prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125", messages=[
        {"role": "system", "content":system_prompt},
        {"role": "user", "content":user_prompt}
    ])

    return response.choices[0].message.content


# Shared dict for thread-safe collection of agent outputs
agent_outputs = {}

# Example contract text (in a real application, this would be loaded from a file)
contract_text = """
CONSULTING AGREEMENT

This Consulting Agreement (the "Agreement") is made effective as of January 1, 2025 (the "Effective Date"), by and between ABC Corporation, a Delaware corporation ("Client"), and XYZ Consulting LLC, a California limited liability company ("Consultant").

1. SERVICES. Consultant shall provide Client with the following services: strategic business consulting, market analysis, and technology implementation advice (the "Services").

2. TERM. This Agreement shall commence on the Effective Date and shall continue for a period of 12 months, unless earlier terminated.

3. COMPENSATION. Client shall pay Consultant a fee of $10,000 per month for Services rendered. Payment shall be made within 30 days of receipt of Consultant's invoice.

4. CONFIDENTIALITY. Consultant acknowledges that during the engagement, Consultant may have access to confidential information. Consultant agrees to maintain the confidentiality of all such information.

5. INTELLECTUAL PROPERTY. All materials developed by Consultant shall be the property of Client. Consultant assigns all right, title, and interest in such materials to Client.

6. TERMINATION. Either party may terminate this Agreement with 30 days' written notice. Client shall pay Consultant for Services performed through the termination date.

7. GOVERNING LAW. This Agreement shall be governed by the laws of the State of Delaware.

8. LIMITATION OF LIABILITY. Consultant's liability shall be limited to the amount of fees paid by Client under this Agreement.

9. INDEMNIFICATION. Client shall indemnify Consultant against all claims arising from use of materials provided by Client.

10. ENTIRE AGREEMENT. This Agreement constitutes the entire understanding between the parties and supersedes all prior agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
"""

# TODO: Implement these agent classes

class LegalTermsChecker:
    """Agent that checks for problematic legal terms and clauses in contracts."""
    def run(self, contract_text):
        # DONE: Implement this method to analyze legal terms
        print("LegalTermsChecker: Analyzing contract for problematic legal terms...")
        system_prompt = """You are a legal expert specializing in contract law. 
        Review the provided contract text and identify any problematic clauses, ambiguous terms, 
        or non-standard legal language. List your key findings.
        """
        user_prompt = f""" Analyze : {contract_text} """
        agent_outputs['legal'] = call_openai(system_prompt, user_prompt)

class ComplianceValidator:
    """Agent that validates regulatory and industry compliance of contracts."""
    def run(self, contract_text):
        # DONE: Implement this method to check compliance
        print("ComplianceValidator: Analyzing contracts and business practices for legal compliance...")
        system_prompt = """You are a Compliance Validator specializing in contract law and business regulation. 
        Your primary purpose is to ensure organizations adhere to legal standards and regulations by assessing compliance,
        monitoring legal changes, and recommending compliance programs.  

        **Task Scope:**  
        - Do: Analyze contracts and business practices for legal compliance, identify regulatory risks, and suggest corrective actions.  
        - Do Not: Provide legal advice or represent clients in legal matters.  

        **Output Format:**  
        - Structure responses as: [Summary] → [Key Findings] → [Recommended Actions].  
        - Keep responses under 300 words unless complex analysis is required.  
        - Use bullet points for clarity.  
        - Example:  
        *[Summary]* This clause violates GDPR Article 17.  
        *[Key Findings]* Missing data deletion protocols.  
        *[Recommended Actions]* Add a 30-day data retention limit and deletion process.  

        **Personality and Tone:**  
        - Professional, precise, and cautious. Avoid speculation; base responses on verified regulations.  

        **Constraints and Guardrails:**  
        - Never interpret laws beyond your expertise or guarantee legal outcomes.  
        - Flag uncertain cases with: "Consult a qualified attorney for clarification."  

        **Edge Case Handling:**  
        - If a request is unclear, ask for specific contract excerpts or regulations to review.  
        - For out-of-scope queries (e.g., litigation), redirect to legal counsel.
                
        """
        user_prompt = f""" Analyze : {contract_text} """
        agent_outputs['compliance'] = call_openai(system_prompt, user_prompt)

class FinancialRiskAssessor:
    """Agent that assesses financial risks and liabilities in contracts."""
    def run(self, contract_text):
        # DONE: Implement this method to evaluate financial risks
        print("FinancialRiskAssessor: Evaluating potential financial losses related to legal actions or non-compliance...")
        system_prompt = """
        You are a Financial Risk Assessor specializing in contract law and business regulation. 
        Your primary purpose is to evaluate potential financial losses related to legal actions 
        or non-compliance, helping clients make informed decisions.

        Your task scope includes:
        - Analyzing financial implications of legal risks in contracts, agreements, or regulatory matters
        - Providing risk exposure assessments and mitigation strategies
        - Offering insights on financial investments with legal considerations
        You do NOT provide:
        - Legal advice (always recommend consulting a qualified attorney)
        - Tax advice
        - Personal financial planning

        Output format:
        - Responses should be structured as: [Risk Level] → [Key Findings] → [Recommended Actions]
        - Keep answers concise (3-5 sentences for simple queries, up to 200 words for complex cases)
        - Use professional tone with clear financial terminology
        - Include numerical estimates when possible (e.g., "Potential exposure: $50k-$75k")

        Personality and tone:
        - Professional yet approachable
        - Fact-based and data-driven
        - Cautious when making projections
        - Transparent about uncertainty

        Constraints:
        - Never guarantee outcomes
        - Never bypass recommending legal counsel for interpretation
        - Never provide advice outside financial risk assessment
        - Never comment on ongoing legal cases

        Edge case handling:
        - For unclear requests: "Could you clarify the contract clause/regulation you're concerned about?"
        - For out-of-scope requests: "As a financial risk assessor, I can't advise on [topic]. You may want to consult a [relevant professional]."
        - When uncertain: "Based on typical cases, [general guidance], but consult your legal team for specifics."

        Example response:
        "[Moderate Risk] → This non-compete clause could expose you to $100k in potential damages if enforced. → Recommended: 
        1) Limit duration to 12 months, 2) Define geographic scope precisely, 3) Budget $15k for potential litigation costs.        
        """
        user_prompt = f""" Analyze : {contract_text} """
        agent_outputs['financial'] = call_openai(system_prompt, user_prompt)

class SummaryAgent:
    """Agent that synthesizes findings from all specialized agents."""
    def run(self, contract_text, inputs):
        # TODO: Implement this method to create a comprehensive summary
        print("SummaryAgent: Synthesizing all findings...")
        legal_findings = inputs.get('legal', 'No legal analysis found')
        compliance_findings = inputs.get('compliance', 'No compliance analysis found')
        financial_findings = inputs.get('financial', 'No financial analysis found')

        system_prompt = """You are a senior legal counsel. You have received analyses on a contract from legal terms, 
        compliance, and financial risk specialists. Your task is to synthesize these findings into a single, comprehensive 
        executive summary of the contract's overall status and key concerns."""

        user_prompt = f"""Please synthesize the following analyses of a contract into a comprehensive summary report.
        Original Contract Text (for reference, if needed, but focus on the analyses):
        --- BEGIN CONTRACT TEXT (abbreviated for prompt, or just mention it was analyzed) ---
        {contract_text[:500]}... 
        --- END CONTRACT TEXT ---
        Legal Terms Analysis:
        {legal_findings}
        Compliance Validation:
        {compliance_findings}
        Financial Risk Assessment:
        {financial_findings}
        Provide a consolidated executive summary identifying key issues and an overall assessment.
        """
        return call_openai(system_prompt, user_prompt)

# Main function to run all agents in parallel
def analyze_contract(contract_text):
    """Run all agents in parallel and summarize their findings."""
    # TODO: Implement parallel execution of agents
    # 1. Create agent instances
    legal_agent = LegalTermsChecker()
    compliance_agent = ComplianceValidator()
    financial_agent = FinancialRiskAssessor()
    summary_agent = SummaryAgent()

    # 2. Run them in parallel using threading
    threads = []
    all_agents = [legal_agent, compliance_agent, financial_agent]
    for agent in all_agents:
        t = threading.Thread(target=agent.run, args=(contract_text,))
        threads.append(t)

    # Start each thread
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # 3. Collect their outputs
    # 4. Generate a summary using the SummaryAgent
    final_report = summary_agent.run(contract_text, agent_outputs)
    # 5. Return the final analysis
    return final_report

if __name__ == "__main__":
    print("Enterprise Contract Analysis System")
    print("Analyzing contract...")
    
    # TODO: Call the analyze_contract function and print results
    final_analysis = analyze_contract(contract_text)
    print("\n=== FINAL CONTRACT ANALYSIS ===\n")
    print(final_analysis)