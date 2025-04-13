.PHONY: install run clean setup help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Directories
SRC_DIR := src
REPORTS_DIR := reports
DATA_DIR := $(SRC_DIR)/data
DELIVERY_DATA_DIR := $(DATA_DIR)/delivery_sales
SUBSCRIPTION_DATA_DIR := $(DATA_DIR)/subscription_sales
WEEKLY_DATA_DIR := $(DATA_DIR)/weekly_sales

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo
	@echo 'Targets:'
	@awk '/^[a-zA-Z0-9_-]+:.*?## .*$$/ {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install required Python packages
	$(PIP) install -r requirements.txt

setup: ## Create necessary directories
	mkdir -p $(REPORTS_DIR)
	mkdir -p $(DELIVERY_DATA_DIR)
	mkdir -p $(SUBSCRIPTION_DATA_DIR)
	mkdir -p $(WEEKLY_DATA_DIR)
	mkdir -p assets/images/logos
	mkdir -p assets/icons/currency
	mkdir -p assets/fonts

run: ## Generate sales report
	$(PYTHON) $(SRC_DIR)/sales_report.py

clean: ## Remove generated reports and cache files
	rm -f $(REPORTS_DIR)/*.pdf
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

check-data: ## Check if required data files exist
	@echo "Checking data files..."
	@if [ -d "$(DELIVERY_DATA_DIR)" ] && [ -d "$(SUBSCRIPTION_DATA_DIR)" ] && [ -d "$(WEEKLY_DATA_DIR)" ]; then \
		echo "✓ Data directories exist"; \
	else \
		echo "✗ Data directories missing"; \
		exit 1; \
	fi

lint: ## Run linting checks
	$(PYTHON) -m pylint $(SRC_DIR)/*.py

test: ## Run tests (when implemented)
	$(PYTHON) -m pytest tests/

dev-setup: install setup ## Complete development setup
	@echo "Development environment setup complete"

report: check-data run ## Check data and generate report
	@echo "Report generation complete"

# Weekly Report
w-report: check-data ## Generate weekly sales report
	@echo "Generating weekly sales report..."
	@cd src && $(PYTHON) weekly_report.py
	@echo "Weekly report generation complete!" 