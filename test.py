from cmu_graphics import *
import random

def onAppStart(app):
    app.width = 800
    app.height = 400
    app.highestScore = 0
    app.screen = 1
    app.rectCoords = [(400, 200, 200, 50)]


    #Stage 3
    app.selectedBox = 0

    #Revised Stage 3
    app.eqnLengths = [9, 5, 7, 9]
    app.operators = ['*', '+', '-', '*']
    app.savedOps = []

    #Stage 3 (Timed) (AI helped)
    app.timedMode = True
    app.gameOver = False
    app.stepsPerSecond = 1
    
    #model
    gameModel(app)

    #Controller
    app.message = ''

def gameModel(app): #AI helped 
    app.numElements = None
    app.target = None
    app.grayBoxPosition = []
    app.savedOpsPosition = []
    app.equalSignPosition = []
    app.answerPosition = []
    app.numInBoxes = []
    app.score = 0
    app.timedMode = True
    app.timeLeft = 300
    app.gameOver = False
    app.savedOps = []
    app.usedNums = []

#######################################################INITIALIZATION#####################################################

def redrawAll(app):
    #Main Menu
    if app.screen == 1: drawScreen1(app)

    #Press Play
    elif app.screen == 2: drawScreen2(app)

    #Game Stage
    elif app.screen == 3:
        if app.gameOver:
            drawScreen4(app)
        else: drawScreen3(app)

def drawScreen1(app):
    drawLabel('digitChallenge', 400, 50, size=40, bold=True)
    drawLabel('Click the button to start', 400, 100, size=20)
    for cx, cy, wid, len in app.rectCoords:
        drawRect(cx, cy, wid, len, fill='green', align='center', border='black')
    drawLabel('Start', app.width/2, app.height/2, size= 20, bold=True, align='center')
    drawLabel(f'Highest This Session: {app.highestScore}', 50, 300, size=20, align='left')
    drawLabel('Made By: Ricky Ni', 600, 300, size=20, align='left')

def drawScreen2(app):
    drawLabel('digitChallenge', 400, 50, size=40, bold=True)
    drawLabel('What mode would you like to select?', 400, 100, size=20, align='center')
    counter = 0
    for cx, cy, wid, len in app.rectCoords:
        drawRect(cx, cy, wid, len, fill='green', align='center', border='black')
        drawLabel('Timed', cx, cy, size = 20, align='center', bold = True)
        counter += 1

def drawScreen3(app):
    #Draw Initial Conditions
    drawEquation(app)
    drawNumpad(app)
    drawLabel(app.message, 600,300,size=26, fill='green' if app.message == 'Correct!' else 'red')
    drawLabel(f'Score: {app.score}', 600, 350, size=20)
    drawTime(app)

def drawEquation(app): 
    drawGrayBox(app)
    drawOperator(app)
    drawAnswer(app)
    
def drawGrayBox(app): 
    boxW, boxH = 60,60
    for i, (cx, cy) in enumerate(app.grayBoxPosition):
        drawRect(cx, cy, boxW, boxH, fill='gray' if i != app.selectedBox else 'green',border='black', align='center')
        if app.numInBoxes[i] is not None:
            drawLabel(app.numInBoxes[i], cx, cy, size=26, bold=True)
def drawOperator(app):
    for i, operator in enumerate(app.savedOps):
        cx, cy = app.savedOpsPosition[i]
        drawLabel(operator, cx, cy, size=35, align='center')
    cx, cy = app.equalSignPosition[0]
    drawLabel('=', cx, cy, size=35, align='center')

def drawAnswer(app):
    cx, cy = app.answerPosition[0]
    drawLabel(app.target, cx, cy, size = 26, align='center')
    

def drawNumpad(app): #Used AI to help make this
    buttonW, buttonH = 80, 65
    gap = 10
    btnLeft, btnTop = 60, 175
    for ind in range(9):
        row, col = ind // 3, ind % 3
        bx = btnLeft + col * (buttonW + gap)
        by = btnTop  + row * (buttonH + gap)
        color = 'red' if ind + 1 in app.usedNums else 'gray'
        drawRect(bx, by, buttonW, buttonH, fill=color, border=rgb(180,180,180))
        drawLabel(str(ind + 1), bx + buttonW//2, by + buttonH//2, size=24, bold=True)

    cx = btnLeft + 3 * (buttonW + gap)
    cy = btnTop
    drawRect(cx, cy, buttonW, (buttonH*3 + gap*2), fill=rgb(220,220,220), border=rgb(180,180,180))
    drawLabel('C', cx + buttonW//2, cy + (buttonH + gap) + buttonH/2, size=24, bold=True)

def drawTime(app): #AI helped
    minutes = app.timeLeft//60
    seconds = app.timeLeft%60
    if minutes == 0: 
        if seconds < 30: 
            color = 'red'
        else: color = 'orange'
    else: color = 'black' 
    label = f'{minutes}:{seconds}' if seconds >= 10 else f'{minutes}:0{seconds}'
    drawLabel(label, 750, 25, size=25,fill = color )

def drawScreen4(app):
    drawLabel('Game Over!', 400, 100, size = 40, align='center', bold=True)
    drawLabel(f'Your score was {app.score}', 400, 200, size = 20, align='center', bold=True)
    drawLabel('Click anywhere to try again.', 400, 300, size = 20, align='center', bold=True)
#######################################################VIEW#####################################################

def generateEquation(app): #Used AI to help make this
    #Equation Constants
    eqnSelect = random.randint(0,3)
    app.numElements = app.eqnLengths[eqnSelect] #if 5, 2 gray boxes and 1 operator, if 9, 4 gray boxes and 3 operators
    #Positioning Constants
    middleX, gap = app.width//2, 80
    centerY = 90
    leftmostX = middleX - (app.numElements//2)*gap

    for i in range(app.numElements):
        centerX = leftmostX + i*gap
        if i == (app.numElements - 1):
            numNumbers = (app.numElements - 2)//2 + 1
            calculateAnswer(app, numNumbers)
            app.answerPosition = [(centerX, centerY)]
        elif i%2 == 0:
            app.grayBoxPosition.append((centerX, centerY))
        elif i%2 == 1:
            drawEqual = True if i == (app.numElements - 2) else False
            if drawEqual: 
                app.equalSignPosition.append((centerX, centerY)) 
            else:
                operator = app.operators[random.randint(0,3)]
                app.savedOps.append(operator)
                app.savedOpsPosition.append((centerX, centerY)) 
    app.numInBoxes = [None]*len(app.grayBoxPosition)
    
def calculateAnswer(app, numNumbers): #Used AI to help make this
    listNums = []
    while len(listNums) != numNumbers: #get nums
        num = random.randint(1,9)
        if str(num) not in listNums:
            listNums.append(str(num))
        #turn equation into string
    parts = []
    for i in range(len(listNums)):
        parts.append(listNums[i])
        if i < len(app.savedOps):
            parts.append(app.savedOps[i])
    print(parts)
    eqnStr = ' '.join(parts)

    #evaluate string
    result = eval(eqnStr)
    app.target = result

#######################################################MODEL#####################################################

def onKeyPress(app, key):
    if not app.gameOver: 
        if app.screen == 3 and key == 'enter':
            checkEquation(app)

def checkEquation(app): #Used AI to help make this
    if None in app.numInBoxes:
        app.message = ''
        return 
    parts = []
    for i in range(len(app.numInBoxes)):
        parts.append(str(app.numInBoxes[i]))
        if i < len(app.savedOps):
            parts.append(app.savedOps[i])
    print(parts)
    eqnStr = ' '.join(parts)

    #evaluate string
    result = eval(eqnStr)
    if result == app.target:
        app.message = 'Correct!'
        app.score += 1
        resetEquation(app)
    else: app.message = 'Incorrect! Try again!'

def resetEquation(app):
    app.grayBoxPosition = []
    app.savedOps = []
    app.savedOpsPosition = []
    app.equalSignPosition = []
    app.answerPosition = []
    app.usedNums = []
    generateEquation(app)


def onMousePress(app, mouseX, mouseY):
    if app.screen == 3:
        if app.gameOver == True: #ai helped
            gameModel(app)
            app.message = ''
            app.screen = 1
            app.rectCoords = [(app.width//2, app.height//2, 200, 50)]
            return 
        else: #Ai helped with this
            grayBoxClick(app, mouseX, mouseY)
            key = getNumpadPress(mouseX, mouseY)
            if key is not None and key != 'C' and key not in app.usedNums:
                oldNum = app.numInBoxes[app.selectedBox]
                if oldNum is not None:
                    app.usedNums.remove(oldNum)
                app.numInBoxes[app.selectedBox] = key
                app.usedNums.append(key)
                print(app.numInBoxes)
            elif key == 'C':
                if app.numInBoxes[app.selectedBox] != None: 
                    app.usedNums.remove(app.numInBoxes[app.selectedBox])
                app.numInBoxes[app.selectedBox] = None


    inRect, app.screenSpecific = inRectangle(app, mouseX, mouseY)
    if inRect: 
        if app.screen == 1: app.screen = 2
        elif app.screen == 2: 
            app.screen = 3
            app.timedMode = True
        changeRectangles(app)

def getNumpadPress(mouseX, mouseY):
    btnW, btnH = 80, 65
    gap = 10
    btnLeft, btnTop = 60, 175
    for ind in range(9):
        row, col = ind // 3, ind % 3
        bx = btnLeft + col * (btnW + gap)
        by = btnTop  + row * (btnH + gap)
        if bx <= mouseX <= bx + btnW and by <= mouseY <= by + btnH:
            return ind + 1
    cx = btnLeft + 3 * (btnW + gap)
    cy = btnTop
    if cx <= mouseX <= cx + btnW and cy <= mouseY <= cy + btnH*3 + gap*2:
        return 'C'
    return None




def grayBoxClick(app, mouseX, mouseY):
    boxW, boxH = 60,60
    for i, (cx, cy) in enumerate(app.grayBoxPosition):
        if cx - boxW//2 <= mouseX <= cx + boxW//2 and cy - boxH//2 <= mouseY <= cy + boxH//2:
            app.selectedBox = i


def inRectangle(app, mouseX, mouseY): # If in rectangles, return True else False
    count = 0
    for cx, cy, wid, len in app.rectCoords:
        count += 1
        if (cx - wid/2 <= mouseX <= cx + wid/2) and (cy - len/2 <= mouseY <= cy + len/2):
            if app.screen != 1 and app.screen != 3:
                return (True, count)
            else: return (True, None)
    return (False, None)
        
def changeRectangles(app): #Hard coding rectangle locations
    if app.screen == 1: 
        app.rectCoords = [(app.width//2, app.height//2, 200, 50)]
    elif app.screen == 2:
        app.rectCoords = [(app.width//2, app.height//2, 200, 50)]
    elif app.screen == 3: 
        app.rectCoords = []
        generateEquation(app)
#######################################################CONTROLLER#####################################################

def onStep(app):
    if app.screen == 3 and app.timedMode == True and app.gameOver == False:
        if app.timeLeft > 0:
            app.timeLeft -= 1
        else: 
            app.gameOver = True

runApp()

#Features

#3. Typing number or pressing keypad inputs number into green boxes
#6. Move onto next box after number is inputted
#7. Regenerate equations if negative
#8. Main Menu/Pause button 
#9. 
#NOTES

#1 - Find ways to not hardcode (app.width and app.length for centering)