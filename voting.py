import numbers

class Voting:

	def __init__(self, candidates = []):
		self.candidates = candidates
		self.voteList = []

	def addCandidate(self,name):
		self.candidates.append(name)
		print(f"candidate {name} added.")

	def addVote(self,preferenceList):
		"""
			preferenceList in the shape:
			{preference:name}
		"""
		try:
			assert all([i in self.candidates for i in list(preferenceList.values())])
			assert all([isinstance(i,numbers.Number) for i in preferenceList.keys()])
			self.voteList.append(preferenceList)
			print("Vote added")
		except:
			print("Vote not added.")

	@classmethod
	def getPreferredCandidate(cls, vote):
		minNum = 99999
		currentVote = None
		for preference, candidate in vote.items():
			if preference < minNum:
				minNum = preference
				currentVote = candidate

		return currentVote

	def removeCandidateFromVotes(self, candidate):
		assert candidate in self.candidates
		newVoteList = []

		for vote in self.voteList:
			vote.pop(self.get_key(vote,candidate), None)
			newVoteList.append(vote)

		self.voteList = newVoteList

	def calculateVotes(self):
		votes = {}
		for candidate in self.candidates:
			votes[candidate] = 0

		for vote in self.voteList:
			votes[self.getPreferredCandidate(vote)] += 1

		return votes

	def getMinVoteCandidate(self, votes):
		minNum = 99999
		currentCandidate = None

		for candidate, result in votes.items():
			if result < minNum and result > 0:
				currentCandidate = candidate
				minNum = result

		return currentCandidate


	def checkMajority(self, votes):
		numVotes = len(self.voteList)/2
		numWithVotes = 0

		for candidate, result in votes.items():
			if result > numVotes:
				return candidate
			elif result > 0:
				numWithVotes += 1

		if numWithVotes == 2:
			# In case of tie
			return [key for  key,value in votes.items() if value>0]

		return None


	def calculateResult(self):
		majorityAchieved = False
		electionWinner = None

		while not majorityAchieved:
			votes = self.calculateVotes()
			winner = self.checkMajority(votes)
			if winner is not None:
				majorityAchieved = True
				electionWinner = winner
			else:
				self.removeCandidateFromVotes(self.getMinVoteCandidate(votes))

		return (electionWinner, votes)
	
	@classmethod				    
	def get_key(cls, dictToCheck, val):
	    for key, value in dictToCheck.items():
	         if val == value:
	             return key
	    return -1
