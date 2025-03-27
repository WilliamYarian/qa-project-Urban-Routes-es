import time

from selenium import webdriver

import data
import methods
from data import urban_routes_url, address_from, address_to, phone_number, card_number, card_code, card_expire
from methods import UrbanRoutesPage
import phone_code_retrieval

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(urban_routes_url)
        routes_page = methods.UrbanRoutesPage(self.driver)
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

    def test_input_code(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        code = phone_code_retrieval.retrieve_phone_code(self.driver)
        assert code is not None, "No confirmation code was retrieved."
        routes_page.set_code(code)

    def test_add_payment(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.select_add_payment()


    def test_write_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_driver_message()
        entered_message = routes_page.get_driver_message()
        assert entered_message == data.message_for_driver, "The entered message does not match the expected message."

    def test_blanket_slider(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.order_blanket_and_tissues()

    def test_add_ice_cream(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream()

    def test_search_for_taxi(self):
        routes_page = methods.UrbanRoutesPage(self.driver)
        routes_page.search_taxi()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()