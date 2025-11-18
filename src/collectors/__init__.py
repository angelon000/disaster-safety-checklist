"""
Data collectors for KCL Checklist System
"""
from collectors.web_researcher import WebResearcher
from collectors.paper_researcher import PaperResearcher
from collectors.tech_researcher import TechResearcher
from collectors.api_researcher import APIResearcher

__all__ = [
    'WebResearcher',
    'PaperResearcher',
    'TechResearcher',
    'APIResearcher'
]
