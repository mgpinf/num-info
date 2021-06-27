import phonenumbers
from phone_iso3166.country import phone_country
import truecaller_lookup
import phndir_lookup
import auxillary


class Lookups:

	# sets the webdriver (browser) to firefox or chrome
	def set_browser(self, browser):
		self.browser = browser

	# sets the phone no. based on input
	def set_number(self):
		auxillary.line()
		auxillary.phonenumber_input()
		auxillary.line()

		string_no = input('Enter here          :    ')

		# in case no. is entered in International format, it is converted into E164 format since the parse function can only parse E164 format nos.
		if not string_no.startswith('+'):
			string_no = '+'+string_no

		self.phone_no = phonenumbers.parse(string_no)

		while not phonenumbers.is_valid_number(self.phone_no):
		    auxillary.line()
		    print('Enter valid nuber')
		    auxillary.line()
		    string_no = input('Enter here          :    ')
		    if not string_no.startswith('+'):
		        string_no = '+'+string_no
		    self.phone_no = phonenumbers.parse(string_no)

		self.national_no = self.phone_no.national_number
		self.country_code = self.phone_no.country_code

	# method to handle and run all the lookup processes
	def processes(self):

		self.iso3166_code = phone_country(self.country_code)

		# truecaller lookup (must have a microsoft account)
		self.microsoft_flag = input(
			'Do you have a microsoft account? (Y/n): ').lower()

		if self.microsoft_flag == 'y':
			self.truecaller_instance = truecaller_lookup.TrueCaller(
		            self.iso3166_code, self.national_no, self.browser)

		    # display results only if the lookup is successful
			if self.truecaller_instance.process() != -1:
				self.truecaller_instance.set_lookup_status()

		else:
			auxillary.line()
			print('Microsoft account is required for Truecaller lookup')
			auxillary.line()

		# phndir lookup (applicable only to Indian nos.)
		if self.country_code == 91:
			self.phndir_instance = phndir_lookup.Phndir(self.national_no, self.browser)
			if self.phndir_instance.process() != -1:
				self.phndir_instance.set_lookup_status()
		else:
			auxillary.line()
			print('Phndir lookup only applicable to Indian nos.')
			auxillary.line()

	def display_results(self):

		# colors for displaying results
		colors = ('blue', 'red', 'green')

		if self.truecaller_instance.get_lookup_status():
			self.truecaller_instance.display_results(colors[0], colors[1], colors[2])

		if self.phndir_instance.get_lookup_status():
			self.phndir_instance.display_results(colors[0], colors[1], colors[2])
