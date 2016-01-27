#
# Example file for working with classes
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)

import bottle
import beaker.middleware
import simplejson
from bottle import route, redirect, post, run, request, hook
from instagram import client, subscriptions
from instagram.client import InstagramAPI

myAccessToken  = '723066430.f01b0ca.733da33d9055407fa018ac698908df78'
myClientID     = 'f01b0ca9cbdd43afaabe4abf564e0771'
myClientSecret = 'd45cab5e7d6f4b1581a2b89e9db6c037'
lav_q_id = 723066430;

def grab_all_media(id):
    api = client.InstagramAPI(access_token=myAccessToken, client_secret=myClientSecret)
    recent_media, next = api.user_recent_media(user_id=id)
    while next:
        more_media, next = api.user_recent_media(user_id=id, with_next_url=next)
        recent_media.extend(more_media)
        
    return recent_media

def northernmost_media():
    all_media = grab_all_media()    
    latitude = -90
    result_media = "Not found"
    for media in all_media:
        if hasattr(media, 'location'):
            if  latitude < media.location.point.latitude :
                latitude = media.location.point.latitude
                result_media = media
                
    return result_media
        
        
def southernmost_media(id=1):
    all_media = grab_all_media(id)
    latitude = 90
    result_media = "Not found"
    for media in all_media:
        if hasattr(media, 'location'):
            if  latitude > media.location.point.latitude :
                latitude = media.location.point.latitude
                result_media = media
                
    return result_media

def westernmost_media():
    all_media = grab_all_media();
    longitude = 180
    result_media = '';
    for media in all_media:
        if (hasattr(media, 'location')):
            if longitude > media.location.point.longitude :
                longitude = media.location.point.longitude;
                result_media = media;

    return result_media;

def easternmost_media(id=lav_q_id):
    all_media = grab_all_media(lav_q_id);
    longitude = -180;
    result_media = '';
    for media in all_media:
        if hasattr(media, 'location'):
            if longitude < media.location.point.longitude:
                longitude = media.location.point.longitude;
                result_media = media;
    return result_media;
    

def recent_med():
    content = "<h2>User Recent Media</h2>"
    
    recent_media = grab_all_media()
    
    media_count = 0;
    total_likes = 0;
    
    photos = []
    for media in recent_media:
        photos.append('<div style="float:left;">')
        if(media.type == 'video'):
            photos.append('<video controls width height="150"><source type="video/mp4" src="%s"/></video>' % (media.get_standard_resolution_url()))
        else:
            photos.append('<img src="%s"/>' % (media.get_low_resolution_url()))
        photos.append("<br/> <a href='/media_like/%s'>Like</a>  <a href='/media_unlike/%s'>Un-Like</a>  LikesCount=%s</div>" % (media.id,media.id,media.like_count))
        media_count += 1
        total_likes += media.like_count
        if hasattr(media, 'location'):
            print media.location.point.latitude, media.location.point.longitude, media.link
        else:
            print "NO LOCATION"
        
    content += ''.join(photos)
    return content, media_count, total_likes

def main():
    api = InstagramAPI(client_id=myClientID, client_secret=myClientSecret)
    user_search = api.user_search(q='tlmnva')
    user_me = user_search[0]
    recent_media, next = api.user_recent_media(user_id=user_me.id, count=10)
    media = easternmost_media(user_me.id)
    print media.link

    # media_id = media.id;
    # print media.like_count;
    # #api.like_media(media_id);
    # #print media.like_count;
    # print media.link;


#    print user_me.id;
#     for user in user_search:
#         if (user.username == "lav_q"):
#             user_me = user
#             break
    
#   print user_me.username, user_me.profile_picture#, user_me.count_media
#     popular_media = api.media_popular()
#     for media in popular_media:
#         print media.user, media.like_count
  
if __name__ == "__main__":
  print "started"
  main();
  # north = southernmost_media(lav_q_id);
  # if hasattr(north, 'link'):
  #     print north.link;
  # else:
  #     print "Shit";
