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

redis-users:
	heroku redis:cli REDIS_URL --app metropolia-it-sales --confirm metropolia-it-sales

redis-objects:
	heroku redis:cli HEROKU_REDIS_MAUVE_URL --app metropolia-it-sales --confirm metropolia-it-sales

watch:
	watchmedo shell-command \
	    --patterns="*.py" \
	    --recursive \
	    --command='./bot.py' \
	    .
