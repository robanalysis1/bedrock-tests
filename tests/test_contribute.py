#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests

from unittestzero import Assert

from pages.desktop.contribute import Contribute, Signup

link_check = pytest.mark.link_check
nondestructive = pytest.mark.nondestructive

class TestContribute:

    @nondestructive
    def test_footer_section(self, mozwebqa):
        contribute_page = Contribute(mozwebqa)
        contribute_page.go_to_page()
        bad_links = []
        for link in Contribute.Footer.footer_links_list:
            url = contribute_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @nondestructive
    def test_tabzilla_links_are_correct(self, mozwebqa):
        contribute_page = Contribute(mozwebqa)
        contribute_page.go_to_page()
        Assert.true(contribute_page.header.is_tabzilla_panel_visible)
        contribute_page.header.toggle_tabzilla_dropdown()
        bad_links = []
        for link in Contribute.Header.tabzilla_links_list:
            url = contribute_page.link_destination(link.get('locator'))
            if url.find(link.get('url_suffix')) < 1:
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @nondestructive
    def test_major_link_destinations_are_correct(self, mozwebqa):
        contribute_page = Contribute(mozwebqa)
        contribute_page.go_to_page()
        bad_links = []
        for link in contribute_page.major_links_list:
            url = contribute_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @link_check
    @nondestructive
    def test_major_link_urls_are_valid(self, mozwebqa):
        contribute_page = Contribute(mozwebqa)
        contribute_page.go_to_page()
        bad_urls = []
        for link in contribute_page.major_links_list:
            url = contribute_page.link_destination(link.get('locator'))
            response_code = contribute_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_urls), '%s bad urls found: ' % len(bad_urls) + ', '.join(bad_urls))

    @nondestructive
    def test_sign_up_form_fields_are_visible(self, mozwebqa):
        contribute_page = Contribute(mozwebqa)
        contribute_page.go_to_page()
        signup_page = contribute_page.click_signup()
        bad_fields = []
        for field in signup_page.sign_up_form_fields:
            if not signup_page.is_element_visible(*field.get('locator')):
                bad_fields.append('The field at %s is not visible' % field.get('locator')[1:])
        Assert.equal(0, len(bad_fields), '%s bad fields found: ' % len(bad_fields) + ', '.join(bad_fields))

    @nondestructive
    def test_sign_up_form_is_visible(self, mozwebqa):
        signup_page = Signup(mozwebqa)
        signup_page.go_to_page()
        Assert.true(signup_page.is_sign_up_form_present, 'The sign up form is not present on the page.')
