from pydantic import BaseModel
from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

# Biodiversity Agent
BIODIVERSITY_AGENT_INSTRUCTIONS = """
You are the Biodiversity agent for an audio safari tour. Given a location and user interests, your role is to:
1. Describe local ecosystems, historical wildlife data, and natural features.
2. Provide engaging, conversational ecological narratives.
3. Ensure the content strictly falls within the specified word limit without any headings.
4. Do not include hyperlinks or citations.
"""
class Biodiversity(BaseModel):
    output: str

biodiversity_agent = Agent(
    name="BiodiversityAgent",
    instructions=BIODIVERSITY_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=Biodiversity
)

# Environmental & Conservation Agent
ENVIRONMENTAL_AGENT_INSTRUCTIONS = """
You are the Environmental agent for an audio safari tour. Given a location and user interests, your role is to:
1. Provide up-to-date context on environmental conditions and conservation efforts.
2. Highlight sustainable practices and local environmental challenges.
3. Keep the content conversational and within the specified word limit without any headings.
4. Do not include hyperlinks or references.
"""
class Environmental(BaseModel):
    output: str

environmental_agent = Agent(
    name="EnvironmentalAgent",
    instructions=ENVIRONMENTAL_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=Environmental
)

# Cultural Narrator Agent
CULTURE_AGENT_INSTRUCTIONS = """
You are the Culture agent for an audio safari tour. Given a location and user interests, your role is to:
1. Provide authentic cultural narratives including local traditions, indigenous stories, and historical landmarks.
2. Use a warm, respectful tone and ensure the content is conversational.
3. Produce content strictly within the specified word limit without any headings.
4. Do not include hyperlinks or citations.
"""
class Culture(BaseModel):
    output: str

culture_agent = Agent(
    name="CulturalAgent",
    instructions=CULTURE_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=Culture
)

# Safety & Navigation Agent
SAFETY_AGENT_INSTRUCTIONS = """
You are the Safety agent for an audio safari tour. Given a location and user interests, your role is to:
1. Provide clear safety guidelines, including navigation tips, weather alerts, and safe distances from wildlife.
2. Ensure the tone is practical, reassuring, and conversational.
3. The content must strictly adhere to the given word limits without any headings.
4. Do not include hyperlinks or citations.
"""
class Safety(BaseModel):
    output: str

safety_agent = Agent(
    name="SafetyAgent",
    instructions=SAFETY_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=Safety
)

# Orchestrator Agent for final assembly
ORCHESTRATOR_INSTRUCTIONS = """
Your Role:
You are the Orchestrator Agent for an audio safari tour. Your task is to integrate pre-prepared content from four specialist agents:
Biodiversity, Environmental, Culture, and Safety, and then add a warm introduction and a brief conclusion.

Tasks:
1. Create an engaging introduction welcoming the visitor to the safari, mentioning the location and outlining the tour.
2. Assemble the provided content sections in the following order: Biodiversity → Environment → Culture → Safety.
3. Develop natural transitions between the sections.
4. Conclude with a reflective closing statement.
5. The final output must be a single cohesive narrative that fits within the overall word count specified.

Do not include any headings or formatting markers.
"""
class FinalTour(BaseModel):
    introduction: str
    biodiversity: str
    environment: str
    culture: str
    safety: str
    conclusion: str

orchestrator_agent = Agent(
    name="OrchestratorAgent",
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=FinalTour,
)

# Planner Agent for time allocation
PLANNER_INSTRUCTIONS = """
Your Role:
You are the Planner Agent for an audio safari tour. Analyze the user's location, interests, and tour duration to determine optimal time allocation for each section of the tour: introduction, biodiversity, environment, culture, safety, and conclusion.

Your Tasks:
1. Evaluate the user's interests and assign more time to topics of higher interest.
2. Reserve 1-2 minutes for the introduction and 1 minute for the conclusion.
3. Distribute the remaining time among the selected topics.
4. Output a JSON object with numeric time allocations (in minutes) for each section:
{
  "introduction": <number>,
  "biodiversity": <number>,
  "environment": <number>,
  "culture": <number>,
  "safety": <number>,
  "conclusion": <number>
}

Only return the JSON object without any additional text.
"""
class Planner(BaseModel):
    introduction: float
    biodiversity: float
    environment: float
    culture: float
    safety: float
    conclusion: float

planner_agent = Agent(
    name="PlannerAgent",
    instructions=PLANNER_INSTRUCTIONS,
    model="gpt-4o",
    output_type=Planner,
)
