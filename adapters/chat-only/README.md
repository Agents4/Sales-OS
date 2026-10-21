# Chat-only tools

For tools with no skill support: custom GPTs, Copilot, Grok, plain chat.

1. Build the portable files: `python3 tools/sos.py build --target portable`. Output is in `dist/portable/`.
2. Paste `dist/portable/system-prompt.md` as the custom instructions (it stays under 8,000 characters).
3. Attach the skill files you need from `dist/portable/skills/` as knowledge, or paste one into a chat when you need it. Each file is self-contained: instructions, references and templates in one document.
4. Work three questions at a time; the tool returns each artifact in one block. Save it yourself.

Limits: no file access, no linting, no connectors. The tool will walk the rubrics by hand and say lint was not run. Keep real customer data out unless the tool is approved for it.
