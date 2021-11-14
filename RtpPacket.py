import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		#--------------
		# TO COMPLETE
		#--------------
		# Fill the header bytearray with RTP header fields

		# Default fields:
		# 	Set the RTP-version field (V) ==> Version = 2; 
		# 	Set padding (P), extension (X), number of contributing sources (CC), and marker (M) fields. These are all set to zero in this lab ==> Padding = 0; Extension = 0;	CC = 0; Marker = 0; Ssrc = 0;
		# 	Set payload type field (PT)

		# First byte
		header[0] = (header[0] | version << 6) & 0xC0;	# 2 first bits of 8
		header[0] = (header[0] | padding << 5);	# 1 bit next to these 2 above
		header[0] = (header[0] | extension << 4); # 1 bit next to the one above
		header[0] = (header[0] | (cc & 0x0F)); # 4 bits

		# Second byte
		header[1] = (header[1] | marker << 7); # First bit of second byte
		header[1] = (header[1] | (pt & 0x7f)); # The rest bits of second byte

		# Third byte - Sequence number takes 16 bits in total
		header[2] = (seqnum & 0xFF00) >> 8;

		# Forth byte
		header[3] = (seqnum & 0xFF); 

		# Fifth byte - timestamp has 32 bits in total
		header[4] = (timestamp >> 24); # Save first 8 bits of timestamp to header 

		# Sixth byte
		header[5] = (timestamp >> 16) & 0xFF; # Save next 8 bits of timestamp to header

		# Seventh byte
		header[6] = (timestamp >> 8) & 0xFF; # Save next 8 bits of timestamp to header

		# Eighth byte
		header[7] = timestamp & 0xFF; # Save last 8 bits of timestamp to header
		
		# Do the same for saving bits of ssrc - 32 bits
		header[8] = (ssrc >> 24);
		header[9] = (ssrc >> 16) & 0xFF;
		header[10] = (ssrc >> 8) & 0xFF;
		header[11] = ssrc & 0xFF
		# Set completed header to RtpPacket's header 
		self.header = header;

		# Get the payload from the argument
		self.payload = payload;
		
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload