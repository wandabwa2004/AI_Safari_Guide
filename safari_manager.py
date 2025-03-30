from __future__ import annotations
import asyncio
import json
from rich.console import Console

from agents import Runner, RunResult, custom_span, gen_trace_id, trace
from agents_util import (
    Biodiversity, biodiversity_agent,
    Environmental, environmental_agent,
    Culture, culture_agent,
    Safety, safety_agent,
    Planner, planner_agent,
    FinalTour, orchestrator_agent
)
from printer import Printer

class SafariManager:
    """
    Orchestrates the full safari tour flow.
    """

    def __init__(self) -> None:
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, query: str, interests: list, duration: str, language: str) -> str:
        trace_id = gen_trace_id()
        with trace("Safari Research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/{trace_id}",
                is_done=True,
                hide_checkmark=True,
            )
            self.printer.update_item("start", "Starting safari research...", is_done=True)
            
            # Get planning based on location, interests, duration, and language
            planner = await self._get_plan(query, interests, duration, language)
            
            research_results = {}
            words_per_minute = 150
            total_words = int(duration) * words_per_minute
            words_per_section = total_words // len(interests)

            if "Biodiversity" in interests:
                research_results["biodiversity"] = await self._get_biodiversity(query, interests, words_per_section, language)
            if "Environment" in interests:
                research_results["environment"] = await self._get_environment(query, interests, words_per_section, language)
            if "Culture" in interests:
                research_results["culture"] = await self._get_culture(query, interests, words_per_section, language)
            if "Safety" in interests:
                research_results["safety"] = await self._get_safety(query, interests, words_per_section, language)
            
            final_tour = await self._get_final_tour(query, interests, duration, research_results, language)
            self.printer.update_item("final_report", "", is_done=True)
            self.printer.end()

            sections = []
            if "Biodiversity" in interests:
                sections.append(final_tour.biodiversity)
            if "Environment" in interests:
                sections.append(final_tour.environment)
            if "Culture" in interests:
                sections.append(final_tour.culture)
            if "Safety" in interests:
                sections.append(final_tour.safety)

            final = "\n\n".join(sections)
            return final

    async def _get_plan(self, query: str, interests: list, duration: str, language: str) -> Planner:
        self.printer.update_item("Planner", "Planning your safari tour...")
        prompt = f"Language: {language}\nQuery: {query} Interests: {', '.join(interests)} Duration: {duration}"
        result = await Runner.run(planner_agent, prompt)
        self.printer.update_item("Planner", "Completed planning", is_done=True)
        return result.final_output_as(Planner)

    async def _get_biodiversity(self, query: str, interests: list, word_limit: int, language: str) -> Biodiversity:
        self.printer.update_item("Biodiversity", "Curating ecological and biodiversity insights...")
        prompt = (
            f"Language: {language}\nQuery: {query} Interests: {', '.join(interests)} Word Limit: {word_limit} - {word_limit + 20}\n\n"
            "Instructions: Create engaging ecological content for an audio safari tour. "
            "Focus on local ecosystems and historical wildlife data. Keep it conversational."
        )
        result = await Runner.run(biodiversity_agent, prompt)
        self.printer.update_item("Biodiversity", "Completed biodiversity research", is_done=True)
        return result.final_output_as(Biodiversity)

    async def _get_environment(self, query: str, interests: list, word_limit: int, language: str) -> Environmental:
        self.printer.update_item("Environment", "Gathering environmental insights...")
        prompt = (
            f"Language: {language}\nQuery: {query} Interests: {', '.join(interests)} Word Limit: {word_limit} - {word_limit + 20}\n\n"
            "Instructions: Create engaging environmental content for an audio safari tour. "
            "Highlight conservation efforts and current environmental conditions. Keep it conversational."
        )
        result = await Runner.run(environmental_agent, prompt)
        self.printer.update_item("Environment", "Completed environmental research", is_done=True)
        return result.final_output_as(Environmental)

    async def _get_culture(self, query: str, interests: list, word_limit: int, language: str) -> Culture:
        self.printer.update_item("Culture", "Exploring cultural narratives...")
        prompt = (
            f"Language: {language}\nQuery: {query} Interests: {', '.join(interests)} Word Limit: {word_limit} - {word_limit + 20}\n\n"
            "Instructions: Create engaging cultural content for an audio safari tour. "
            "Focus on local traditions and indigenous stories. Keep it conversational."
        )
        result = await Runner.run(culture_agent, prompt)
        self.printer.update_item("Culture", "Completed cultural research", is_done=True)
        return result.final_output_as(Culture)

    async def _get_safety(self, query: str, interests: list, word_limit: int, language: str) -> Safety:
        self.printer.update_item("Safety", "Collecting safety guidelines...")
        prompt = (
            f"Language: {language}\nQuery: {query} Interests: {', '.join(interests)} Word Limit: {word_limit} - {word_limit + 20}\n\n"
            "Instructions: Create clear safety and navigation content for an audio safari tour. "
            "Provide practical advice in a conversational tone."
        )
        result = await Runner.run(safety_agent, prompt)
        self.printer.update_item("Safety", "Completed safety research", is_done=True)
        return result.final_output_as(Safety)

    async def _get_final_tour(self, query: str, interests: list, duration: float, research_results: dict, language: str) -> FinalTour:
        self.printer.update_item("Final Tour", "Assembling your complete safari tour...")
        content_sections = []
        for interest in interests:
            key = interest.lower()
            if key in research_results:
                content_sections.append(research_results[key].output)
        
        words_per_minute = 150
        total_words = int(duration) * words_per_minute
        
        prompt = (
            f"Language: {language}\nQuery: {query}\nSelected Interests: {', '.join(interests)}\n"
            f"Total Safari Tour Duration (minutes): {duration}\nTarget Word Count: {total_words}\n\n"
            "Content Sections:\n" + "\n\n".join(content_sections) + "\n\n"
            "Instructions: Create a cohesive, conversational audio safari tour guide that integrates the "
            "provided sections seamlessly. Start with an inviting introduction and conclude with a reflective closing. "
            f"Ensure the final output is approximately {total_words} words."
        )
        result = await Runner.run(orchestrator_agent, prompt)
        self.printer.update_item("Final Tour", "Completed final safari tour creation", is_done=True)
        return result.final_output_as(FinalTour)

