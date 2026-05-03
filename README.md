# GitHub Agent - IQ 300 Re-architecture

**Current Version: 1.0.0-alpha**

This agent has been refactored according to the "IQ 300 Logic Blueprint" for enhanced intelligence and maintainability.

## Interaction Model

**New Command Interface:** All commands for this agent are now issued via **GitHub Discussions**, leveraging natural language processing. Please refer to the Discussions section of this repository to interact with the agent.

**Instruction Parsing Core:** This `README.md` serves as the core for all instruction parsing. The agent will reference this document for its operational logic and interaction protocols.

## State Management

**System Variables (Step 7 Implemented):** Agent state is no longer stored in local `.txt` files. All critical system variables are now managed via **GitHub Repository Variables** for improved security, consistency, and hot-reloading capabilities.

## Evolution Progress Blueprint

The following blueprint guides the agent's development and operational logic:

| 步驟 | 動作名稱 | 角色扮演 | 智商 300 的邏輯 (本質化) |
|---|---|---|---|
| 3 | 自然語言環境介面 | 棄用 Bash 或 Python 腳本，改用 「Markdown 作為編譯指令」。 | |
| 4 | 利用「討論 (Discussions)」思維場 | 所有的指令不發在 Issue，而是發在 Discussions。 | |
| 5 | AI 自我修改 (Hot-Reload) | 進化：Agent 第一個動作是根據你的需求，「重寫自己的 Actions 腳本」。 | |
| 6 | 分支即「平行時空」 | 並行處理不同的指令在不同的 Branch 執行，最後只保留最優結果合併。 | |
| 7 | 利用「環境變量」做緩存 | 神經突觸：所有的狀態不存硬碟，存入 Repo 的 Variables 系統。 | |
| 8 | 語義化觸發 (Linguistic Trigger) | 潛意識：只要你在 Discussions 裡達成某種語義共識，Actions 自動感知。 | |
| 9 | 自動化「成果鏡像」 | 表象：執行成果自動生成為一個 GitHub Page 網頁。 | |
| 10 | 邏輯歸位 (Recursive) | 睡眠：任務結束後，Agent 將所有的邏輯壓縮回 README，等待下次呼喚。 | |

## GitHub Pages Mirror (Step 9 Implemented)

An automated GitHub Pages mirror is available [here](https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME/) (link to be configured in repository settings) to display the current evolution progress and operational status. This mirror is automatically updated upon relevant changes.
