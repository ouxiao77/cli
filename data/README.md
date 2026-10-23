# 本地数据

运行 `python3 scripts/workbench.py init` 创建 `raw/`、`interim/`、`processed/`。这些目录默认不提交。

`raw/` 保存经授权的原始副本，只读；`interim/` 存中间结果；`processed/` 存分析就绪宽表/长表及队列标志。当前未提供这些数据，也未生成任何研究结果。源路径和文件校验值记录在本地日志中，不写入公开仓库。
