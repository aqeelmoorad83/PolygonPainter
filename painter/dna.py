''' 
Array format:
numPolys, numSides, r, g, b, a, x1, y1, x2, y2... r, g, b, a, x1, y1... 
'''

import numpy
from random import randint, randrange

class Dna:
	imgSize = 0
	def __init__(self, numPolys, numSides):
		self.numPolys = numPolys
		self.headerSize = 2
		self.polyDataLen = 4 + numSides * 2
		self.length = self.headerSize + (numPolys * self.polyDataLen) 
		self.genes = numpy.zeros(self.length, dtype=numpy.int)
		self.genes[0], self.genes[1] = numPolys, numSides

	def mutate(self):
		if randint(0, 100) == 1:
			self.swapPolys(randrange(0, self.numPolys), randrange(0, self.numPolys))
		else:
			index = randrange(self.headerSize, self.length)
			if self.indexIsColour(index):
				self.genes[index] = randint(0, 255)
			else:
				self.genes[index] = randint(0, Dna.imgSize)
				
	def indexIsColour(self, index):
		return (index - self.headerSize) % self.polyDataLen < 4

	def polyAtIndex(self, index):
		offset = self.headerSize + (index * self.polyDataLen)
		colour = tuple(self.genes[offset:offset+4])
		coords = zip(self.genes[offset+4 : offset+self.polyDataLen : 2], self.genes[offset+5 : offset+self.polyDataLen : 2])
		return (colour, coords) 

	def splice(self, other):
		assert other.genes[0] == self.genes[0]
		assert other.genes[1] == self.genes[1]
		child = Dna(self.genes[0], self.genes[1])
		child.genes = [n for tup in zip(self.genes[::2], other.genes[1::2]) for n in tup]
		return child

	def randomisePolys(self):
		for i in xrange(self.headerSize, self.length):
			if not self.indexIsColour(i):
				self.genes[i] = randint(0, Dna.imgSize)

	def swapPolys(self, indexA, indexB):
		a = self.polyOffset(indexA)
		b = self.polyOffset(indexB)
		p = self.polyDataLen - 4
		self.genes[a:a+p], self.genes[b:b+p] = self.genes[b:b+p], self.genes[a:a+p]

	def polyOffset(self, index):
		return self.headerSize + (self.polyDataLen * index) + 4
				

