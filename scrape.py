import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

f = open("key.txt", "r")
keyPlusNewLine = f.readline()
DEVELOPER_KEY = keyPlusNewLine.rstrip("\n")
f.close()

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

SEARCH_TERM = 'basketball'

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=SEARCH_TERM,
    part='id,snippet',
    maxResults=10
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))

  print 'Videos:\n', '\n'.join(videos), '\n'
  print 'Channels:\n', '\n'.join(channels), '\n'
  print 'Playlists:\n', '\n'.join(playlists), '\n'


if __name__ == '__main__':

  try:
    youtube_search()
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
