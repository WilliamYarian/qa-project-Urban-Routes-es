from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from selenium.webdriver.common.by import By
import data

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
        comfort_button = (By.CSS_SELECTOR, 'div.tcard.active')
        phone_pop_up = (By.CLASS_NAME, 'np-button')
        phone_input = (By.ID, 'phone')
        next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
        code_input = (By.ID, 'code')
        confirm_button = (By.XPATH, '//*[contains(text(), "Confirmar")]')


        def __init__(self, driver):
            self.driver = driver

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
            self.driver.find_element(*self.comfort_button).click()

        def open_pop_up(self):
            WebDriverWait(self.driver, 15).until(expected_conditions.element_to_be_clickable(self.phone_pop_up)).click()

        def set_phone_number(self):
            phone_input = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable( self.phone_input))
            phone_input.clear()
            phone_input.send_keys(data.phone_number)
            self.driver.find_element(*self.next_button).click()

        def get_phone_number(self):
            return self.driver.find_element(self.phone_input).get_property('value')

        def set_code(self):
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.code_input))
            self.driver.find_element(*self.code_input).send_keys(retrieve_phone_code(driver=self.driver))
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.confirm_button))
            self.driver.find_element(*self.confirm_button).click()

        def get_confirmation_code(self):
            return self.driver.find_element(self.code_input).get_property('value')

time.sleep(10)





time.sleep(5)