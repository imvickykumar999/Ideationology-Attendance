
api_key = 'AIzaSyC3EsHgVkGg11WfvEgVYuamubsGsjq1n-I'
# The request cannot be completed because you have exceeded your quota

# api_key = 'AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs'

# ------------------------------------------

from googleapiclient.discovery import build
youtube = build('youtube', 'v3',
                developerKey=api_key)

def yts(q = 'puppies', maxResults = 10):
    dogs_videos_ids = youtube.search().list(
        part="id",
        type='video',
        regionCode="US",
        order="relevance",
        q=q,
        maxResults=maxResults,
        fields="items(id(videoId))",
    ).execute()
    return dogs_videos_ids


def com(video_id = 'Cpc_rHf1U6g'):
    dict = {}
    replies = []

    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id
    ).execute()

    for item in video_response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        replycount = item['snippet']['totalReplyCount']

        if replycount>0:
            for reply in item['replies']['comments']:
                reply = reply['snippet']['textDisplay']
                replies.append(reply)

        dict.update({comment: replies})
        replies = []
    return dict


# https://www.thepythoncode.com/article/using-youtube-api-in-python

def tvl(video_id = 'hlznpxNGFGQ'):

    video_request=youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )

    data = video_request.execute()
    # api = 'AIzaSyC3EsHgVkGg11WfvEgVYuamubsGsjq1n-I'
    # url = f'https://www.googleapis.com/youtube/v3/videos?id={vid}&key={api}&part=snippet,contentDetails,statistics,status'
    #
    # resp = requests.get(url=url)
    # data = resp.json()

    data1 = data['items'][0]['snippet']
    data2 = data['items'][0]['statistics']
    data1.update(data2)
    data1.pop('thumbnails', None)
    data1.pop('localized', None)
    data1.pop('description', None)
    data1.pop('tags', None)

    return data1
