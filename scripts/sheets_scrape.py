import pygsheets
from os import path
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from time import sleep
from os import path, getcwd
from pprint import pprint
import pickle

from src.database import init_db, get_session, Muscle, Day, Exercise, drop_tables

# google sheets
key_path = path.join(path.dirname(__file__), "google_key.json")
gs_client = pygsheets.authorize(service_account_file=key_path)
# print(gs_client.spreadsheet_titles())
sets_sheet = gs_client.open("SetsApp")
ex_wksheet = sets_sheet.worksheet_by_title("Exercises")

# database
exercises_df = ex_wksheet.get_as_df()
init_db()
db_session = get_session()

ex_names = set()
ex_data = []


class BodyBuidlingSpider(scrapy.Spider):
	name = "BodyBuidling"
	start_urls = ["https://www.bodybuilding.com/exercises/"]

	def __init__(self):
		executable_path = path.join(path.dirname(__file__), "geckodriver.exe")
		# capabilities = DesiredCapabilities().FIREFOX
		# capabilities["marionette"] = False
		options = webdriver.FirefoxOptions()
		options.headless = True
		# options.binary = r"C:\Users\jacob\AppData\Local\Mozilla Firefox\firefox.exe"
		options.binary = r"C:\Program Files\Mozilla Firefox\firefox.exe"
		self.driver = webdriver.Firefox(
			executable_path=executable_path,
			# capabilities=capabilities,
			options=options,
			# firefox_binary=ff_binary,
		)
		# self.driver.install_addon(path.join(path.dirname(__file__), "adblock_plus-3.7-an+fx.xpi"))
		super(BodyBuidlingSpider, self).__init__()

	def parse(self, response):
		muscle_url_elements = response.xpath(
				"/html/body/div[3]/main/div[2]/div/div[1]/section"
		)
		muscle_urls = muscle_url_elements.css("a::attr(href)").getall()
		for url in muscle_urls:
			yield response.follow(url, self.parse_exercise)

	def parse_exercise(self, response):
		# print(f"Selenium to page {response.url}")
		self.driver.get(response.url)
		self.driver.implicitly_wait(3)
		load_more_btn = self.driver.find_element_by_class_name("ExLoadMore-btn")
		if load_more_btn:
			load_more_btn.click()
			self.driver.implicitly_wait(3)
		exercises = self.driver.find_elements_by_class_name("ExResult-row")
		for ex in exercises:
			ex_name = ex.find_element_by_class_name(
				"ExResult-resultsHeading"
			).find_element_by_tag_name("a").text
			ex_url = ex.find_element_by_class_name(
				"ExResult-resultsHeading"
			).find_element_by_tag_name("a").get_attribute("href")
			ex_muscle = ex.find_element_by_class_name(
				"ExResult-muscleTargeted"
			).find_element_by_tag_name("a").text
			# pprint(["test:", name, url, muscle])
			if ex_name:
				if ex_name not in ex_names:
					ex_data.append({
						"name": ex_name,
						"muscle": ex_muscle,
					})
				ex_names.add(ex_name)

		# sleep(3)

	def __del__(self):
		self.driver.close()
		pprint(ex_data)
		with open("ex_data.p", "wb") as pickle_file:
			pickle.dump(ex_data, pickle_file)
		# print("COMPLETE!")


def start_scrape():
	process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})

	process.crawl(BodyBuidlingSpider)
	process.start()  # the script will block here until the crawling is finished


def load_pickled_data():
	drop_tables()
	init_db()
	db_session = get_session()
	with open("ex_data.p", "rb") as muscle_pickle:
		exercises = pickle.load(muscle_pickle)
	pprint(exercises)
	day_1_db = Day(desc="Day 1")
	day_2_db = Day(desc="Day 2")
	day_3_db = Day(desc="Day 3")
	day_4_db = Day(desc="Day 4")
	db_session.add_all([day_1_db, day_2_db, day_3_db, day_4_db])
	db_session.flush()

	day_muscle_map = [
		[
			[
				'Abdominals',
				'Lower Back',
				'Middle Back',
				'Quadriceps'
			], day_1_db
		],
		[
			[
				'Glutes',
				'Calves',
				'Triceps'
			], day_2_db
		],
		[
			[
				'Biceps',
				'Forearms',
				'Traps',
				'Shoulders'
			], day_3_db
		],
		[
			[
				'Lats',
				'Chest',
				'Hamstrings'
			], day_4_db
		]
	]
	# Muscle, Day, Exercise
	db_muscles = {}
	for ex in exercises:
		muscle = ex["muscle"]
		ex_name = ex["name"]
		db_day = next((day for muscles, day in day_muscle_map if muscle in muscles))
		if muscle not in db_muscles.keys():
			db_muscle = Muscle(
				name=muscle,
				day_id=db_day.id
			)
			db_muscles[muscle] = db_muscle
			db_session.add(db_muscle)
		else:
			db_muscle = db_muscles[muscle]
		db_exercise = Exercise(
			name=ex_name,
			muscle=db_muscle
		)
		db_session.add(db_exercise)
	db_session.commit()


if __name__ == '__main__':
	# start_scrape()
	load_pickled_data()
