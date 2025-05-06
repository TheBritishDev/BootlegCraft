from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    loadPrcFile,
    DirectionalLight,
    AmbientLight,
    TransparencyAttrib,
    WindowProperties,
    CollisionTraverser,
    CollisionNode,
    CollisionBox,
    CollisionRay,
    CollisionHandlerQueue,
    TextNode,
    Vec4,
)
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame, DirectButton

# Load configuration
loadPrcFile('settings.prc')


def degToRad(degrees):
    """Convert degrees to radians."""
    return degrees * (pi / 180.0)


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Initialize variables
        self.selectedBlockType = 'grass'
        self.menuActive = False
        self.cameraSwingActivated = False
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        # Load assets and setup the game
        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()
        self.createMenu()

        # Add the update task
        self.taskMgr.add(self.update, 'update')

    def loadModels(self):
        """Load block models."""
        self.blockModels = {
            'grass': self.loader.loadModel('grass-block.glb'),
            'dirt': self.loader.loadModel('dirt-block.glb'),
            'sand': self.loader.loadModel('sand-block.glb'),
            'stone': self.loader.loadModel('stone-block.glb'),
        }

    def setupLights(self):
        """Setup lighting."""
        mainLight = DirectionalLight('main light')
        mainLightNodePath = self.render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        self.render.setLight(mainLightNodePath)

        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNodePath)

    def setupCamera(self):
        """Setup the camera."""
        self.disableMouse()
        self.camera.setPos(0, 0, 3)
        self.camLens.setFov(90)

        # Add crosshairs
        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        # Setup collision for raycasting
        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def setupSkybox(self):
        """Setup the skybox."""
        skybox = self.loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def generateTerrain(self):
        """Generate the terrain."""
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    def createNewBlock(self, x, y, z, blockType):
        """Create a new block at the specified position."""
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        blockModel = self.blockModels[blockType]
        blockModel.instanceTo(newBlockNode)

        if blockType == 'grass':
            newBlockNode.setHpr(0, 90, 0)  # Rotate grass block for proper texture orientation

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)

    def setupControls(self):
        """Setup keyboard and mouse controls."""
        self.accept('escape', self.toggleMenu)
        self.accept('mouse1', self.placeBlock)  # Left click to place blocks
        self.accept('mouse3', self.handleLeftClick)  # Right click to destroy blocks

        # Movement controls
        for key, action in [
            ('w', 'forward'), ('s', 'backward'),
            ('a', 'left'), ('d', 'right'),
            ('space', 'up'), ('lshift', 'down')
        ]:
            self.accept(key, self.updateKeyMap, [action, True])
            self.accept(f'{key}-up', self.updateKeyMap, [action, False])

        # Block selection
        for i, blockType in enumerate(['grass', 'dirt', 'sand', 'stone'], start=1):
            self.accept(str(i), self.setSelectedBlockType, [blockType])

    def updateKeyMap(self, key, value):
        """Update the key map."""
        self.keyMap[key] = value

    def setSelectedBlockType(self, blockType):
        """Set the selected block type."""
        self.selectedBlockType = blockType

    def captureMouse(self):
        """Capture the mouse."""
        self.cameraSwingActivated = True
        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(properties)

    def releaseMouse(self):
        """Release the mouse."""
        self.cameraSwingActivated = False
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def createMenu(self):
        """Create the in-game menu."""
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
        """Toggle the in-game menu."""
        if self.menuActive:
            self.menuFrame.hide()
            self.menuActive = False
            self.captureMouse()
        else:
            self.menuFrame.show()
            self.menuActive = True
            self.releaseMouse()

    def exitGame(self):
        """Exit the game."""
        self.userExit()

    def update(self, task):
        """Update the game state."""
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

    def handleLeftClick(self):
        """Handle left mouse click."""
        self.captureMouse()
        self.removeBlock()

    def removeBlock(self):
        """Remove a block."""
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
        """Place a block."""
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


# Run the game
game = MyGame()
game.run()
