# 功能策划案流程归档

现行通用版与简化版流程，核对日期 2026-09-07，依据 `feature-design-document-standard` v1.6。

- [完整可编辑工作流程手册](策划案工作流程_通用版与简化版_v1.0.docx)
- [通用 Word 母版](skills/game-feature-design-docs/assets/general-feature-design-template.docx)
- [简化 Word 母版](skills/game-feature-design-docs/assets/simple-feature-design-template.docx)
- [当前主 Skill 快照](skills/game-feature-design-docs/SKILL.md)与[标准原文](skills/game-feature-design-docs/references/feature-design-document-standard.md)
- 模板库入口：[通用](skills/artifact-template-game-feature-design-general/SKILL.md)、[简化](skills/artifact-template-game-feature-design-simple/SKILL.md)
- 调用示例：[通用最终案](prompts/general.md)、[简化方向评审](prompts/simple-review.md)、[简单最终案](prompts/simple-final.md)
- [来源与 SHA-256 清单](source-manifest.json)

正式说明以 Word 手册为准。这个目录是整理和归档，不会自动覆盖已安装的 Skills，也不代表任何具体功能已经获准实现。主 Skill 快照依赖 `game-studio-orchestrator`、`game-project-control-plane`、适用时的项目 RAG、Documents 和可编辑设计工具；本包不包含这些依赖，不是完整插件安装包。复用时只复制选中的母版到真实项目，按最新项目正式来源填写。

母版发布副本保留规则正文，清除个人编辑元数据，并修正简化母版表头跨页；安装源未改。来源与发布 SHA-256 分别记录。简单母版写作时需补入文档阶段、实现授权、评审稿禁止实现标识和升级清单；两母版均需补全可编辑图 Artifact Register 字段。旧模板提示与 v1.6 阶段规则不一致时，按手册和 v1.6 处理。原项目参考文件未打包。
