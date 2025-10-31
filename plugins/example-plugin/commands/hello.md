---
description: Say hello to someone
argument-hint: [name]
---

## Name
example-plugin:hello

## Synopsis
```
/example-plugin:hello [name]
```

## Description
The `example-plugin:hello` command greets the specified person by name. If no name is provided, it greets "World".

This is a simple example demonstrating the basic structure of a Claude Code plugin command.

## Implementation

1. **Parse Arguments**: Extract the name from the command arguments
   - If no name is provided, default to "World"

2. **Generate Greeting**: Create a friendly greeting message
   - Format: "Hello, {name}!"

3. **Return Response**: Output the greeting to the user

## Return Value

- **Format**: Text greeting
- **Example**: "Hello, Alice!"

## Examples

1. **Greet a specific person**:
   ```
   /example-plugin:hello Alice
   ```
   Output: "Hello, Alice!"

2. **Default greeting**:
   ```
   /example-plugin:hello
   ```
   Output: "Hello, World!"

## Arguments

- `$1`: (Optional) The name of the person to greet. Defaults to "World" if not provided.
