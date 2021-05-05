import math
posts = 5
post_counter = 0
_max = 2
counter = 0
loops = math.ceil(posts/_max)
print(loops)

for loop in range(loops):
    print('currently on loop {}'.format(loop))
    while counter < _max:
        for post in range(posts):

            print('currently on post {}'.format(post))
