from psychopy import visual, core, event

win = visual.Window((1024,768))

ratingScale = visual.RatingScale(win,low=1, high=100, markerStart=1,leftKeys='1', rightKeys = '2', skipKeys = 'tab', acceptKeys='4')
ratingScale.slidingInterval = 0.1

while ratingScale.noResponse:
    ratingScale.draw()
    win.flip()
rating = ratingScale.getRating()
decisionTime = ratingScale.getRT()
choiceHistory = ratingScale.getHistory()