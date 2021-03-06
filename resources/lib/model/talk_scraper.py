# Custom xbmc thing for fast parsing. Can't rely on lxml being available
# as of 2012-03.
import CommonFunctions as xbmc_common
import json
import requests
import urlparse


def get(html, logger, video_quality='180kbps'):
    '''Extract talk details from talk html
       @param video_quality string in form '\\d+kbps' that should match one of the provided TED bitrates.
    '''

    init_scripts = [script for script in xbmc_common.parseDOM(html, 'script', {'data-spec':'q' } ) if '"talkPage.init"' in script]
    if init_scripts:

        logger('%s = %s' % ('init_scripts', init_scripts), level='debug')

        # let's do this some other way
        init_scripts_start_pos = str(init_scripts).find('{')
        init_scripts = str(init_scripts)[init_scripts_start_pos:]
        init_scripts = init_scripts + '}'

        logger('%s = %s' % ('init_scripts altered', init_scripts), level='debug')

        # let's remove some json breaking invalid characters
        init_scripts = init_scripts.replace('\\n\\t', '')
        init_scripts = init_scripts.replace("\\n})']", '')
        init_scripts = init_scripts.replace('\\\\"', '')
        init_scripts = init_scripts.replace('\\', '')

        logger('%s = %s' % ('init_scripts sliced', init_scripts), level='debug')
        init_scripts = init_scripts[:-4]

        init_json = json.loads(str(init_scripts), strict=False)
        talk_json = init_json['__INITIAL_DATA__']['talks'][0]
        title = talk_json['player_talks'][0]['title']

        logger('%s = %s' % ('title', title), level='debug')

        speaker = talk_json['player_talks'][0]['speaker']

        logger('%s = %s' % ('speaker', speaker), level='debug')

        resources = talk_json['player_talks'][0]['resources']

        logger('%s = %s' % ('resources', json.dumps(resources)), level='debug')

        url = resources['h264'][0]['file']
        pos_of_question_mark = str(url).find('?')
        if pos_of_question_mark >= 0:
            url = str(url)[0:pos_of_question_mark]

        logger('%s = %s' % ('url', url), level='debug')

        plot = talk_json['description']

        logger('%s = %s' % ('plot', plot), level='debug')

        if video_quality != '180kbps':
            url_custom = url.replace('-180k.mp4', '-%sk.mp4' % (video_quality.split('k')[0]))
            if requests.head(url_custom).ok:
                url = url_custom

        return url, title, speaker, plot, talk_json
    else:
        raise Exception('Could not parse HTML:\n%s' % (html))
