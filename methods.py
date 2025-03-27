from faulthandler import is_enabled
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from selenium.webdriver.common.by import By
import data
from selenium.webdriver.common.keys import Keys


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    flash_button = (By.CSS_SELECTOR, '.mode.active')
    order_taxi = (By.CSS_SELECTOR, 'button.button.round')
    comfort_button = (By.XPATH, "//*[contains(text(),'Comfort')]")
    phone_pop_up = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    code_input = (By.ID, 'code')
    confirm_button = (By.XPATH, '//*[contains(text(), "Confirmar")]')
    add_payment = (By.CLASS_NAME, 'pp-button')
    add_card = (By.CLASS_NAME, 'pp-plus')
    card_field = (By.ID, 'number')
    card_cvv = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    add_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    added_card = (By.CLASS_NAME, 'pp-row')
    close_payments_button = (By.CSS_SELECTOR, '.payment-picker.open .modal .section.active .close-button')
    message_field = (By.ID, 'comment')
    requirements_of_order = (By.CLASS_NAME, 'reqs-head')
    blanket_slider = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[@class='slider round']")
    ice_cream_plus_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    ice_cream_counter = By.XPATH, "//div[text()='Helado']/following-sibling::div//div[@class='counter-value']"
    taxi_search_button = (By.CLASS_NAME, 'smart-button-wrapper')
    taxi_details = (By.CLASS_NAME, 'order-header')
    taxi_confirmed = (By.XPATH, '//div[@class="order-number"]')



    def __init__(self, driver):
        self.driver = driver

        driver.implicitly_wait(3)

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def set_flash(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.flash_button))
        self.driver.find_element(*self.flash_button).click()

    def taxi_order(self):
        self.driver.find_element(*self.order_taxi).click()

    def set_comfort(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.comfort_button))
        self.driver.find_element(*self.comfort_button).click()

    def is_comfort_tariff_selected(self):
        try:
            self.driver.find_element(*self.comfort_button)
            return True
        except:
            return False

    def open_pop_up(self):
        WebDriverWait(self.driver, 15).until(expected_conditions.element_to_be_clickable(self.phone_pop_up)).click()

    def set_phone_number(self):
        phone_input = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.phone_input))
        phone_input.clear()
        phone_input.send_keys(data.phone_number)
        self.driver.find_element(*self.next_button).click()

    def get_phone_number(self):
        return self.driver.find_element(self.phone_input).get_property('value')

    def validate_phone_number(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.phone_input))
        displayed_number = self.driver.find_element(*self.phone_input).text
        assert displayed_number == data.phone_number

    def set_code(self, code):
        code_input = self.driver.find_element(*self.code_input)  # Adjust the locator as necessary
        code_input.send_keys(code)
        self.driver.find_element(*self.confirm_button).click()

    def get_confirmation_code(self):
        return self.driver.find_element(self.code_input).get_property('value')

    def select_add_payment(self):
        self.driver.find_element(*self.add_payment).click()
        self.driver.find_element(*self.add_card).click()
        card_field = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.card_field))
        card_field.click()
        card_field.send_keys(data.card_number)
        card_field.send_keys(Keys.TAB)
        card_cvv = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.card_cvv))
        card_cvv.click()
        time.sleep(0.5)
        card_cvv.send_keys(data.card_code)
        card_cvv.send_keys(Keys.TAB)
        self.driver.find_element(*self.add_button).click()
        self.driver.find_element(*self.close_payments_button).click()

    def assert_card_number(self, expected_card_number):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.added_card))
        actual_card_number = self.driver.find_element(*self.added_card).text
        assert actual_card_number == expected_card_number

    def set_driver_message(self):
        message_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.message_field))
        self.driver.execute_script("arguments[0].scrollIntoView();", message_field)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, "locator_of_interfering_element")))
        time.sleep(0.1)  # Let any animations complete
        # Click using JavaScript instead
        self.driver.execute_script("arguments[0].click();", message_field)
        message_field.send_keys(data.message_for_driver)

    def get_driver_message(self):
        return self.driver.find_element(*self.message_field).get_attribute('value')

    def assert_driver_message(self, expected_driver_message):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.get_driver_message()))
        actual_driver_message = self.driver.find_element(*self.get_driver_message()).text
        assert actual_driver_message == expected_driver_message

    def order_blanket_and_tissues(self):
        blanket_slider = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.blanket_slider))
        self.driver.execute_script("arguments[0].scrollIntoView();", blanket_slider)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.blanket_slider)).click()

    def assert_blanket_and_tissues (self):
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.blanket_slider))
            slider_selected = self.driver.find_element(*self.blanket_slider).text
            assert slider_selected == is_enabled()

    def add_ice_cream(self):
        ice_cream_selector = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.ice_cream_plus_button))
        self.driver.execute_script("arguments[0].scrollIntoView();", ice_cream_selector)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)).click()
        ice_cream_selector.click()

    def search_taxi(self):
        self.driver.find_element(*self.taxi_search_button).click()
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.taxi_details))
        WebDriverWait(self.driver, 60).until(expected_conditions.visibility_of_element_located(self.taxi_confirmed))


















