# Makefile for Claude Code and Codex plugins

SKILLSAW_VERSION := 0.17.0
CODEX_MARKETPLACE := .agents/plugins/marketplace.json

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

.PHONY: docs
docs: ## Generate plugin/skill documentation to docs/index.html
	uvx skillsaw==$(SKILLSAW_VERSION) docs --format html -o docs/index.html --title "stbenjam's skills"

.PHONY: plugin-table
plugin-table: ## Generate the README plugin table from the marketplace catalogs
	@python3 scripts/generate_plugin_table.py

.PHONY: sync-skills
sync-skills: ## Refresh root skills/ symlinks from plugin skills
	@python3 scripts/sync_skills.py

.PHONY: update
update: ## Regenerate documentation, the README plugin table, and root skill symlinks
	@$(MAKE) docs
	@$(MAKE) plugin-table
	@$(MAKE) sync-skills

.PHONY: new-plugin
new-plugin: ## Create a new plugin (usage: make new-plugin NAME=my-plugin)
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME is required. Usage: make new-plugin NAME=my-plugin"; \
		exit 1; \
	fi
	@echo "Creating new plugin: $(NAME)..."
	@mkdir -p plugins/$(NAME)/{.claude-plugin,.codex-plugin,skills/$(NAME)}
	@python3 -c "import json; from pathlib import Path; name='$(NAME)'; description='Reusable $(NAME) workflows.'; root=Path('plugins')/name; claude={'name': name, 'description': description, 'version': '0.1.0', 'author': {'name': 'stbenjam'}}; codex={'name': name, 'version': '0.1.0', 'description': description, 'author': {'name': 'stbenjam'}, 'skills': './skills/', 'interface': {'displayName': name.replace('-', ' ').title(), 'shortDescription': description, 'longDescription': description, 'developerName': 'stbenjam', 'category': 'Productivity', 'capabilities': [], 'defaultPrompt': 'Help me use this plugin.'}}; (root/'.claude-plugin/plugin.json').write_text(json.dumps(claude, indent=2)+'\\n'); (root/'.codex-plugin/plugin.json').write_text(json.dumps(codex, indent=2)+'\\n')"
	@printf '%s\n' '---' 'name: $(NAME)' 'description: Reusable $(NAME) workflows.' '---' '' '# $(NAME)' '' 'Follow the workflow for this plugin.' > plugins/$(NAME)/skills/$(NAME)/SKILL.md
	@printf '%s\n' '# $(NAME)' '' 'Reusable Claude Code and Codex workflows.' > plugins/$(NAME)/README.md
	@echo "Adding $(NAME) to both marketplace catalogs..."
	@python3 -c "import json; from pathlib import Path; name='$(NAME)'; description='Reusable $(NAME) workflows.'; claude_path=Path('.claude-plugin/marketplace.json'); claude=json.loads(claude_path.read_text()); claude['plugins'].append({'name': name, 'source': './plugins/'+name, 'description': description}); claude_path.write_text(json.dumps(claude, indent=2)+'\\n'); codex_path=Path('$(CODEX_MARKETPLACE)'); codex=json.loads(codex_path.read_text()); codex['plugins'].append({'name': name, 'source': {'source': 'local', 'path': './plugins/'+name}, 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}); codex_path.write_text(json.dumps(codex, indent=2)+'\\n')"
	@$(MAKE) update
	@echo "✓ Created plugin: $(NAME)"
	@echo "✓ Added to Claude and Codex marketplace catalogs"

.DEFAULT_GOAL := help
