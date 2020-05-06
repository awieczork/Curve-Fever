import numpy as np
import cv2

def draw(img, X, Y):
    cv2.circle(img, (X, Y), int(4), (255, 255, 255), -1)

### GAME CONFIGURATION
# 3.25 change in angle per move
# radius = 5
# speed = 1.8572830964234517
# curve radius = 1.7


actions = ['left', 'right', 'forward']
X = np.random.randint(0 + 200, 898 - 200, 1)
Y = np.random.randint(0 + 200, 898 - 200, 1)
angle = np.random.choice(np.round(np.linspace(0, 360, 120)))
# ANGLE:
# 0 : RIGHT
# 90 : DOWN
# 180 : LEFT
# 270 : UP

radius = 5
speed = 1.8572830964234517
board = np.zeros((898, 898))
boardHIST = np.zeros((898, 898))
draw(board, X, Y)
draw(boardHIST, X, Y)
print(X, Y, angle)
for i in range(500):
    move = np.random.choice(actions, p = [0.4, 0.3, 0.3])
    print(move)
    if move == 'left':
        angle -= 3.25
    elif move == 'right':
        angle += 3.25

    if angle > 360:
        angle -= 360
    elif angle < 360:
        angle += 360

    # X += int(1.7 * speed * np.cos(angle * np.pi/180))
    # Y -= int(1.7 * speed * np.sin(angle * np.pi/180))

    X = np.append(X, X[-1] + int(1.7 * speed * np.cos(angle * np.pi / 180)))
    Y = np.append(Y, Y[-1] + int(1.7 * speed * np.sin(angle * np.pi / 180)))


    if X[-1] >= 898 or X[-1] < 0 or Y[-1] >= 898 or Y[-1] < 0:
        print('Game Over')
        break

    if X.shape[0] == 4:
        if boardHIST[Y[-1], X[-1]] != 0:
            print('Game Over2')
            break
        draw(boardHIST, X[1], Y[1])
        X = np.delete(X, 0)
        Y = np.delete(Y, 0)

    draw(board, X[-1], Y[-1])

    cv2.imshow('View', board)

    if cv2.waitKey(25) & 0xFF == ord("q"):
       cv2.destroyAllWindows()
       break