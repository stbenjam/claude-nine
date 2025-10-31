---
name: Example Agent
description: Demonstrates autonomous agent for complex workflows
subagent_type: example-agent
---

# Example Agent

An autonomous agent that handles multi-step workflows independently.

## Purpose

This agent is designed to:
- Execute complex sequences of operations
- Make decisions based on intermediate results
- Handle errors and retry logic automatically

## When to Use

Invoke this agent when you need to:
- Perform exploratory tasks
- Execute workflows with multiple decision points
- Handle tasks that require adaptive behavior

## Capabilities

The agent has access to:
- File system operations
- Search and analysis tools
- External API calls

## Usage

```
Use the Task tool to launch this agent:
- subagent_type: "example-agent"
- prompt: Detailed task description
```

## Implementation Details

The agent will:
1. Analyze the task requirements
2. Create an execution plan
3. Execute steps sequentially
4. Handle errors gracefully
5. Return a comprehensive report

## Examples

### Example 1: Analysis Task
```
subagent_type: "example-agent"
prompt: "Analyze the project structure and identify optimization opportunities"
```

### Example 2: Automation Task
```
subagent_type: "example-agent"
prompt: "Refactor all components to use new API pattern"
```

## Best Practices

- Provide clear, specific task descriptions
- Set appropriate scope boundaries
- Review agent output before applying changes
