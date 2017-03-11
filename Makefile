TOPDIR := $(PWD)

# Running 'make' will by default execute the first rule.
nothing:
	@echo 'Usage: make RULE_NAME_HERE'

remote:
	heroku git:remote --app metropolia-it-sales

deploy:
	git push heroku master

logs:
	heroku logs --app metropolia-it-sales --tail
