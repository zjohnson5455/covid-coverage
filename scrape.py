from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from video import Video

f = open("key.txt", "r")
keyPlusNewLine = f.readline()
DEVELOPER_KEY = keyPlusNewLine.rstrip("\n")
f.close()

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

SEARCH_TERM = 'coronavirus'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def get_related_videos(id):
    search_response = youtube.search().list(
        relatedToVideoId=id,
        type='video',
        part='id,snippet',
        maxResults=5
    ).execute()

    neighbors = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            video = Video(id, title)
            neighbors.append(video)
        else:
            print('Found something that was not a video')


    for neighbor in neighbors:
        print(neighbor.title)

    return neighbors



def youtube_search():

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=SEARCH_TERM,
        type='video',
        part='id,snippet',
        maxResults=3
    ).execute()

    seedVideos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            video = Video(id, title)
            seedVideos.append(video)
        else:
            print('Found something that was not a video')


    for vid in seedVideos:
        print(vid.id)

    return seedVideos

if __name__ == '__main__':

    try:
        # youtube_search()
        get_related_videos('BJXq83_GvY8')
    except HttpError, e:
        print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
