import requests, colorama

reduce = lambda text, n: (text + ' '*n)[:n]

query = input(colorama.Fore.YELLOW + 'Search: ' + colorama.Style.RESET_ALL)
n_cards = input(colorama.Fore.YELLOW + 'Questions count (empty for all): ' + colorama.Style.RESET_ALL)
items = requests.get('https://kahoot.it/rest/kahoots/?query=%s&cursor=0&limit=50&includeKahoot=true' % query.replace(' ', '+')).json()['entities']


print('No  %s %s answers uuid' % (reduce('name', 30), reduce('description', 40)))
for item in items:
    count = item['card']['number_of_questions']
    if n_cards == '' or int(n_cards) == count:
        name = reduce(item['card']['title'], 30)
        desc = reduce(item['card']['description'], 40).replace('\n', ' ')
        if desc[-1] != ' ': desc = desc[:-3] + '...'
        uuid = item['card']['uuid']
        n_quests = reduce(str(count), 7)
        print('%s %s %s %s %s' % (reduce(str(items.index(item)), 3), name, desc, n_quests, uuid))

while True:
    try:
        n = int(input(colorama.Fore.YELLOW + 'Select quiz: ' + colorama.Style.RESET_ALL))
        if n >= len(items):
            print(colorama.Fore.RED + 'Out of range' + colorama.Style.RESET_ALL)
            continue
        break
    except ValueError:
        print(colorama.Fore.RED + 'Value must be number' + colorama.Style.RESET_ALL)

for question in items[n]['kahoot']['questions']:
    if question['type'] == 'content':
        title = question['title']
        content = reduce(colorama.Fore.LIGHTBLUE_EX + question['description'] + colorama.Style.RESET_ALL, 80)
        if content[-1] != ' ': content = content[:-3] + '...'
    else:
        title = question['question']
        content = ' | '.join([
            [colorama.Back.RED, colorama.Back.LIGHTBLUE_EX, colorama.Back.YELLOW, colorama.Back.GREEN][question['choices'].index(answer)] \
            + (('✔ ') if answer['correct'] else ('✖' + colorama.Style.RESET_ALL + ' ' + colorama.Fore.LIGHTRED_EX)) \
            + reduce(answer['answer'], 20) + colorama.Style.RESET_ALL
            for answer in question['choices']
        ])
    print('[%s%i%s] %s%s%s:' % (colorama.Fore.CYAN, items[n]['kahoot']['questions'].index(question), colorama.Style.RESET_ALL,
                    colorama.Style.BRIGHT + colorama.Fore.LIGHTBLUE_EX, title.replace('&nbsp;', ''), colorama.Style.RESET_ALL))
    print('    ' + content)
