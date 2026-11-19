import httpx
from typing import Optional, Dict, Any
from app.core.config import settings

class GitHubService:
    def __init__(self):
        self.base_url = settings.GITHUB_API_BASE_URL
        # Github API ko User-Agent header chahiye hota hai
        self.headers = {"User-Agent": "dev-kb-api-agent"}

    async def get_repo_details(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """
        GitHub URL se owner aur repo name nikal kar metadata fetch karta hai.
        Example: https://github.com/fastapi/fastapi -> owner: fastapi, repo: fastapi
        """
        try:
            # 1. URL parsing (Simple logic)
            parts = repo_url.rstrip("/").split("/")
            if len(parts) < 2 or "github.com" not in repo_url:
                return None
            
            owner, repo = parts[-2], parts[-1]
            api_url = f"{self.base_url}/repos/{owner}/{repo}"

            # 2. Async API Call (Like Axios)
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.get(api_url, timeout=10.0)
                
                if response.status_code != 200:
                    return None
                
                data = response.json()
                
                # 3. Zaruri data extract karna
                return {
                    "github_stars": data.get("stargazers_count", 0),
                    "github_language": data.get("language"),
                    "github_description": data.get("description"),
                    "github_open_issues": data.get("open_issues_count", 0),
                    "is_github": True
                }
        except Exception as e:
            print(f"Error fetching GitHub data: {e}")
            return None

# Singleton instance
github_service = GitHubService()