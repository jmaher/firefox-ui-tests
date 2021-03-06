# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette_driver import By, Wait
from marionette_driver.errors import MarionetteException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestUntrustedConnectionErrorPage(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://ssl-selfsigned.mozqa.com'

    def test_untrusted_connection_error_page(self):
        # In some localized builds, the default page redirects
        target_url = self.browser.get_final_url(self.browser.default_homepage)

        # Test the GetMeOutOfHereButton from an Untrusted Error page
        with self.marionette.using_context('content'):
            self.assertRaises(MarionetteException, self.marionette.navigate, self.url)
            # Wait for the DOM to receive events
            time.sleep(1)

            button = self.marionette.find_element(By.ID, "getMeOutOfHereButton")
            button.click()
            Wait(self.marionette).until(lambda mn: target_url == self.marionette.get_url())
