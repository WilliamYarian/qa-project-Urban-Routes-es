from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import methods
from data import urban_routes_url, address_from, address_to, phone_number, card_number, card_code, card_expire, message_for_driver


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        cls.driver = webdriver.Chrome(
            service=Service(r'C:\Users\willi\Documents\Tripleten\Sprint 8\Selenium\WebDriverbin\chromedriver.exe'),
            options=options)

    def test_set_route(self):
        self.driver.get(urban_routes_url)
        routes_page = methods.UrbanRoutesPage(self.driver)
        #address_from = address_from
        #address_to = address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_flash(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.set_flash()

    def test_taxi_order(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.taxi_order()

    def test_select_comfort(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.set_comfort()

    def test_phone_pop_up(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.open_pop_up()

    def test_input_number(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.set_phone_number()
        routes_page.set_code()
















    #@classmethod
    #def teardown_class(cls):
        #cls.driver.quit()
