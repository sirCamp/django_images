from django_cron import CronJobBase, Schedule
from django.conf import settings
from twython import Twython
from cron.models import Configuration
from cron.models import Photo
from cron.models import Album
from django.core.exceptions import ObjectDoesNotExist
import time
from django.utils import timezone
from django.core.mail import get_connection, EmailMultiAlternatives

class RetriveImageCron(CronJobBase):

    RUN_EVERY_MINS = 1 # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.retrive_image_cron'    # a unique code

    def do(self):

        print("CRON STARTED")


        access_token_configuration = None
        album = None
        last_check_configuration = None
        results = None

        ## retrive or create token
        try:

            access_token_configuration = Configuration.objects.get(configuration_key='ACCESS_TOKEN')

            ACCESS_TOKEN = access_token_configuration.configuration_value

            print("Token: found!")


        except ObjectDoesNotExist:

            twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET, oauth_version=2)

            ACCESS_TOKEN = twitter.obtain_access_token()

            access_token_configuration = Configuration.objects.create(configuration_key='ACCESS_TOKEN',
                                                                      configuration_value=ACCESS_TOKEN)
            print("Token: saved!")


        twitter = Twython(settings.TWITTER_API_KEY, access_token=ACCESS_TOKEN)


        ## retrive ore create last check
        try:

            last_check_configuration = Configuration.objects.get(configuration_key='NEXT_ID')

            results = twitter.search(

                q=settings.TWITTER_SEARCHED_HASHTAG,
                result_type='mixed',
                count=100,
                filter='twimg',
                since_id=last_check_configuration.configuration_value,
                include_entities=True
            )


            print("Search twitter since_id: "+last_check_configuration.configuration_value)

        except ObjectDoesNotExist:

            print("Search twitter with no id")

            last_check_configuration = Configuration.objects.create(
                configuration_key='NEXT_ID',
                configuration_value='',
            )

            results = twitter.search(
                q=settings.TWITTER_SEARCHED_HASHTAG,
                count=100,
                filter='twimg',
                result_type='mixed',
                include_entities=True
            )


        ## retrive or create the current album
        try:

            album = Album.objects.get(album_name='album_'+settings.TWITTER_SEARCHED_HASHTAG)
            print "Album find!"

        except ObjectDoesNotExist:

            album = Album.objects.create(

                album_name='album_'+settings.TWITTER_SEARCHED_HASHTAG,
                album_photos=0,
                album_next_goal=settings.ALBUM_GOALS[0],
                album_created_at=timezone.now(),
                album_updated_at= timezone.now()
            )
            print "New Album created!"

        ## parsing query result

        for result in results.get('statuses'):

            for media in result.get('entities').get('media'):

                print media.get('media_url')

                if not Photo.objects.filter(photo_url=media.get('media_url')).exists():

                    hashtags = ""

                    for tag in result.get('entities').get('hashtags'):
                        hashtags += tag.get('text') + ","

                    hashtags = hashtags[:-1]

                    photo = Photo.objects.create(

                        photo_url=media.get('media_url'),
                        photo_https_url=media.get('media_url_https'),
                        photo_user=result.get('user').get('screen_name'),
                        photo_user_name=result.get('user').get('name'),
                        photo_likes=int(result.get('favorite_count')),
                        photo_post_id=int(result.get('id')),
                        photo_hashtags=hashtags,
                        photo_created_at=timezone.now(),
                        photo_album=album

                    )

                    album.album_photos = int(album.album_photos) + 1
                    album.save()
                    self.send(album)

                    print photo
                else:

                    print "This phosto already exsists"



        last_check_configuration.configuration_value=str(results.get('search_metadata').get('max_id_str'))

        last_check_configuration.save()

        print "CRON FINISHED"



    def send(self,album):

        if album.album_next_goal == album.album_photos and album.album_next_goal <= settings.ALBUM_GOALS[len(settings.ALBUM_GOALS)-1]:

            next_goal_index = settings.ALBUM_GOALS.index(album.album_next_goal)
            next_goal_index = int(next_goal_index) + 1

            print "arrivo"
            try:

                connection = get_connection()
                email_from = settings.EMAIL_FROM
                email_to = settings.EMAIL_TO
                email_copy = settings.EMAIL_BCC
                email_body = settings.EMAIL_BODY
                email_subject = settings.EMAIL_SUBJECT

                email_subject = email_subject % (settings.TWITTER_SEARCHED_HASHTAG, album.album_next_goal)

                print "try to send email"

                msg = EmailMultiAlternatives(

                    email_subject,
                    email_body,
                    email_from,
                    [email_to],
                    email_copy,
                    connection=connection
                )

                msg.send()
                print "Mail sended"

                if album.album_next_goal < settings.ALBUM_GOALS[len(settings.ALBUM_GOALS)-1]:
                    album.album_next_goal = settings.ALBUM_GOALS[next_goal_index]
                else:
                    album.album_next_goal = settings.ALBUM_GOALS_LIMIT

                album.save()
                print "Album saved"


            except IndexError as e:
                print "No mail to send"


