from playwright.sync_api import sync_playwright

class BrowserController:
	def __init__(self, browser_type='chrome', headless=True, executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
		self.browser_type = browser_type
		self.headless = headless
		self.executable_path = executable_path
		self.playwright = None
		self.browser = None
		self.context = None
		self.page = None

	def launch_browser(self):
		self.playwright = sync_playwright().start()
		browser_launcher = getattr(self.playwright, self.browser_type)
		launch_args = {"headless": self.headless}
		if self.executable_path:
			launch_args["executable_path"] = self.executable_path
		self.browser = browser_launcher.launch(**launch_args)
		self.context = self.browser.new_context()
		self.page = self.context.new_page()
		return self.page

	def goto(self, url):
		if self.page:
			self.page.goto(url)
		else:
			raise Exception("Browser not launched. Call launch_browser() first.")

	def close_browser(self):
		if self.browser:
			self.browser.close()
		if self.playwright:
			self.playwright.stop()

	def click(self, selector):
		if self.page:
			self.page.click(selector)
		else:
			raise Exception("Browser not launched. Call launch_browser() first.")

	def fill(self, selector, text):
		if self.page:
			self.page.fill(selector, text)
		else:
			raise Exception("Browser not launched. Call launch_browser() first.")

	def get_title(self):
		if self.page:
			return self.page.title()
		else:
			raise Exception("Browser not launched. Call launch_browser() first.")
