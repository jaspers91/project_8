from selenium import webdriver
from pages import UrbanRoutesPage
import data
import helpers
class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_addresses_only(self):
        # Open the Urban Routes page
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        from_value = self.driver.find_element(*page.FROM_LOCATOR).get_attribute("value")
        to_value = self.driver.find_element(*page.TO_LOCATOR).get_attribute("value")
        assert from_value == data.ADDRESS_FROM, f"Expected {data.ADDRESS_FROM}, but got {from_value}"
        assert to_value == data.ADDRESS_TO, f"Expected {data.ADDRESS_TO}, but got {to_value}"

    def test_set_addresses_and_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()
        actual_value= page.supportive_card_text()
        assert actual_value in "Supportive"

    def test_phone_number(self):
        # Quit whatever is running
        self.driver.quit()
        # Restart Chrome with the same logging prefs
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)
        # Continue the phone test
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()
        page.phone_button()
        page.phone_number_click(data.PHONE_NUMBER)  # or page.enter_phone(...)
        # optionally click Next if your flow requires it:
        # self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BTN)).click()
        page.phone_number_next()
        sms_code = helpers.retrieve_phone_code(self.driver)
        page.sms(sms_code)
        page.confirm_phone_number()
        actual_value= page.check_phone()
        assert actual_value in data.PHONE_NUMBER, f"Expected {data.PHONE_NUMBER}, but got {actual_value}"

    def test_credit_card_number(self):
        self.driver.quit()
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)
        # Continue the phone test
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()
        page.phone_button()
        page.phone_number_click(data.PHONE_NUMBER)
        page.phone_number_next()
        sms_code = helpers.retrieve_phone_code(self.driver)
        page.sms(sms_code)
        page.confirm_phone_number()
        page.payment_method()
        page.add_card()
        page.card_number(data.CARD_NUMBER)
        page.card_code(data.CARD_CODE)
        page.link_btn()
        actual_value = page.check_card_text()
        assert actual_value in "Card"

    def test_comment(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        # Continue the phone test
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        actual_value = page.comments(data.MESSAGE_FOR_DRIVER)
        assert actual_value == data.MESSAGE_FOR_DRIVER

    def test_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()

        # Open the accordion, then guarantee switch is ON and assert
        page.open_order_requirements()
        page.ensure_blanket_on()
        actual_value = page.handkerchief_text()
        assert actual_value in "Blanket and handkerchiefs"

    def test_ice_cream(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()

        # Open the accordion, then guarantee switch is ON and assert
        page.open_order_requirements()
        actual_value = page.ice_cream()
        assert actual_value in "ice cream"

    def test_final(self):
        # start a fresh driver WITH logging
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)

        page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)

        page.enter_from_location(data.ADDRESS_FROM)
        page.enter_to_location(data.ADDRESS_TO)
        page.enter_custom_option()
        page.taxi_card_option()
        page.taxi_pick()
        page.supportive_card_click()

        # phone + confirm
        page.phone_button()
        page.phone_number_click(data.PHONE_NUMBER)
        page.phone_number_next()
        sms_code = helpers.retrieve_phone_code(self.driver)
        page.sms(sms_code)
        page.confirm_phone_number()

        # add card
        page.payment_method()
        page.add_card()
        page.card_number(data.CARD_NUMBER)
        page.card_code(data.CARD_CODE)
        page.link_btn()

        # IMPORTANT: close the payment modal (with the resilient version I gave you)
        page.close_payment_modal()

        # comment + order requirements
        page.comments(data.MESSAGE_FOR_DRIVER)
        page.open_order_requirements()
        page.handkerchief_text()
        page.ice_cream()
        page.order()
        # order and assert
        actual_value = page.car_search() # make sure this returns the header text
        assert "Car search" in actual_value

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()