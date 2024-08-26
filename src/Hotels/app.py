import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

class HotelBooking(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Show the welcome page initially
        self.show_welcome_page()

        self.main_window.show()

    def show_welcome_page(self):
        # Main layout container for the welcome page
        welcome_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER))

        # WebView to display the YouTube video with autoplay enabled
        video_html = """
            <html>
            <body style="margin:0;">
                <iframe width="680" height="383" 
                src="https://www.youtube.com/embed/yC-X0vKLqTQ?autoplay=1" 
                title="YouTube Video" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
                </iframe>
            </body>
            </html>
        """
        video_webview = toga.WebView(style=Pack(height=383, width=680))
        video_webview.set_content(root_url="", content=video_html)

        # Welcome message
        welcome_label = toga.Label(
            'Welcome to the Luxury Hotel Booking System!',
            style=Pack(padding=(20, 0), font_size=24, text_align=CENTER)
        )

        # Continue button to proceed to the booking interface
        continue_button = toga.Button(
            'Continue to Bookings', on_press=self.show_booking_interface, style=Pack(padding=10, background_color='#4CAF50', color='white')
        )

        welcome_box.add(video_webview)
        welcome_box.add(welcome_label)
        welcome_box.add(continue_button)

        self.main_window.content = welcome_box

    def show_booking_interface(self, widget=None):
        # Main layout container for the booking interface
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER))

        # Header
        header_label = toga.Label(
            '🏨 Hotel Booking System',
            style=Pack(padding_bottom=20, font_size=24, text_align=CENTER)
        )
        main_box.add(header_label)

        # Room booking form
        room_type_label = toga.Label('🛏️ Room Type:', style=Pack(padding=(10, 0)))
        self.room_type_input = toga.Selection(
            items=['Single', 'Double', 'Suite'], style=Pack(flex=1)
        )
        self.room_type_input.on_select = self.update_room_image

        check_in_label = toga.Label('📅 Check-in Date (YYYY-MM-DD):', style=Pack(padding=(10, 0)))
        self.check_in_input = toga.TextInput(placeholder="YYYY-MM-DD", style=Pack(flex=1))

        check_out_label = toga.Label('📅 Check-out Date (YYYY-MM-DD):', style=Pack(padding=(10, 0)))
        self.check_out_input = toga.TextInput(placeholder="YYYY-MM-DD", style=Pack(flex=1))

        # Image area for the room preview
        self.room_image = toga.ImageView(style=Pack(height=200, width=300, padding=20))
        self.update_room_image()

        # User details form
        name_label = toga.Label('👤 Full Name:', style=Pack(padding=(10, 0)))
        self.name_input = toga.TextInput(placeholder="Your Full Name", style=Pack(flex=1))

        email_label = toga.Label('📧 Email:', style=Pack(padding=(10, 0)))
        self.email_input = toga.TextInput(placeholder="Your Email", style=Pack(flex=1))

        credit_card_label = toga.Label('💳 Credit Card Number:', style=Pack(padding=(10, 0)))
        self.credit_card_input = toga.TextInput(placeholder="Credit Card Number", style=Pack(flex=1))

        cvv_label = toga.Label('🔒 CVV:', style=Pack(padding=(10, 0)))
        self.cvv_input = toga.TextInput(placeholder="CVV", style=Pack(flex=1))

        # Button for booking
        self.book_button = toga.Button(
            'Book Now', on_press=self.book_room, style=Pack(padding=10, background_color='#4CAF50', color='white')
        )

        form_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        form_box.add(room_type_label)
        form_box.add(self.room_type_input)
        form_box.add(check_in_label)
        form_box.add(self.check_in_input)
        form_box.add(check_out_label)
        form_box.add(self.check_out_input)
        form_box.add(self.room_image)

        # Adding user and payment details fields to the form
        form_box.add(name_label)
        form_box.add(self.name_input)
        form_box.add(email_label)
        form_box.add(self.email_input)
        form_box.add(credit_card_label)
        form_box.add(self.credit_card_input)
        form_box.add(cvv_label)
        form_box.add(self.cvv_input)

        form_box.add(self.book_button)

        # Wrap the form in a ScrollContainer to enable scrolling
        scroll_container = toga.ScrollContainer(content=form_box, style=Pack(flex=1))

        main_box.add(scroll_container)

        self.main_window.content = main_box

    def update_room_image(self, widget=None):
        room_type = self.room_type_input.value
        if room_type == 'Single':
            self.room_image.image = toga.Image('resources/single_room.jpg')
        elif room_type == 'Double':
            self.room_image.image = toga.Image('resources/double_room.jpg')
        elif room_type == 'Suite':
            self.room_image.image = toga.Image('resources/suite_room.jpg')

    def book_room(self, widget):
        room_type = self.room_type_input.value
        check_in = self.check_in_input.value
        check_out = self.check_out_input.value
        name = self.name_input.value
        email = self.email_input.value
        credit_card = self.credit_card_input.value
        cvv = self.cvv_input.value

        # Check if any field is empty
        if not all([room_type, check_in, check_out, name, email, credit_card, cvv]):
            self.main_window.error_dialog('Incomplete Information', 'Please complete all fields before booking.')
            return

        # Prices per night
        room_prices = {
            'Single': 100,
            'Double': 200,
            'Suite': 500
        }

        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            if check_in_date >= check_out_date:
                raise ValueError("Check-out date must be after check-in date.")

            # Calculate the number of nights
            nights = (check_out_date - check_in_date).days
            total_price = nights * room_prices[room_type]

            # Validate credit card and CVV
            if not credit_card.isdigit() or len(credit_card) not in [13, 16]:
                raise ValueError("Invalid credit card number.")
            if not cvv.isdigit() or len(cvv) != 3:
                raise ValueError("CVV must be exactly 3 digits.")

            # Display the confirmation message and return to home page
            self.show_confirmation_dialog(room_type, check_in, check_out, name, email, total_price)
            
        except ValueError as e:
            self.main_window.error_dialog('Invalid Input', str(e))

    def show_confirmation_dialog(self, room_type, check_in, check_out, name, email, total_price):
        confirmation_message = (
            f"Your reservation has been confirmed!\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Room Type: {room_type}\n"
            f"Check-in: {check_in}\n"
            f"Check-out: {check_out}\n"
            f"Total Price: ${total_price}\n\n"
            f"An email will be sent as confirmation. Thank you for your custom!"
        )
        self.main_window.info_dialog('Booking Confirmed', confirmation_message)

        # Return to the welcome page after confirmation
        self.show_welcome_page()

def main():
    return HotelBooking()
