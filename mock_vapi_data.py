# Mock Vapi Data for Hackathon Test
CALL_ID = "call_12345"
RECORDING_URL = "https://vapi.ai/recordings/call_12345.mp3"

ASSISTANT_PROMPT = """
You are a helpful assistant for Falcon Point Maintenance. 
Your goal is to collect the caller's name, apartment number, and the issue they are facing.
SEQUENCE:
1. Greet the caller.
2. Ask for their name.
3. Ask for the apartment number.
4. Ask for the issue.
RULES:
- Never interrupt the caller.
- Always confirm the apartment number before ending the call.
"""

TRANSCRIPT = """
Agent: Hello, this is Falcon Point Maintenance. How can I help you?
Caller: Hi, my name is John Smith and I'm calling about a leak.
Agent: Oh, a leak? Where is the leak?
Caller: It's in the kitchen, under the sink.
Agent: Okay, and what's your apartment number?
Caller: I'm in 402.
Agent: Got it. I'll get someone over there.
Caller: Thanks, bye.
Agent: Goodbye.
"""
