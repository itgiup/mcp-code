# mcp-code

MCP server chạy trên máy của bạn, cho phép Claude **đọc và tìm kiếm code** trong một thư mục được chỉ định. Server chỉ có quyền **đọc**, không ghi file và không chạy lệnh.

## Tính năng

| Tool | Mô tả |
|---|---|
| `list_dir` | Liệt kê file và thư mục |
| `read_file` | Đọc nội dung một file text |
| `search_code` | Tìm chuỗi trong code, trả về `file:dòng: nội dung` |

Các thư mục `.git`, `node_modules`, `__pycache__`, `.venv` bị bỏ qua. Các file `.env`, `id_rsa`, `id_ed25519` bị chặn không cho đọc.

## Yêu cầu

- [uv](https://docs.astral.sh/uv/)
- Python 3.10 trở lên
- [Claude Desktop](https://claude.ai/download)

## Cài đặt

```bash
git clone https://github.com/itgiup/mcp-code.git
cd mcp-code
uv sync
```

Dự án dùng `mcp` bản 1.x (`mcp[cli]<2`). Bản 2.x đã đổi API (`FastMCP` thành `MCPServer`) nên chưa tương thích.

## Chạy thử

```bash
MCP_CODE_ROOT=/path/to/your/project uv run mcp-code
```

Server dùng giao thức stdio nên sẽ đứng im chờ input, không in gì ra. Đó là bình thường, nhấn `Ctrl+C` để thoát. Nếu có traceback thì là lỗi cài đặt.

Muốn thử các tool qua giao diện web:

```bash
uv run mcp dev src/mcp_code/__init__.py
```

## Cấu hình Claude Desktop

Mở file cấu hình `claude_desktop_config.json` (trong Claude Desktop: **Settings → Developer → Edit Config**) và thêm:

```json
{
  "mcpServers": {
    "mcp-code": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/mcp-code",
        "run",
        "mcp-code"
      ],
      "env": {
        "MCP_CODE_ROOT": "/path/to/your/project"
      }
    }
  }
}
```

Thay các đường dẫn cho đúng máy của bạn:

- `command`: đường dẫn tuyệt đối tới `uv`, lấy bằng `which uv`.
- `--directory`: thư mục chứa project `mcp-code` này. Bắt buộc, vì Claude Desktop không chạy lệnh trong thư mục project.
- `MCP_CODE_ROOT`: thư mục Claude được phép đọc. Nếu bỏ trống, server dùng thư mục làm việc hiện tại của tiến trình, thường không phải thứ bạn muốn.

Nếu file đã có sẵn nội dung khác, chỉ thêm khối `mcpServers` và nhớ dấu phẩy để JSON hợp lệ. Sau đó **thoát hẳn** Claude Desktop rồi mở lại.

Kiểm tra bằng cách mở chat mới và hỏi, ví dụ: "Liệt kê file trong thư mục gốc rồi đọc README.md".

## Bảo mật

- Server chỉ đọc được bên trong `MCP_CODE_ROOT`. Mọi đường dẫn thoát ra ngoài (ví dụ `../`) đều bị từ chối.
- Hãy trỏ `MCP_CODE_ROOT` vào một dự án cụ thể, không trỏ vào cả thư mục home.
- Nội dung các file Claude đọc sẽ được gửi tới Claude, nên đừng trỏ vào thư mục chứa bí mật.
- Muốn chặn thêm file nhạy cảm, thêm tên file vào tập `BLOCKED` trong `src/mcp_code/__init__.py`.

## Xử lý lỗi

| Hiện tượng | Cách xử lý |
|---|---|
| `Failed to spawn process: No such file or directory` | Sai đường dẫn `command`. Dùng đường dẫn tuyệt đối từ `which uv` |
| `No module named 'mcp.server.fastmcp'` | Đang dùng mcp 2.x. Chạy `uv add "mcp[cli]<2"` |
| Server thoát ngay sau khi khởi động | Chạy tay `uv run mcp-code` để xem lỗi. Log của Claude Desktop nằm ở file `mcp-server-mcp-code.log` |
| Có tool nhưng không đọc được file | Kiểm tra `MCP_CODE_ROOT` có đúng và có quyền đọc không |

Khi viết thêm code, không dùng `print()` ra stdout vì stdout dành cho giao thức MCP. Dùng `print(..., file=sys.stderr)` để debug.

## Giấy phép

[MIT](LICENSE)
