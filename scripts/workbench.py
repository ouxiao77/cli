#!/usr/bin/env python3
"""Repository scaffold utilities only. Never read or analyze patient records."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_CONFIG = ROOT / "config/project.local.json"
EXAMPLE_CONFIG = ROOT / "config/project.example.json"
LOCAL_DIRS = (
    "data/raw", "data/interim", "data/processed",
    "outputs/qc", "outputs/tables", "outputs/figures",
    "outputs/reports", "outputs/logs",
    "manuscript/drafts/zh", "manuscript/drafts/en",
    "manuscript/exports", "references/fulltext",
)
REQUIRED_FILES = (
    "README.md", ".gitignore", "docs/INVENTORY.md", "docs/PROTOCOL.md",
    "docs/TASKS.md", "docs/ROLLBACK.md", "config/project.example.json",
    "templates/data_dictionary.csv", "templates/decisions.csv",
    "templates/results_manifest.csv", "scripts/R/README.md",
    "data/README.md", "outputs/README.md", "manuscript/README.md",
    "references/README.md", "scripts/workbench.py",
)


def initialize():
    for relative in LOCAL_DIRS:
        (ROOT / relative).mkdir(parents=True, exist_ok=True)
    # Exclusive creation preserves any existing local configuration byte-for-byte.
    try:
        with LOCAL_CONFIG.open("x", encoding="utf-8") as target:
            target.write(EXAMPLE_CONFIG.read_text(encoding="utf-8"))
        print("已创建本地配置：config/project.local.json")
    except FileExistsError:
        print("已保留已有本地配置：config/project.local.json")
    print("本地工作目录已就绪；未读取数据，未运行清洗、分组或统计分析。")
    return 0


def check():
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    if missing:
        print("骨架文件缺失：" + ", ".join(missing), file=sys.stderr)
        return 1
    if not LOCAL_CONFIG.is_file():
        print("尚未初始化。请运行：python3 scripts/workbench.py init", file=sys.stderr)
        return 1
    try:
        config = json.loads(LOCAL_CONFIG.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        print("配置不是有效的 UTF-8 JSON：" + str(error), file=sys.stderr)
        return 1
    if not isinstance(config, dict):
        print("配置顶层必须是 JSON 对象。", file=sys.stderr)
        return 1
    required = set(json.loads(EXAMPLE_CONFIG.read_text(encoding="utf-8")))
    if required - config.keys():
        print("配置缺少字段：" + ", ".join(sorted(required - config.keys())), file=sys.stderr)
        return 1
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        print("仅支持 schema_version=1。", file=sys.stderr)
        return 1
    if config["mode"] != "scaffold":
        print("当前只支持 scaffold 模式；分析模块尚未实现。", file=sys.stderr)
        return 1
    if not isinstance(config["source_sheet"], str) or not config["source_sheet"].strip():
        print("source_sheet 必须为非空文本。", file=sys.stderr)
        return 1
    if config["id_column"] is not None and (
        not isinstance(config["id_column"], str) or not config["id_column"].strip()
    ):
        print("id_column 应为空值或已核实的非空列名。", file=sys.stderr)
        return 1
    if config["al_months"] != [0, 6, 12]:
        print("本骨架约定眼轴时间为 [0, 6, 12]，变更前请更新研究约定。", file=sys.stderr)
        return 1
    for field in ("main_optical_zones_mm", "extension_optical_zones_mm"):
        value = config[field]
        if not isinstance(value, list) or not value or any(
            type(item) not in (int, float) or item not in (5.0, 5.5, 6.0) for item in value
        ) or len(set(value)) != len(value):
            print(field + " 必须为不重复的可用光学区列表。", file=sys.stderr)
            return 1
    if set(config["main_optical_zones_mm"]) & set(config["extension_optical_zones_mm"]):
        print("主分析与拓展光学区不能重叠。", file=sys.stderr)
        return 1
    if type(config["udva_pass_decimal"]) not in (int, float) or config["udva_pass_decimal"] != 0.8:
        print("本骨架 UDVA 小数视力达标阈值为 0.8。", file=sys.stderr)
        return 1
    n = config["expected_cohort_n"]
    if n is not None and (type(n) is not int or n <= 0):
        print("expected_cohort_n 应为空值或正整数，仅用于对账。", file=sys.stderr)
        return 1
    input_file = config["input_file"]
    if input_file is not None:
        if not isinstance(input_file, str) or not input_file.strip():
            print("input_file 应为 null 或 data/raw 下的相对文件路径。", file=sys.stderr)
            return 1
        path = Path(input_file)
        resolved = (ROOT / path).resolve()
        if path.is_absolute() or ROOT / "data/raw" not in resolved.parents:
            print("输入路径必须指向本仓库 data/raw 内的文件，不能越界。", file=sys.stderr)
            return 1
        if not resolved.is_file():
            print("配置指向的源文件不存在；请核对本地路径。", file=sys.stderr)
            return 1
        print("已找到配置指向的本地源文件；未读取或验证工作簿内容。")
    else:
        print("骨架及配置检查通过；尚未配置数据。")
    print("本阶段只检查文件与配置；清洗、分组、统计、图表和论文生成均待实施。")
    return 0


def main():
    parser = argparse.ArgumentParser(description="科研工作台骨架：初始化/检查，不执行研究分析")
    parser.add_argument("command", choices=("init", "check"))
    args = parser.parse_args()
    try:
        return initialize() if args.command == "init" else check()
    except OSError as error:
        print("文件操作未完成：" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
