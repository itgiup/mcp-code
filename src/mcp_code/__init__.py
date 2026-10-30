import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Thư mục được phép đọc, đặt qua biến môi trường MCP_CODE_ROOT
ROOT = Path(os.environ.get("MCP_CODE_ROOT", ".")).expanduser().resolve()
SKIP = {".git", "node_modules", "__pycache__", ".venv"}
BLOCKED = {".env", "id_rsa", "id_ed25519"}

mcp = FastMCP("mcp-code")

def safe(p: str) -> Path:
    path = (ROOT / p).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Đường dẫn nằm ngoài thư mục cho phép")
    if path.name in BLOCKED:
        raise ValueError("File bị chặn")
    return path


@mcp.tool()
def list_dir(path: str = ".") -> list[str]:
    """Liệt kê file/thư mục."""
    return sorted(
        f"{'[d] ' if c.is_dir() else ''}{c.name}"
        for c in safe(path).iterdir()
        if c.name not in SKIP
    )


@mcp.tool()
def read_file(path: str, max_bytes: int = 200_000) -> str:
    """Đọc nội dung một file text."""
    return safe(path).read_text(encoding="utf-8", errors="replace")[:max_bytes]


@mcp.tool()
def search_code(query: str, path: str = ".", max_results: int = 50) -> list[str]:
    """Tìm chuỗi trong code, trả về 'file:dòng: nội dung'."""
    out = []
    for f in safe(path).rglob("*"):
        if not f.is_file() or SKIP & set(f.parts) or f.name in BLOCKED:
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if query in line:
                    out.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()}")
                    if len(out) >= max_results:
                        return out
        except (UnicodeDecodeError, OSError):
            pass
    return out


def main() -> None:
    mcp.run(transport="stdio")

