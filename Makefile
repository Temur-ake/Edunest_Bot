extract:
	 pybabel extract --input-dirs=. -o locales/messages.pot
update:
	pybabel update -d locales -D messages -i locales/messages.pot

compile:
	pybabel compile -d locales -D messages
