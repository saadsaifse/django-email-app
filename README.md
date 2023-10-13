# django-email-app

Rest endpoints to send and track emails through ESPs (Email Service Providers). This app is build on Django 4 framework, Django Rest Framework, and Anymail library (https://github.com/anymail/django-anymail). Although Anymail supports various ESPs and makes this API extendable, presently, the Postmark ESP (https://postmarkapp.com/) is being used.

## Getting Started
The project is built using docker containers where django, postgres, and other frameworks are installed.
1. Make sure you have docker installed on your machine to build this API.
2. Use the `.env.sample` file to create a `.env` file at the root of project directory.
3. To get the `POSTMARK_SERVER_TOKEN`, create a free account on Postmark using a business domain. In free version, the emails can only be sent and received for the users in the same business domain.
It will also create a server in Postmark. From the server settings, go to the API Token tab and copy the Server API tokens and use it for the env variable above.
1. [OPTIONAL] If you want to setup a webhook for production, open the **Default Transactional Stream** and follow the instructions there. You *don't* need to set that up for development purposes.
2. Set your own `WEBHOOK_SECRET`
3. Make sure you have both docker and docker-compose installed and they are accessible from the command line. Verify it by running `docker --version` and `docker-compose --version`
4. Run `docker-compose build`
5. Run `docker-compose run --rm app sh -c "python manage.py createsuperuser --email admin@example.com --username admin"` to create a superuser admin. Feel free to use any emails or username. You will be asked for a password.
6.  Run `docker-compose up`
7.  Head over to your browser and browse to http://127.0.0.1:8000/api/docs. This will open the Swagger UI, that you can use to authorize using the superuser credentials and call the endpoints.

## Functionalities and Endpoints

1. `admin/` -> django admin
2. `api/docs/` -> swagger UI
3. `api/email/emails` -> email list with documented filtering
4. `api/email/send` -> send an email to multiple recipients with attachment
5. `api/email/status` -> get status of emails using documented filters
6. `api/email/webhook/` -> receive webhook events form your ESP (i.e, Postmark). Currently the delivery events are handled and the status of emails is updated

**Notes:**
1. Use uppercase email status values in filters as written in the enum under `app/emailSender/models.py`.
2. Use the message_id returned after sending the email to filter it while getting
3. Use comma-separated recipient email addresses to send to multiple recipients. Those emails will get the same message_id but individual `SentEmail` entry and status tracking in the database. This helps tracking statuses efficiently.

## Calling Webhooks During Development
During development, testing webhook is a manual process. Use the following curl request to trigger a Delivery webhook and to update the status of any email to DELIVERED.

```bash
curl http://changemewith16characters:changemewith16characters@127.0.0.1:8000/api/email/webhook/postmark/tracking/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
  "MessageID": "9e072697-fc89-40a9-bfc1-4d967f8ae26f",
  "Recipient": "test@example.com",
  "DeliveredAt": "2014-08-01T13:28:10.2735393-04:00",
  "Details": "Test delivery webhook details",
  "Tag": "welcome-email",
  "ServerID": 23,
  "Metadata": {
    "a_key": "a_value",
    "b_key": "b_value"
  },
  "RecordType": "Delivery",
  "MessageStream": "outbound"
}'
```

Just replace the first part of the url with your `WEBHOOK_SECRET`, your message id and recipient. To trigger other kinds with different payloads, visit https://postmarkapp.com/developer/webhooks/webhooks-overview

## Design Decisions

1. Docker is used for usability, portability and consistent deployments.
2. Flake8 linter is used to have consistent coding formatting. Use `docker-compose run --rm app  sh -c "flake8"` to check errors.
3. Anymail library is used as it supports multiple ESPs that can easily swap out the existing Postmaker. It was also the recommended library by Postmaker.
4. Swagger OpenAPI UI is provided built-in and is used for documentation and testing.
5. Email attachments are stored in a mounted docker volume so that the attachments can live if the container restarts.
6. Postgres data is stored in a mounted docker volume so that the the data can persist if the container restarts.
7. Coded using Behavior-driven development as TDD might have required more time.
8. Webhook are implemented using Django Signals in the `emailSender` app. All signals live under one submodule `emailSender.signals`