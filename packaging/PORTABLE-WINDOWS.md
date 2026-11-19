# Tick Stock Panel — Windows 免安装预览版

1. 将 ZIP 完整解压到可写目录，例如 D:\TSP。不要在压缩包里直接运行。
2. 双击 TSP.exe。必须保留同目录的 _internal 和 TSP.exe.config。
3. 首次在「设置 → 数据源」填写自己的 API Key，并按需获取历史数据。
4. 自动刷新频率可在设置中调整；本包不携带 Mac 上的 Key、自选或行情文件。

支持 Windows 10/11 x64；不需要安装 Python、Node.js、pnpm 或本程序安装器。
桌面窗口依赖 Microsoft Edge WebView2 Runtime 和 .NET Framework 4.8。
Windows 11 通常已具备；缺失的 Windows 10 需从 Microsoft 官方补装系统运行库。
这是未签名预览版，不修改系统的安全保护设置。

数据与配置自动保存到 TSP.exe 旁边的 data 目录；移动或备份时复制整个 TSP 目录。
升级时先退出程序，保留原 data 目录，用新版程序文件覆盖；不要删除 data。
退出应用窗口即退出本程序。启动故障可查看 data\logs\desktop.log。
行情与首次数据下载需要联网；无 API 权限的数据不会因封装而解锁。
纯 Polars 回测可用，本包不含可选 vectorbt 回测链。

核对 build-info.json 可查看构建版本和 Git 提交；ZIP 旁的 .sha256 可用于校验下载完整性。
