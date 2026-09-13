#!/usr/bin/env bash
set -e

echo "==> Ruff check"
ruff check .

echo "==> Ruff format check"
ruff format --check --diff .
