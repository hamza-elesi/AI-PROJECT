import asyncio
import os
from dotenv import load_dotenv
from moz_api import MozClient  # Ensure the path to MozClient is correct

# Mock RateLimiter for testing
class MockRateLimiter:
    async def wait_if_needed(self, api_name: str):
        """Simulate rate limiting."""
        print(f"Simulating rate limiting for {api_name} API")
        await asyncio.sleep(0.1)

async def main():
    load_dotenv()  # Load environment variables
    moz_token = os.getenv("MOZ_TOKEN")
    if not moz_token:
        print("Error: MOZ_TOKEN is not set in the environment variables.")
        return

    # Initialize MozClient
    rate_limiter = MockRateLimiter()
    moz_client = MozClient(api_token=moz_token, rate_limiter=rate_limiter)

    # Replace with a domain to test
    domain = "https://example.com"

    print(f"Fetching metrics for domain: {domain}")
    metrics = await moz_client.get_domain_metrics(domain)

    print("Metrics fetched:")
    print(metrics)

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
