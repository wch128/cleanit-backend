import django
django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
#from RecycleITBackend.settings import DATABASES, INSTALLED_APPS
#settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
from django.db.models import Count
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.models import Recycler, Organization, Alert
from datetime import datetime, timedelta


sched = BlockingScheduler()

@sched.scheduled_job('interval', weeks=4)
def timed_job():
    from datetime import datetime, timedelta
    #last_month = datetime.today() - timedelta(days=30)
    alerts = Alert.objects.\
        annotate(dcount=Count('recycler'))
    recipents = []
    for item in Organization.objects.all():
        recipents.append(item.email)

    for item in Recycler.objects.all():
        recipents.append(item.email)

    temp_recipents = ['abdullahjaffer96@gmail.com', 'maousama0396@gmail.com']
    for email in temp_recipents:

        message = Mail(
            from_email='abdullahjaffer96@gmail.com',
            to_emails=email,
            subject='Top Monthly Users',
            html_content='<strong>Top Users this month, '
                             '1. '+str(alerts[0].recycler.username)+
                             ' congratulations to all three, try to maintain'
                             ' your record next month!</strong>')
        try:
            sg = SendGridAPIClient('apikey')
            response = sg.send(message)
        except Exception as e:
            print(e.message)

@sched.scheduled_job('cron', week=4)
def scheduled_job():
    print('This job is run every 4 minutes.')

sched.start()
