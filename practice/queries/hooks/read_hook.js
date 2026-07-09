// PreToolUse hook: chặn Claude dùng tool Read để mở .env.
// Bản hiện hành của khoá CHỈ cover Read (tool Read gửi field `file_path`).
// Grep/Bash có input shape khác -> xem ghi chú "Why Read only" + permissions.deny.
process.stdin.setEncoding("utf8");
let input = "";
process.stdin.on("data", (d) => (input += d));
process.stdin.on("end", () => {
  const toolArgs = JSON.parse(input); // JSON tool call Claude đẩy qua STDIN
  const readPath = toolArgs.tool_input?.file_path || ""; // Read -> tool_input.file_path
  if (readPath.includes(".env")) {
    console.error("You cannot read the .env file"); // stderr = message Claude nhận
    process.exit(2); // exit 2 = CHẶN tool call (chỉ có tác dụng ở PreToolUse)
  }
  process.exit(0); // exit 0 = cho phép tool call chạy tiếp
});
