.PHONY: lint
lint:
	${INVENV} ruff check ${flags} .

.PHONY: lint-fix
lint-fix:
	${INVENV} ruff check ${flags} . --fix

.PHONY: fmt
fmt:
	${INVENV} ruff format .

