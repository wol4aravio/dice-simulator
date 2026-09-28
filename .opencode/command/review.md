---
description: Ask the read-only reviewer subagent to review the current diff against main
agent: build
---
Delegate to the `reviewer` subagent: review `git diff main...HEAD` (or the working tree if there are
uncommitted changes) and return its findings verbatim. Then, for every blocker or major finding,
propose a concrete fix but do not apply it until asked. $ARGUMENTS
