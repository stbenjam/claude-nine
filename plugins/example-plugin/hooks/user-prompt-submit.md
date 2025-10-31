---
event: user-prompt-submit
description: Example hook that runs before user prompts are submitted
---

# User Prompt Submit Hook

This hook runs before a user's prompt is submitted to Claude, allowing you to modify or validate the input.

## Implementation

When this hook is triggered:

1. **Validate Input**: Check if the user's input meets certain criteria
2. **Transform**: Optionally modify the prompt before submission
3. **Add Context**: Inject additional context or instructions

## Example Use Cases

- Add custom system prompts
- Validate user input
- Inject project-specific context
- Track usage patterns

## Hook Execution

This hook receives the user's prompt and can return a modified version or the original.
