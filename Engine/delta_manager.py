class DeltaManager:
	def __init__(self, delta):
		self._centroids = []
		self._delta = delta
		self._lastMovement = -1	

	def add_Centroid(self, centroid):
		self._centroids.append(centroid)

	def get_Move_Events(self):
		return self._findMovement()
        
	def _findMovement(self):
		start = self._centroids[0]
		nMove = -1
		for x in self._centroids[:0:-1]:
			pMove = _isMovement(start, x)
			if(pMove != -1):
				nMove = pMove
				break;
		
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
		x1, y1 = a
		x2, y2 = b
		
		if self._calculateDelta(0) < abs(x1-x2) and x1 < x2:
			return ("kinect_movement", 0)
		elif self._calculateDelta(1) < abs(x1-x2) and x1 > x2:
			return ("kinect_movement", 2)
		elif self._calculateDelta(2) < abs(y1-y2) and y1 < y2:
			return ("kinect_movement", 1)
		elif self._calculateDelta(3) < abs(y1-y2) and y1 > y2: 
			return ("kinect_movement", 3)
		else:
			return -1
	
	
	def _calculateDelta(self, direction)
		if direction == 0 && self._lastMovement == 1:
			return self._delta * 2
		elif direction == 1 && self._lastMovement == 0:
			return self._delta * 2
		elif direction == 2 && self._lastMovement == 3:
			return self._delta * 2
		elif direction == 3 && self._lastMovement == 2:
			return self._delta * 2

		return self._delta

	
			
		

if(__name__ == "__main__"):
	delta = DeltaManager(2)

	delta.addCentroid((0,0))
	delta.addCentroid((0,1))
	delta.addCentroid((0,2))
	delta.addCentroid((1,0))
	delta.addCentroid((2,0))

	delta._findMovement()
