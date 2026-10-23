# 分阶段审阅与回滚

初始 main 提交：`5d2cb5d70696eeb43d6f3d3c1631a3f37b34d19d`。

本次新增内容使用独立分支 `workbench/scaffold-20261023`，保留原有 `.gitkeep`，不合并主分支。

1. 提交 A：`docs: define OK lens workbench structure and workflow`。含使用说明、盘点、研究约定、任务及目录说明。
2. 提交 B：`feat: add non-destructive workspace init and configuration check`。含 Python 入口、JSON 配置示例、空白 CSV 模板。

未合并时：关闭对应 PR 即可不采纳该版本；main 无需恢复。保留分支方便以后参考，也可在确认无需使用时手动删除。

如果以后合并了：在 GitHub 中对已合并 PR 使用 Revert 创建撤销 PR，审阅后合并；如分批以普通提交合并，则先撤销 B、再撤销 A。使用新增撤销提交保留历史，不用强制推送或 reset 覆盖协作者工作。

`init` 只增加本地目录和不存在的本地配置，不改原始数据。要停用骨架，保留本地数据及输出备份后即可停止使用；撤销仓库提交不等于删除本地被忽略的研究文件。
