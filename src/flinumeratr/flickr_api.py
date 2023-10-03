"""
This file contains some methods for calling the Flickr API.
"""

import datetime
import xml.etree.ElementTree as ET

import httpx


class FlickrApi:
    def __init__(self, *, api_key):
        self.client = httpx.Client(
            base_url='https://api.flickr.com/services/rest/',
            params={'api_key': api_key}
        )
    
    def call(self, method, /, **params):
        params['method'] = method
        
        resp = self.client.get(url='', params=params)
        resp.raise_for_status()
        
        # Note: the xml.etree.ElementTree is not secure against maliciously
        # constructed data (see warning in the Python docs [1]), but that's
        # fine here -- we're only using it for responses from the Flickr API,
        # which we trust.
        #
        # [1]: https://docs.python.org/3/library/xml.etree.elementtree.html
        return ET.fromstring(resp.text)


def get_single_photo_info(api: FlickrApi, *, photo_id: str):
    """
    Look up the information for a single photo.
    """
    info_resp = api.call('flickr.photos.getInfo', photo_id=photo_id)
    sizes_resp = api.call('flickr.photos.getSizes', photo_id=photo_id)
        
    # The getInfo response is a blob of XML of the form:
    #
    #       <?xml version="1.0" encoding="utf-8" ?>
    #       <rsp stat="ok">
    #       <photo …>
    #       	<owner
    #               nsid="30884892@N08
    #               username="U.S. Coast Guard"
    #               realname="Coast Guard" …
    #           >
    #       		…
    #       	</owner>
    #       	<title>Puppy Kisses</title>
    #       	<dates
    #               posted="1490376472"
    #               taken="2017-02-17 00:00:00"
    #               …
    #           />
    #       	<urls>
    #       		<url type="photopage">https://www.flickr.com/photos/coast_guard/32812033543/</url>
    #       	</urls>
    #           …
    #       </photo>
    #       </rsp>
    #
    title = info_resp.find('.//photo/title').text
    
    # e.g. '1490376472'
    date_posted = datetime.datetime.fromtimestamp(
        int(info_resp.find('.//photo/dates').attrib['posted'])
    )
    
    # e.g. '2017-02-17 00:00:00'
    date_taken = datetime.datetime.strptime(
        info_resp.find('.//photo/dates').attrib['taken'],
        '%Y-%m-%d %H:%M:%S'
    )
    
    photo_page_url = info_resp.find('.//photo/urls/url[@type="photopage"]').text
    
    # The getSizes response is a blob of XML of the form:
    #
    #       <?xml version="1.0" encoding="utf-8" ?>
    #       <rsp stat="ok">
    #       <sizes canblog="0" canprint="0" candownload="1">
	#           <size
    #               label="Square"
    #               width="75"
    #               height="75"
    #               source="https://live.staticflickr.com/2903/32812033543_c1b3784192_s.jpg"
    #               url="https://www.flickr.com/photos/coast_guard/32812033543/sizes/sq/"
    #               media="photo"
    #           />
	#           <size
    #               label="Large Square"
    #               width="150"
    #               height="150"
    #               source="https://live.staticflickr.com/2903/32812033543_c1b3784192_q.jpg"
    #               url="https://www.flickr.com/photos/coast_guard/32812033543/sizes/q/"
    #               media="photo"
    #           />
    #           …
    #       </sizes>
    #       </rsp>
    #
    # Within this function, we just return all the sizes -- we leave it up to the
    # caller to decide which size is most appropriate for their purposes.
    sizes = [s.attrib for s in sizes_resp.findall('.//size')]
    
    for s in sizes:
        s['width'] = int(s['width'])
        s['height'] = int(s['height'])
    
    return {
        'title': title,
        'date_posted': date_posted,
        'date_taken': date_taken,
        'url': photo_page_url,
        'sizes': sizes,
    }
    
    # resp. ap
    # info = client.get(params={})
    # info = flickr.photos.getInfo(photo_id=category['photo_id'])
    # sizes = flickr.photos.getSizes(photo_id=category['photo_id'])
    #
    # photos = [
    #     {
    #         'title': info['photo']['title']['_content'],
    #         'dates': info['photo']['dates'],
    #         'url': info['photo']['urls']['url'][0]['_content'],
    #         'author': info['photo']['owner']['realname'],
    #         'thumbnail': next(
    #             s['source'] for s in sizes['sizes']['size'] if s['label'] == 'Thumbnail')
    #     },
    # ]
    #