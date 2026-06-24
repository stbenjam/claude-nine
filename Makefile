# Makefile for Claude Code Marketplace

SKILLSAW_VERSION := 0.14.1

.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint plugins and skills with skillsaw (strict mode)
	uvx skillsaw==$(SKILLSAW_VERSION) --strict

.PHONY: lint-fix
lint-fix: ## Apply skillsaw autofixes
	uvx skillsaw==$(SKILLSAW_VERSION) fix

.PHONY: new-plugin
new-plugin: ## Create a new plugin (usage: make new-plugin NAME=my-plugin)
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME is required. Usage: make new-plugin NAME=my-plugin"; \
		exit 1; \
	fi
	@echo "Creating new plugin: $(NAME)..."
	@mkdir -p plugins/$(NAME)/{.claude-plugin,commands,skills}
	@echo '{\n  "name": "$(NAME)",\n  "description": "TODO: Add description",\n  "version": "0.0.1",\n  "author": {\n    "name": "TODO: Add author"\n  }\n}' > plugins/$(NAME)/.claude-plugin/plugin.json
	@echo '---\ndescription: Example command\n---\n\n## Name\n$(NAME):example\n\n## Synopsis\n```\n/$(NAME):example\n```\n\n## Description\nTODO: Add description\n\n## Implementation\n1. TODO: Add implementation steps\n\n## Return Value\nTODO: Describe output' > plugins/$(NAME)/commands/example.md
	@echo "# $(NAME)\n\nTODO: Add plugin description" > plugins/$(NAME)/README.md
	@echo "Adding plugin to marketplace.json..."
	@python3 -c "import json; \
		f = open('.claude-plugin/marketplace.json', 'r'); \
		data = json.load(f); \
		f.close(); \
		data['plugins'].append({'name': '$(NAME)', 'source': './plugins/$(NAME)', 'description': 'TODO: Add description'}); \
		f = open('.claude-plugin/marketplace.json', 'w'); \
		json.dump(data, f, indent=2); \
		f.close()"
	@echo "✓ Created plugin: $(NAME)"
	@echo "✓ Added to marketplace.json"

.DEFAULT_GOAL := help
