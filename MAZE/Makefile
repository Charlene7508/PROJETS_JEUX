install:
	pip install -r requirements.txt

install-mlx:
	cd mlx/mlx_CLXV && chmod +x *.sh && make
	pip install mlx/mlx_CLXV/python/dist/mlx-2.2-py3-none-any.whl

run:
	python3 a_maze_ing.py config.txt

run-mlx:
	python3 -m output.mlx_display

debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 . --exclude=venv,mlx_CLXV
	mypy . --exclude 'venv|mlx_CLXV' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=venv,mlx_CLXV
	mypy . --exclude 'venv|mlx_CLXV' --strict

clean:
	find . -path ./venv -prune -o -type d -name "__pycache__" -exec rm -rf {} +
	find . -path ./venv -prune -o -type d -name ".mypy_cache" -exec rm -rf {} +

.PHONY: install install-mlx run run-mlx debug lint lint-strict clean