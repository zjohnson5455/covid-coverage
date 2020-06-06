from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from video import Video

f = open("key.txt", "r")
keyPlusNewLine = f.readline()
DEVELOPER_KEY = keyPlusNewLine.rstrip("\n")
f.close()

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def gather_data(searchTerm, maxDepth):
    seedNodes = youtube_search(searchTerm)

    # we want to avoid redundancy in our search
    visited = set()

    queue = []

    f = open("edgelist2.txt", "w")
    f2 = open("nodeattributes2.txt", "w")

    for seed in seedNodes:
        queue.append(seed)
        visited.add(seed.id)
        f2.write(','.join((seed.id, seed.title)).encode('utf-8'))
        f2.write('\n')

    depth = 0

    while queue and depth <= maxDepth:
        n = queue.pop(0)

        relatedVideos = get_related_videos(n.id, n.foundAtDepth)

        for vid in relatedVideos:
            f.write(','.join((n.id,vid.id)).encode('utf-8'))
            f.write('\n')
            if vid.id not in visited:
                visited.add(vid.id)
                f2.write(','.join((vid.id, vid.title)).encode('utf-8'))
                f2.write('\n')
                queue.append(vid)

        depth = n.foundAtDepth + 1

    f.close()
    f2.close()


def get_related_videos(id, currDepth):
    search_response = youtube.search().list(
        relatedToVideoId=id,
        regionCode='US',
        relevanceLanguage='en',
        safeSearch='none',
        fields='items(id, snippet/title)',
        type='video',
        part='id,snippet',
        maxResults=3
    ).execute()

    neighbors = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            video = Video(id, title, currDepth + 1)
            neighbors.append(video)
        else:
            print('Found something that was not a video')

    return neighbors



def youtube_search(searchTerm):

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=searchTerm,
        regionCode='US',
        relevanceLanguage='en',
        safeSearch='none',
        fields='items(id, snippet/title)',
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
            video = Video(id, title, 0)
            seedVideos.append(video)
        else:
            print('Found something that was not a video')

    return seedVideos

if __name__ == '__main__':

    try:
        # youtube_search('coronavirus')
        # get_related_videos('BJXq83_GvY8')
        gather_data('coronavirus', 5)
    except HttpError, e:
        print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
