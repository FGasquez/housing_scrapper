build:
	docker build . -t pgiu/housing_scraper:latest

push: build
	docker push pgiu/housing_scraper:latest