"""
Discussion in the MW class about handling the processing of commands
"""

# Example commands
cmd = 'ls /etc/hosts -lah | grep .txt > outfile.txt'
cmd = 'ls -l  /usr/local -ah /home/runner/5143shellhelp/ | grep nix > out'
cmd = 'history | grep ls | wc -l > out'
cmd = 'grep < somefile.txt > outfile.txt'
cmd = 'history | grep ls | wc -l > out'

# check for redirect
# note: if no redirect exists, this will error
left,right = cmd.split('>')

# print both sides (if they exist)
print(left)
print(right.strip())

# split on pipes if they exist
cmds = left.split('|')

# loop over each command and strip extra spaces away
i = 0
for cmd in cmds:
    cmds[i] = cmd.strip()
    i += 1
print(cmds)

# example dictionary showing processed commands
parts = {
    'cmd':'',
    'flags':'',
    'params':''
}

parts = {
    'cmd':'history',
    'flags':'',
    'params':''
}

parts = {
    'cmd':'grep',
    'flags':'',
    'params':'ls'
}

parts = {
    'cmd':'wc',
    'flags':['l',''],
    'params':''
}

# example function call
# ls(params=['/etc/hosts','-lah'],flags=[''],stdin=historyOut)