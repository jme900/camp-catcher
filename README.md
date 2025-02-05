# camp-catcher
Currently building an open-source Parks Canada site monitor for cancellations of popular sites in BC and Alberta.
# Camp Catcher Backend

Camp Catcher Backend is a Python-based tool designed to continuously monitor Parks Canada's website for campsite availability updates. It serves as the backend component of the Camp Catcher project, which aims to provide timely notifications to users when popular campsites in British Columbia and Alberta (with plans to expand to other provinces) become available due to cancellations.

## Purpose

The primary purpose of the Camp Catcher Backend is to automate the process of monitoring Parks Canada's website for campsite cancellations. By continuously scanning the website for updates, it enables Camp Catcher to promptly notify users when desired campsites become available, allowing outdoor enthusiasts to secure coveted camping spots more efficiently.

## Features

- **Automated Monitoring**: Utilizes web scraping techniques to monitor Parks Canada's website for campsite availability updates.
- **Real-time Notifications**: Sends instant notifications to users via various channels (e.g., email, SMS) when targeted campsites become available.
- **Customizable Alerts**: Allows users to specify their preferred campsites and notification preferences for a personalized camping experience.

## Usage

To use the Camp Catcher Backend, follow these steps:

1. Clone the repository:
```console
git clone https://github.com/your-username/camp-catcher-backend.git
```
2. Install dependencies:
```console
pip install -r requirements.txt
```
3. Configure environment variables (create a free Twilio account for SMS notifications):

Create a `.env` file in the project root directory and specify the following parameters. Ensure your phone numbers 
are formatted correctly according to Twilio API documentation 
```console
TWILIO_SID=XXXXXXXXYYYYYYYYZZZZZZZZ
TWILIO_KEY=XXXXXXXXYYYYYYYYZZZZZZZZ
TWILIO_NUMBER=+10123456789
PERSONAL_NUMBER=+19876543210
```

4. Run the backend service:
```console
python app.py
```
The backend service will start scanning Parks Canada's website for campsite availability updates and send notifications when relevant.

## Contribution

Contributions to the Camp Catcher Backend project are welcome! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).