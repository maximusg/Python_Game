import pickle
from pathlib import Path




def saveGame(array, stateName="default"):
    cwd = Path.cwd()
    saveLocation = cwd.joinpath('levels', 'game_state')
    with open (saveLocation.joinpath(stateName),"wb") as write_file:
        pickle.dump(array,write_file,)



a=[1,2,3,4]
b="string"
c=b#ref
d=234#int

saved=[a,b,c,d]

saveGame(saved)

def loadGame(stateName="default"):
    cwd = Path.cwd()
    saveLocation = cwd.joinpath('levels', 'game_state')
    location = saveLocation.joinpath(stateName)
    levelState=None
    try:
        with open (location,"rb") as read_file:
            levelState= pickle.load(read_file)
    except FileNotFoundError as Error:
        raise ("ERROR: LoadGame failed " + Error)
    
    return levelState

game = loadGame()

print(game)

        