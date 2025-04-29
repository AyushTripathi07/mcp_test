# server.py
from mcp.server.fastmcp import FastMCP
from memory_store import KnowledgeGraphManager
from typing import List, Dict

mcp = FastMCP("Knowledge Memory Server")
kg = KnowledgeGraphManager()


@mcp.tool()
def create_entities(entities: List[Dict]) -> List[Dict]:
    """Create multiple new entities in the knowledge graph"""
    return kg.create_entities(entities)


@mcp.tool()
def create_relations(relations: List[Dict]) -> List[Dict]:
    """Create multiple new relations between entities"""
    return kg.create_relations(relations)


@mcp.tool()
def add_observations(observations: List[Dict]) -> List[Dict]:
    """Add new observations to existing entities"""
    return kg.add_observations(observations)


@mcp.tool()
def delete_entities(entityNames: List[str]) -> str:
    """Delete entities and their relations"""
    kg.delete_entities(entityNames)
    return "Entities deleted."


@mcp.tool()
def delete_observations(deletions: List[Dict]) -> str:
    """Delete specific observations from entities"""
    kg.delete_observations(deletions)
    return "Observations deleted."


@mcp.tool()
def delete_relations(relations: List[Dict]) -> str:
    """Delete specific relations"""
    kg.delete_relations(relations)
    return "Relations deleted."


@mcp.tool()
def read_graph() -> Dict:
    """Read the entire knowledge graph"""
    return kg.read_graph()


@mcp.tool()
def search_nodes(query: str) -> Dict:
    """Search for matching entities and relations"""
    return kg.search_nodes(query)


@mcp.tool()
def open_nodes(names: List[str]) -> Dict:
    """Open specific nodes by name"""
    return kg.open_nodes(names)


if __name__ == "__main__":
    mcp.run()