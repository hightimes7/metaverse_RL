import os.path  # 파일 디렉토리 관련 정보

def place(obj, wd):
    if os.path.isfile(f'{obj}.fbx'):
        wd[2] = f'{obj}.fbx is exist'
        print(wd[2])
    elif os.path.isfile(f'{obj}.py'):
        pyMod = __import__(obj)
        if pyMod == None:
            print(f'Error: module loading {obj} is failed')
            return
        wd[2] = pyMod
        print(f'python module loading {obj} is succeded')
        else:
            print(f'Loading {obj} is failed')

worldData = {
    'Reversi': [(10,10), 0, None],
    'Sofa': [(15,15), 90, None]
}

for obj in worldData:
    place(obj, worldData[obj])

rObj = getattr(worldData['Reversi'][2], 'Reversi')()
while True:
    s = input('>> ')
    if s == 'quit' : break
    ret = rObj.runCommand(s)
    print(ret)
