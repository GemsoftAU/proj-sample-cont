import httpx
from rich import print
from rich.panel import Panel

response = httpx.get("https://httpbin.org/get")
data = response.json()

print(Panel(f"[bold green]Connected successfully![/bold green]\nClient IP: [cyan]{data['origin']}[/cyan]", title="uv run --with Demo"))
