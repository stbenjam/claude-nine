# Makefile for Claude Code Marketplace

# Container runtime (podman or docker)
CONTAINER_RUNTIME ?= $(shell command -v podman 2>/dev/null || echo docker)

# claudelint image
CLAUDELINT_IMAGE = ghcr.io/stbenjam/claudelint:main

# Template repository
TEMPLATE_REPO := https://raw.githubusercontent.com/stbenjam/claude-marketplace-template/main

.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Run plugin linter (verbose, strict mode)
	@echo "Running claudelint with $(CONTAINER_RUNTIME)..."
	$(CONTAINER_RUNTIME) run --rm -v $(PWD):/workspace:Z ghcr.io/stbenjam/claudelint:main -v --strict

.PHONY: lint-pull
lint-pull: ## Pull the latest claudelint image
	@echo "Pulling latest claudelint image..."
	$(CONTAINER_RUNTIME) pull $(CLAUDELINT_IMAGE)

.PHONY: update
update: ## Update plugin documentation and website data
	@echo "Updating plugin documentation..."
	@python3 scripts/generate_plugin_docs.py
	@echo "Building website data..."
	@python3 scripts/build-website.py

.PHONY: update-from-template
update-from-template: ## Update core files from template repository
	@echo "Fetching latest template files..."
	@curl -fsSL $(TEMPLATE_REPO)/docs/index.html -o docs/index.html.new
	@curl -fsSL $(TEMPLATE_REPO)/scripts/build-website.py -o scripts/build-website.py
	@curl -fsSL $(TEMPLATE_REPO)/scripts/generate_plugin_docs.py -o scripts/generate_plugin_docs.py
	@curl -fsSL $(TEMPLATE_REPO)/scripts/apply-branding.py -o scripts/apply-branding.py
	@echo "Applying customizations..."
	@python3 scripts/apply-branding.py
	@mv docs/index.html.new docs/index.html
	@echo "✓ Updated to latest template version"

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
