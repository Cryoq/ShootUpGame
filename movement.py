from Constants import *
from abc import ABC, abstractmethod

class Movement(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = WIDTH/2
        self.y = HEIGHT/2
    
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,coord):
        self._x = coord if coord > 0 and coord < WIDTH  else self._x
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, coord):
        self._y = coord if coord > 0 and coord < HEIGHT else self._y

    def moveLeft(self,dec):
        self.x -= dec
        
    def moveRight(self, inc):
        self.x += inc
    
    def moveUp(self,dec):
        self.y -= dec
        
    def moveDown(self, inc):
        self.y += inc
        
    def getPosition(self):
        return self.x, self.y
    
    @abstractmethod
    def update(self):
        raise NotImplementedError("You need an update function")
