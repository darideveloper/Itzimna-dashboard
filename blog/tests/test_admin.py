from time import sleep

from selenium.webdriver.common.by import By

from core.test_base.test_admin import TestAdminSeleniumBase
from blog import models
from utils.media import get_test_image


class PostAdminTestCase(TestAdminSeleniumBase):

    def setUp(self):

        # Submit endpoint
        super().setUp("/admin/blog/post/add")

        self.markdown_selectors = {
            "tool_bar": ".editor-toolbar",
            "bold": 'a[title="Bold (Ctrl-B)"]',
            "editor": ".CodeMirror-scroll",
            "status_bar": ".editor-statusbar",
        }

    def test_markdown_editor_loaded(self):
        """Check if markdown is not allowed in google maps src"""

        elems = self.get_selenium_elems(self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertTrue(elem, f"Element {elem_name} not found")

    def test_no_markdown_in_description(self):
        """
        Check if the editor is loaded with reference elements
        """

        # Add wrapper class to each markdown element
        wrapper_class = "field-description"
        for elem_name, elem in self.markdown_selectors.items():
            self.markdown_selectors[elem_name] = f".{wrapper_class} {elem}"

        elems = self.get_selenium_elems(self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertIsNone(elem, f"Element {elem_name} found (should not be found)")


class ImageAdminTestCase(TestAdminSeleniumBase):

    def setUp(self):

        # Create image instance
        self.image = self.__create_image__()

        # Login
        super().setUp()

        self.endpoint = "/admin/blog/image"

        self.selectors = {
            "copy_btn": ".copy-btn",
            "image": f"img[src*='{self.image.image.url}']",
        }
        
    def __create_image__(self, image_name: str = "test.webp"):
        """Create a test image instance"""
        image = models.Image.objects.create(name=image_name)
        image_file = get_test_image()
        image.image = image_file
        image.save()
        return image

    def test_image_list_view(self):
        """Check if image list view is loaded"""

        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)

        # Check if image is displayed in list view
        elems = self.get_selenium_elems(self.selectors)
        image_elem = elems["image"]
        self.assertTrue(image_elem, "Image not found in list view")

    def test_image_detail_view(self):
        """Check if image detail view is loaded"""

        # Submit endpoint
        self.set_page(f"{self.endpoint}/{self.image.id}/change/")
        sleep(2)

        # Check if image is displayed in detail view
        elems = self.get_selenium_elems(self.selectors)
        image_elem = elems["image"]
        self.assertTrue(image_elem, "Image not found in detail view")

    def test_copy_buttons_loaded(self):
        """validate copy buttons (2 of them) visible in page"""
        
        self.__create_image__("test2.webp")
        
        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)
        
        # Get buttons
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".copy-btn")
        self.assertEqual(len(buttons), 2, "Copy button missing")

    def test_copy_buttons_action(self):
        """Clock in copy button and validate if copied to clipboard"""

        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)

        # Click button
        elems = self.get_selenium_elems(self.selectors)
        button = elems["copy_btn"]
        button.click()
        sleep(2)

        # Check if image is copied to clipboard
        copied_image = self.driver.execute_script(
            "return navigator.clipboard.readText();"
        )
        self.assertIn(
            self.image.image.url, copied_image, "Image not copied to clipboard"
        )
