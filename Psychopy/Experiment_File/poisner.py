from psychopy import visual, core, event
import random

maxTrials = 200
validity = 0.75
fixTime = 0.25
arrowTime = 0.5
rt = []
tn = []
cueside = []
valid = []
correct = []
targSide = ''

fix = "+"
arrows = ["<", ">"]
targetSymbol = "#"

# Making our windows and stimuli
expWin = visual.Window(size=(400, 400), fullscr=1)
fixspot = visual.TextStim(expWin, pos=(0, 0), text=fix)
leftArrow = visual.TextStim(expWin, pos=(0, 0), text=arrows[0], height=0.2)
rightArrow = visual.TextStim(expWin, pos=(0, 0), text=arrows[1], height=0.2)
target = visual.TextStim(expWin, pos=(0, 0), text=targetSymbol, height=0.4)
expTimer = core.Clock()

for i in range(1, maxTrials + 1):
    fixspot.draw()
    expWin.flip()
    core.wait(fixTime)
    
    if random.random() < 0.5:
        leftArrow.draw()
        cueside.append("L")
        targPos = (-0.5, 0)
    else:
        rightArrow.draw()
        cueside.append("R")
        targPos = (0.5, 0)
    
    expWin.flip()
    tn.append(i)
    core.wait(arrowTime)

    if random.random() < validity:
        valid.append("T")
    else:
        valid.append("F")
        targPos = (targPos[0] * (-1), targPos[1])

    if cueside[-1] == "L":
        targSide = 'slash'
    else:
        targSide = 'z'

    target.setPos(targPos)
    target.draw()
    expWin.flip()

    expTimer.reset()
    buttonPress = event.waitKeys()
    print(buttonPress)
    
    rt.append(expTimer.getTime())

    if valid[-1] == "T":
        if (buttonPress[-1] == "slash" and cueside[-1] == "R") or \
           (buttonPress[-1] == "z" and cueside[-1] == "L"):
            correct.append("T")
        else:
            correct.append("F")
    else:
        if (buttonPress[-1] == "slash" and cueside[-1] == "R") or \
           (buttonPress[-1] == "z" and cueside[-1] == "L"):
            correct.append("F")
        else:
            correct.append("T")

# Save data to a text file
with open("./posnerData_other_.txt", 'w') as f:
    f.write("TN\tCue\tValid\tReaction Time\tCorrect\n")
    for i in range(0, maxTrials):
        f.write(f"{tn[i]}\t{cueside[i]}\t{valid[i]}\t{str(rt[i])}\t{correct[i]}\n")

f.close()
core.quit()