tox -e clean && tox -e build && (tox -e lint || tox -e lint) && (tox || tox)
