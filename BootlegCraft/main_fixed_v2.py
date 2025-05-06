from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel
from panda3d.core import TextNode, Vec4

loadPrcFile('settings.prc')

def degToRad(degrees):
    return degrees * (pi / 180.0)

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

    def setupLights(self):
        mainLight = DirectionalLight('main light')
        mainLightNodePath = self.render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        self.render.setLight(mainLightNodePath)

        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNodePath)

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.grassBlock = self.loader.loadModel('grass-block.glb')
        self.dirtBlock = self.loader.loadModel('dirt-block.glb')
        self.sandBlock = self.loader.loadModel('sand-block.glb')
        self.stoneBlock = self.loader.loadModel('stone-block.glb')

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.selectedBlockType = 'grass'

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()

        self.menuActive = False
        self.createMenu()

        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb')
        }

    def update(self, task):
        if self.menuActive:
            return task.cont

        dt = self.globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def setSelectedBlockType(self, type):
        self.selectedBlockType = type

    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[type]
        blockModel.instanceTo(newBlockNode)

        if type == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont
    
    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])
    
    def setSelectedBlockType(self, type):
        self.selectedBlockType = type
    
    def handleLeftClick(self):
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 12:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):
        self.cameraSwingActivated = True

        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)  # Confine mouse to window
        self.win.requestProperties(properties)

    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)  # Increased FOV to 90 degrees

        crosshairs = OnscreenImage(
            image = 'crosshairs.png',
            pos = (0, 0, 0),
            scale = 0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, type):
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        # Fix grass texture orientation by rotating the grass block model
        if type == 'grass':
            self.grassBlock.instanceTo(newBlockNode)
            newBlockNode.setHpr(0, 90, 0)  # Rotate 90 degrees on pitch to fix texture orientation
        elif type == 'dirt':
            self.dirtBlock.instanceTo(newBlockNode)
        elif type == 'sand':
            self.sandBlock.instanceTo(newBlockNode)
        elif type == 'stone':
            self.stoneBlock.instanceTo(newBlockNode)

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def createMenu(self):
        self.menuFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.menuFrame.hide()

        self.continueButton = DirectButton(
            text="Continue",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.toggleMenu
        )
        self.exitButton = DirectButton(
            text="Exit",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.exitGame
        )

        self.continueButton.reparentTo(self.menuFrame)
        self.exitButton.reparentTo(self.menuFrame)

    def toggleMenu(self):
        if self.menuActive:
            self.menuFrame.hide()
            self.menuActive = False
            self.captureMouse()
        else:
            self.menuFrame.show()
            self.menuActive = True
            self.releaseMouse()

    def exitGame(self):
        self.userExit()

game = MyGame()
game.run()
