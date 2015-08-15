from alchemyapi.alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

txt = '''
The Living's organic bricks are produced by combining corn stalks 
(left over after corn processing) and specially developed living root structures 
called mycelium, derived from mushrooms. These base components, pioneered by the 
biomaterial company Ecovative, are placed together in molds and allowed to biologically cement through 
fungal growth. When used as building blocks, the resulting mycelium bricks create 
a structure that temporarily diverts the natural carbon cycle to produce architecture 
that grows out of nothing but earth and returns to nothing but earth-with no waste, no energy, 
and no carbon emissions. This "low-tech biotech" approach offers a new vision for our society's 
approach to physical objects and the built environment through living structures that respond 
to current crises of material sustainability.
'''

response = alchemyapi.combined('text', txt.encode('utf-8', 'ignore'))

if response['status'] == 'OK':
    print('## Keywords ##')
    for keyword in response['keywords']:
        print(keyword['text'], ' : ', keyword['relevance'])
    print('')

    print('## Concepts ##')
    for concept in response['concepts']:
        print(concept['text'], ' : ', concept['relevance'])
    print('')

    print('## Entities ##')
    for entity in response['entities']:
        print(entity['type'], ' : ', entity['text'], ', ', entity['relevance'])
    print(' ')

else:
    print('Error in concept tagging call: ', response['statusInfo'])


