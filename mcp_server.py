from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

mcp = FastMCP("Job Recommendation")


@mcp.tool()
async def fetch_linkedin(search_query: str):
    return fetch_linkedin_jobs(search_query)


@mcp.tool()
async def fetch_naukri(search_query: str):
    return fetch_naukri_jobs(search_query)


if __name__ == "__main__":
    mcp.run(transport="stdio")
