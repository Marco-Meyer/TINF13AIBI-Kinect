class DeltaManager:
	def __init__(self, delta_x, delta_y):
		self._centroids = []
		self._delta_x = delta_x
		self._delta_y = delta_y
		self._lastMovement = -1	

	def add_Centroid(self, centroid):
		print(centroid)
		self._centroids.append(centroid)

	def get_Move_Events(self):
		return self._findMovement()
        
	def _findMovement(self):
		start = self._centroids[0]
		nMove = -1
		for x in self._centroids[:0:-1]:
			pMove = self._isMovement(start, x)
			if(pMove != -1):
				nMove = pMove
				break
		
		self._centroids = []
		self._lastMovement = nMove
		return nMove


	"""
	-1 - Keine Bewegung
	0 - Rechts
	2 - Links
	1 - Hoch
	3 - Runter
	"""
	def _isMovement(self, a, b):
		dif = b - a

                direction = self._getDirection(dif)

                dic = { 0 : self._delta_x, 1 : self._delta_y, 2 : self._delta_x, 3 : self._delta_y }
                fag = 1;
                
                if direction == 0 and self._lastMovement == 2 or\
                    direction == 1 and self._lastMovement == 3 or\
                    direction == 2 and self._lastMovement == 0 or\
                    direction == 3 and self._lastMovement == 1:
                    fag = 2
                    
		return direction if direction and dif.length >= dic[direction] * fag else -1
	

	def _getDirection(self, centroid):
                tolerance = 10
                for x in range(4):
                        if x * 90 - tolerance < centroid.angle < x * 90 + tolerance:
                                return x
                return None
	
			
		

if(__name__ == "__main__"):
	delta = DeltaManager(2)

	delta.addCentroid((0,0))
	delta.addCentroid((0,1))
	delta.addCentroid((0,2))
	delta.addCentroid((1,0))
	delta.addCentroid((2,0))

	delta._findMovement()
