import os

file_names = filter(lambda x: 'EUROSTAT' in x, os.listdir('./'))

def change_encoding(file_names):
    for file_name in file_names:
        lines = []
        with open('./'+file_name, 'r') as f:
            for i, x in enumerate(f):
                y = x.rstrip('\n').decode('latin1').encode('utf8')
                lines.append(y)
                # print x.rstrip('\n').decode('latin1').encode('utf8')
                # if i == 10:
                    # exit()
        with open('./'+file_name, 'w') as f:
            f.write('\n'.join(lines))

change_encoding(file_names)
