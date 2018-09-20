def _respons_text_card(type,title,text):
            return {
                'actionResponse': {'type': type},
                "cards": [
                {
                'header': {'title': title, 'subtitle': 'City of Edmonton chatbot', 'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png','imageStyle': 'IMAGE'}
                },                      
                {
                "sections": [
                {
                "widgets": [
                {"textParagraph": {"text": text}}
                ]
                }]
                }
                ]
                }

def _respons_textButton_card(type,title,text, url):
            return {
                'actionResponse': {'type': type},
                "cards": [
                {
                'header': {'title': title,'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png','imageStyle': 'IMAGE'}
                },                      
                {
                "sections": [
                {
                "widgets": [
                {"buttons": [{"textButton": {"text": text,"onClick": {"openLink": {"url": url}}}}]}
                ]
                }]
                }
                ]
                }



def _respons_text_with_bottom_link_card(type,title,text,buttonText,buttonUrl):
            return {
                'actionResponse': {'type': type},
                "cards": [
                {
                'header': {'title': title,'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png','imageStyle': 'IMAGE'}
                },                      
                {
                "sections": [
                {
                "widgets": [
                {"textParagraph": {"text": text}},
                {'buttons': [{'textButton': {'text': buttonText, 'onClick': {'openLink': {'url': buttonUrl}}}}]}
                ]
                }]
                }
                ]
                }



def _text_card_with_image(headertitle, headerimage,text, widgetimage):
            return {
            'cards': [{'header': {'title': headertitle, 'imageUrl': headerimage,'imageStyle': 'IMAGE'}}, 
            {'sections':[{
            'widgets': [
            {'textParagraph': {'text': text}},
            {'image': {'imageUrl': widgetimage}}
            ]
            }
            ]
            }
            ]
            } 


def create_cards(cards_order):
    INTERACTIVE_TEXT_BUTTON_ACTION = "doTextButtonAction"
    INTERACTIVE_IMAGE_BUTTON_ACTION = "doImageButtonAction"
    INTERACTIVE_BUTTON_PARAMETER_KEY = "param_key"
    BOT_HEADER = 'Card Bot Python'

    response = dict()
    cards = list()
    widgets = list()
    header = None

    words = cards_order.lower().split()

    for word in words:

        if word == 'header':
            header = {
                'header': {
                    'title': BOT_HEADER,
                    'subtitle': 'Card header',
                    'imageUrl': 'https://goo.gl/5obRKj',
                    'imageStyle': 'IMAGE'
                }
            }

        elif word == 'textparagraph':
            widgets.append({
                'textParagraph' : {
                    'text': '<b>This</b> is a <i>text paragraph</i>.'
                }
            })

        elif word == 'keyvalue':
            widgets.append({
                'keyValue': {
                    'topLabel': 'KeyValue Widget',
                    'content': 'This is a KeyValue widget',
                    'bottomLabel': 'The bottom label',
                    'icon': 'STAR'
                }
            })

        elif word == 'interactivetextbutton':
            widgets.append({
                'buttons': [
                    {
                        'textButton': {
                            'text': 'INTERACTIVE BUTTON',
                            'onClick': {
                                'action': {
                                    'actionMethodName': INTERACTIVE_TEXT_BUTTON_ACTION,
                                    'parameters': [{
                                        'key': INTERACTIVE_BUTTON_PARAMETER_KEY,
                                        'value': event_message
                                    }]
                                }
                            }
                        }
                    }
                ]
            })

        elif word == 'interactiveimagebutton':
            widgets.append({
                'buttons': [
                    {
                        'imageButton': {
                            'icon': 'EVENT_SEAT',
                            'onClick': {
                                'action': {
                                    'actionMethodName': INTERACTIVE_IMAGE_BUTTON_ACTION,
                                    'parameters': [{
                                        'key': INTERACTIVE_BUTTON_PARAMETER_KEY,
                                        'value': event_message
                                    }]
                                }
                            }
                        }
                    }
                ]
            })

        elif word == 'textbutton':
            widgets.append({
                'buttons': [
                    {
                        'textButton': {
                            'text': 'TEXT BUTTON',
                            'onClick': {
                                'openLink': {
                                    'url': 'https://developers.google.com',
                                }
                            }
                        }
                    }
                ]
            })

        elif word == 'imagebutton':
            widgets.append({
                'buttons': [
                    {
                        'imageButton': {
                            'icon': 'EVENT_SEAT',
                            'onClick': {
                                'openLink': {
                                    'url': 'https://developers.google.com',
                                }
                            }
                        }
                    }
                ]
            })

        elif word == 'image':
            widgets.append({
                'image': {
                    'imageUrl': 'https://goo.gl/Bpa3Y5',
                    'onClick': {
                        'openLink': {
                            'url': 'https://developers.google.com'
                        }
                    }
                }
            })



    if header != None:
        cards.append(header)

    cards.append({ 'sections': [{ 'widgets': widgets }]})
    response['cards'] = cards

    return respons
