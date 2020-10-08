# edX MIT 6.00.2x Simulating robots  (Python 2.7)

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.room = []   # Twodimensional list and value is boolean isDirty
        for i in range(width):
            newList = []
            for j in range(height):
                # Create isClean='False' on dimension(i,j)
                # 'False' means the tile is dirty, 'True' that it is clean
                newList.append(False)
            self.room.append(newList)

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x1 = int(math.floor(pos.getX()))
        y1 = int(math.floor(pos.getY()))
        self.room[x1][y1] = True
        return self.room[x1][y1]

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.room[m][n]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        if len(self.room) == 0:
            return 0
        else:
            return len(self.room) * len(self.room[0])

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        countCleaned = 0
        for i in range(len(self.room)):
            for j in range(len(self.room[i])):
                if self.room[i][j]:
                    countCleaned += 1
        return countCleaned

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        xPos = random.random() * self.width
        yPos = random.random() * self.height
        randomPos = Position(xPos,yPos)
        return randomPos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        xPos = pos.getX()
        yPos = pos.getY()
        if (0 <= xPos < self.width) and (0 <= yPos < self.height):
            return True
        else:
            return False

    def __str__(self):
        """ Testfunction to test output """
        for pos in self.room:
            print pos
        if len(self.room) > 0:
            nrTiles = len(self.room) * len(self.room[0])
        else:
            nrTiles = len(self.room)
        return "*** Number of tiles in room: " + str(nrTiles)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.
        Set also random position and random direction (angle in degrees)

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        assert speed > 0, "Speed should be positif: " + str(speed)
        self.speed = speed
        self.direction = random.randint(0,360)
        self.position = self.room.getRandomPosition()
        # Clean tile robot is in
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        Assumption: position of the robot is in the room.
        We cannot check because we don't have the room info.

        position: a Position object.
        """
        self.position = position
        return self.position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        assert 0 <= direction <= 360,  "Angle in degrees out of bound: " + str(direction)
        self.direction = direction
        return self.direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

    def __str__(self):
        """ Testfunction to test output """
        print "*** Testrobot ***"
        print self.position
        #print self.room
        return "*** Speed is " + str(self.speed) + " and direction is " + str(self.direction) + '\n'


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Calculate the new position
        newPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        newDirection = self.getRobotDirection()

        # As long as direction is not in room, then change direction while robot remains on original location
        while not self.room.isPositionInRoom(newPos):
            # Change direction
            newDirection = random.randint(0,360)
            newPos = self.getRobotPosition().getNewPosition(newDirection, self.speed)

        # Update robot with new posiiton and direction
        self.setRobotPosition(newPos)
        self.setRobotDirection(newDirection)
        # Clean tile on new poistion
        self.room.cleanTileAtPosition(newPos)
        return newPos


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    stepList = []  # One timeStep per trial
    # Start trials
    for t in range(num_trials):
        anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.02)
        timeStep = 0
        simRoom = RectangularRoom(width, height)
        robots = []
        for i in range(num_robots):
            newRobot = robot_type(simRoom, speed)
            robots.append(newRobot)

        while float(simRoom.getNumCleanedTiles())/float(simRoom.getNumTiles()) < min_coverage:
            anim.update(simRoom, robots)
            for r in robots:
                r.updatePositionAndClean()
            timeStep += 1

        stepList.append(timeStep)

    anim.done()
    total =  0
    for i in range(len(stepList)):
        total += stepList[i]
    mean = float(total) / float(num_trials)
    return mean


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Calculate the new position
        newPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)

        # As long as direction is not in room, then change direction while robot remains on original location
        while not self.room.isPositionInRoom(newPos):
            # Change direction
            newDirection = random.randint(0,360)
            newPos = self.getRobotPosition().getNewPosition(newDirection, self.speed)

        # Update robot with new positon
        self.setRobotPosition(newPos)
        # Update robot with new random direction
        newDirection = random.randint(0, 360)
        self.setRobotDirection(newDirection)
        # Clean tile on new poistion
        self.room.cleanTileAtPosition(newPos)
        return newPos


# Run vizualization for 1 trial !
#print  runSimulation(1, 1.0, 25, 40, 0.75, 1, StandardRobot)
print  runSimulation(1, 1.0, 25, 40, 0.75, 1, RandomWalkRobot)


# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)