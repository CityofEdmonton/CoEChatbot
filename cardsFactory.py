def _respons_text_card(type,title,text):
	        return {
                'actionResponse': {
                    'type': type
                },
                "cards": [
                {
                'header': {
                    'title': title,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
                }
                },                      
                {
                "sections": [
                        {
                "widgets": [
                {
                    "textParagraph": {
                    "text": text
                    }
                }
            ]
            }
            ]
            }
            ]
        }

def _respons_textButton_card(type,title,text, url):
	        return {
                'actionResponse': {
                    'type': type
                },
                "cards": [
                {
                'header': {
                    'title': title,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
                }
                },

                {
                "sections": [
                    {
                    "widgets": [
                        {
                        "buttons": [
                            {
                             "textButton": {
                                "text": text,
                                "onClick": {
                                  "openLink": {
                                    "url": url
                                  }
                                }
                              }
                            }
                         ]
                        
                        }
                ]
            }
            ]
        }
        ]
        }



def _respons_text_with_bottom_link_card(type,title,text,buttonText,buttonUrl):
            return {
                'actionResponse': {
                    'type': type
                },
                "cards": [
                {
                'header': {
                    'title': title,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
                }
                },                      
                {
                "sections": [
                        {
                "widgets": [
                {
                   "textParagraph": {
                    "text": text
                    }
                },
                {'buttons': [{'textButton': {'text': buttonText, 'onClick': {'openLink': {'url': buttonUrl}}}}]}

            ]
            }
            ]
            }
            ]
        }