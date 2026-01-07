# cc-10113-reproducer

Reproducer for [claude-code#10113](https://github.com/anthropics/claude-code/issues/10113) - Skills incorrectly resolved for git-installed marketplace plugins.

## The Bug

When a plugin is installed from a git-based marketplace (local or remote), skills are resolved to the marketplace cache directory (`~/.claude/plugins/marketplaces/`) instead of the actual git repository location. This causes "no such file or directory" errors when skills reference files in their own directory.

## Steps to Reproduce

1. Add this marketplace from the local git repository:
   ```
   /plugin marketplace add /path/to/claude-nine
   ```

2. Install this plugin:
   ```
   /plugin install cc-10113-reproducer@claude-nine
   ```

3. Invoke the skill:
   ```
   /cc-10113-reproducer:run-check
   ```

## Expected Behavior

The skill should execute `check.sh` from:
```
/path/to/claude-nine/plugins/cc-10113-reproducer/skills/run-check/check.sh
```

And output:
```
SUCCESS: Skill script executed correctly!
```

## Actual Behavior (Bug)

Claude tries to execute the script from:
```
~/.claude/plugins/marketplaces/claude-nine/skills/check.sh
```

Which results in:
```
no such file or directory
```
