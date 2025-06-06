📌 README.md - Fitness Studio Booking API
Fitness Studio Booking API
A simple Django-based API for managing fitness class bookings. Clients can view available classes, book a spot, and retrieve their bookings.

🚀 Features
* View all available classes
* Create new fitness classes (admin access)
* Book a class (if slots available)
* Fetch bookings by client email
* Validation to prevent duplicate class entries

⚙️ Setup & Installation
* Clone the Repository
    git clone {https://github.com/amithuu/fitness_studio.git}
    cd fitness_studio

* Create & Activate Virtual Environment
    * python -m venv env

* Activate the environment:
    * Windows: env\Scripts\activate
    * Mac/Linux: source env/bin/activate

* Install Dependencies
    pip install -r requirements.txt

* Run Migrations & Setup Database
    python manage.py makemigrations
    python manage.py migrate

* Create Superuser (for Admin Panel)
    python manage.py createsuperuser

* Run the Server
    python manage.py runserver

** Now, the API is running on: http://127.0.0.1:8000/ **

🔗 API Endpoints

GET /api/classes/ - Fetch Available Classes [Returns a list of all upcoming fitness classes (name, date/time, instructor, available slots)]

Browser Usage:
Open URL: http://127.0.0.1:8000/api/classes/

Postman Request: ** https://booking-0785.postman.co/workspace/84c588fb-c2d5-49b7-8481-2c229e497ccb/request/43356236-b0eb9741-0248-4e29-9f10-b90174d415a6?action=share&source=copy-link&creator=43356236&ctx=documentation **



POST /api/classes/create/ - Create a New Class

Browser Usage:
Open URL: http://127.0.0.1:8000/api/classes/create/

Postman Request: ** https://booking-0785.postman.co/workspace/84c588fb-c2d5-49b7-8481-2c229e497ccb/request/43356236-4025e445-24a5-4e84-bddb-0fdd5e8a1a3f?action=share&source=copy-link&creator=43356236&ctx=documentation **



POST /api/book/ - Book a Class  [Accepts a booking request (class_id, client_name, client_email)   Validates if slots are available, and reduces available slots upon successful booking]

Browser Usage:
Open URL: http://127.0.0.1:8000/api/book/

Postman Request: ** https://booking-0785.postman.co/workspace/84c588fb-c2d5-49b7-8481-2c229e497ccb/request/43356236-8e0a8b76-8db7-4e1f-ba65-d7ee7ba318cf?action=share&source=copy-link&creator=43356236&ctx=documentation **



GET /api/bookings/{email}/ - Fetch Bookings by Client Email [Returns all bookings made by a specific email address]

Browser Usage:
Open URL: http://127.0.0.1:8000/api/bookings/john@example.com/


Postman Request: ** https://booking-0785.postman.co/workspace/84c588fb-c2d5-49b7-8481-2c229e497ccb/request/43356236-fcebc7eb-9ffd-419f-994c-a92d56123093?action=share&source=copy-link&creator=43356236&ctx=documentation **


* * To run Test Cases : > python manage.py test booking * *
